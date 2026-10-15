from urllib.parse import urlparse, urljoin
from flask import request
import re


def is_safe_redirect(target):
    """Prevent open-redirect attacks. Only allow same-host URLs."""
    if not target:
        return False
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


_WHITESPACE = re.compile(r'\s+')
_CTRL = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')


def clean_text(value, max_len=None, strip_html=True):
    """Trim, drop control chars, optionally strip HTML tags, enforce length."""
    if value is None:
        return ''
    value = _CTRL.sub('', str(value)).strip()
    if strip_html:
        value = re.sub(r'<[^>]*>', '', value)
    value = _WHITESPACE.sub(' ', value)
    if max_len:
        value = value[:max_len]
    return value