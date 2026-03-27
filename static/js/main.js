/**
 * I.A.E™ - Main JavaScript File
 * Handles navigation, animations, counters, and interactive elements
 */

// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    
    // Initialize AOS (Animate On Scroll)
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 700,
            once: true,
            offset: 30,
            easing: 'ease-out-quad'
        });
    }

    // ========================================
    // MOBILE NAVIGATION TOGGLE
    // ========================================
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');

    if (hamburger) {
        hamburger.addEventListener('click', (e) => {
            e.stopPropagation();
            navMenu.classList.toggle('active');
        });
    }

    // Close mobile menu when clicking a link
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', () => {
            if (navMenu) {
                navMenu.classList.remove('active');
            }
        });
    });

    // Close menu when clicking outside (for mobile)
    document.addEventListener('click', (e) => {
        if (navMenu && navMenu.classList.contains('active')) {
            if (!navMenu.contains(e.target) && !hamburger.contains(e.target)) {
                navMenu.classList.remove('active');
            }
        }
    });

    // ========================================
    // ANIMATED COUNTER FOR STATS
    // ========================================
    const counters = document.querySelectorAll('.stat-number');
    let counted = false;

    function startCounters() {
        if (counted) return;
        counted = true;

        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-count'));
            let current = 0;
            const increment = target / 50;

            const updateCounter = () => {
                if (current < target) {
                    current += increment;
                    counter.innerText = Math.floor(current);
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.innerText = target.toLocaleString();
                }
            };

            updateCounter();
        });
    }

    // Observe stats container to trigger counters when visible
    const statsContainer = document.querySelector('.hero-stats');
    if (statsContainer && counters.length > 0) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    startCounters();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });

        observer.observe(statsContainer);
    }

    // ========================================
    // NAVBAR SCROLL EFFECT
    // ========================================
    const navbar = document.querySelector('.navbar');

    window.addEventListener('scroll', () => {
        if (navbar) {
            if (window.scrollY > 50) {
                navbar.style.boxShadow = '0 8px 20px rgba(0, 0, 0, 0.08)';
            } else {
                navbar.style.boxShadow = 'var(--shadow-sm)';
            }
        }
    });

    // ========================================
    // ACTIVE NAVIGATION LINK HIGHLIGHT
    // ========================================
    // Get current path without domain and query params
    const currentPath = window.location.pathname.split('/').pop() || 'index.html';
    document.querySelectorAll('.nav-menu a').forEach(link => {
        const linkHref = link.getAttribute('href');
        if (linkHref === currentPath || 
            (currentPath === '' && linkHref === 'index.html') ||
            (linkHref === currentPath.replace('.html', ''))) {
            link.classList.add('active');
        }
    });

    // ========================================
    // SMOOTH SCROLL FOR ANCHOR LINKS
    // ========================================
    document.querySelectorAll('a[href^="#"]:not([href="#"])').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const targetId = this.getAttribute('href');
            const target = document.querySelector(targetId);
            if (target) {
                e.preventDefault();
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // ========================================
    // SERVICE CARD HOVER EFFECT
    // ========================================
    const serviceCards = document.querySelectorAll('.service-card');
    serviceCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            card.style.transition = 'all 0.3s ease';
        });
    });

    // ========================================
    // LAZY LOAD IMAGES WITH FALLBACK
    // ========================================
    const images = document.querySelectorAll('img');
    images.forEach(img => {
        img.addEventListener('error', function() {
            if (!this.hasAttribute('data-fallback')) {
                this.setAttribute('data-fallback', 'true');
                const width = this.width || 300;
                const height = this.height || 300;
                const text = this.alt || 'Image';
                this.src = `https://placehold.co/${width}x${height}/1E5A6F/white?text=${encodeURIComponent(text)}`;
            }
        });
    });

    // ========================================
    // ADD SCROLL REVEAL FOR ADDITIONAL ELEMENTS
    // ========================================
    const revealElements = document.querySelectorAll('.service-card, .about-grid, .jamb-box');
    if (revealElements.length > 0) {
        const revealObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('revealed');
                    revealObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.2 });

        revealElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(30px)';
            el.style.transition = 'all 0.6s ease-out';
            revealObserver.observe(el);
        });

        // Add class for revealed animation
        const style = document.createElement('style');
        style.textContent = `
            .service-card.revealed,
            .about-grid.revealed,
            .jamb-box.revealed {
                opacity: 1 !important;
                transform: translateY(0) !important;
            }
        `;
        document.head.appendChild(style);
    }

    // ========================================
    // AUTO-HIDE FLASH MESSAGES
    // ========================================
    const flashMessages = document.querySelectorAll('.flash-message');
    if (flashMessages.length > 0) {
        setTimeout(() => {
            flashMessages.forEach(msg => {
                msg.style.opacity = '0';
                msg.style.transition = 'opacity 0.5s ease';
                setTimeout(() => {
                    msg.style.display = 'none';
                }, 500);
            });
        }, 5000);
    }

    // ========================================
    // CONSOLE LOG (welcome message)
    // ========================================
    console.log('🎓 I.A.E™ — INTERDENOMINATIONAL ACADEMIC EXCELLENCE');
    console.log('✅ Website loaded successfully | Excellence is our standard');
    console.log('🚀 Flask Web App | AI Assistant Active | PostgreSQL Connected');

    // ========================================
    // PREVENT DOUBLE SCROLL ON MOBILE MENU
    // ========================================
    if (hamburger) {
        hamburger.addEventListener('click', (e) => {
            e.stopPropagation();
        });
    }

    // Close menu on window resize (if open)
    window.addEventListener('resize', () => {
        if (window.innerWidth > 968 && navMenu && navMenu.classList.contains('active')) {
            navMenu.classList.remove('active');
        }
    });
});
