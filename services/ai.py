import os
import logging
import requests
from config import Config

log = logging.getLogger(__name__)


class AIService:
    """Groq-backed chat with a rule-based fallback."""

    @staticmethod
    def get_response(user_message, username):
        if not Config.GROQ_API_KEY:
            return AIService._fallback(user_message, username)

        try:
            r = requests.post(
                Config.GROQ_API_URL,
                headers={
                    'Authorization': f'Bearer {Config.GROQ_API_KEY}',
                    'Content-Type': 'application/json',
                },
                json={
                    'model': Config.GROQ_MODEL,
                    'messages': [
                        {'role': 'system', 'content': AIService._system_prompt()},
                        {'role': 'user', 'content': user_message},
                    ],
                    'temperature': 0.7,
                    'max_tokens': 500,
                },
                timeout=20,
            )
            r.raise_for_status()
            return r.json()['choices'][0]['message']['content']
        except requests.Timeout:
            log.warning('AI timeout')
            return AIService._fallback(user_message, username)
        except Exception as e:
            log.exception('AI error: %s', e)
            return AIService._fallback(user_message, username)

    @staticmethod
    def _system_prompt():
        return """You are I.A.E Assistant, the official AI helper for INTERDENOMINATIONAL ACADEMIC EXCELLENCE (I.A.E™), founded by Mr. Daniel Moses.

About I.A.E:
- Founded by Mr. Daniel Moses
- Specializes in JAMB, WAEC, NECO, and admission guidance
- Has helped over 25,000 students gain university admission

Style:
- Friendly, concise (2-3 short paragraphs max)
- Focus on Nigerian education context
- Practical, actionable advice"""

    @staticmethod
    def _fallback(user_message, username):
        msg = user_message.lower()

        if any(w in msg for w in ('founder', 'mr daniel', 'owner', 'who created')):
            return "I.A.E™ was founded by Mr. Daniel Moses. His vision: give Nigerian students honest, expert guidance through JAMB, WAEC, and admission — without the guesswork. 🎓"

        if 'jamb' in msg:
            return "For JAMB: start early with past questions, drill your weak subjects, take mock CBTs, and don't leave registration late. I.A.E has helped thousands score 280+. Want the masterclass details? 🎯"

        if 'waec' in msg:
            return "WAEC prep at I.A.E focuses on past-question analysis, time management, and intensive mocks. Our students routinely pull excellent results. 📝"

        if any(w in msg for w in ('admission', 'university')):
            return "Admission in Nigeria is a maze — CAPS, cut-offs, supplementary lists. I.A.E has walked 6,200+ students through it. Tell me your course and target school and I'll point the way. 🏛️"

        if any(w in msg for w in ('hello', 'hi', 'hey')):
            return f"Hello {username}! I'm the I.A.E assistant. JAMB, WAEC, admissions, NIN — ask away. 😊"

        return "Ask me about JAMB, WAEC, admissions, certificates, or NIN — or WhatsApp us on 0707 939 6111 for a human reply."