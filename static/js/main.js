/**
 * I.A.E™ - Main JavaScript with GSAP
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // ========================================
    // GSAP CONFIG
    // ========================================
    gsap.registerPlugin(ScrollTrigger);
    
    // ========================================
    // NAVBAR
    // ========================================
    const navbar = document.getElementById('navbar');
    const hamburger = document.getElementById('hamburger');
    const navMenu = document.getElementById('navMenu');
    
    // Navbar scroll
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });
    
    // Mobile menu
    if (hamburger) {
        hamburger.addEventListener('click', (e) => {
            e.stopPropagation();
            navMenu.classList.toggle('active');
        });
    }
    
    document.querySelectorAll('.nav-menu a').forEach(link => {
        link.addEventListener('click', () => {
            navMenu.classList.remove('active');
        });
    });
    
    document.addEventListener('click', (e) => {
        if (navMenu.classList.contains('active')) {
            if (!navMenu.contains(e.target) && !hamburger.contains(e.target)) {
                navMenu.classList.remove('active');
            }
        }
    });
    
    // ========================================
    // HERO ANIMATIONS
    // ========================================
    const heroTL = gsap.timeline({ defaults: { ease: 'power3.out' } });
    
    heroTL
        .from('.hero-content h1', {
            opacity: 0,
            y: 60,
            duration: 1
        })
        .from('.hero-content p', {
            opacity: 0,
            y: 40,
            duration: 0.8
        }, '-=0.5')
        .from('.hero-buttons .btn', {
            opacity: 0,
            y: 30,
            duration: 0.6,
            stagger: 0.15
        }, '-=0.4')
        .from('.hero-trust span', {
            opacity: 0,
            y: 20,
            duration: 0.5,
            stagger: 0.1
        }, '-=0.3')
        .from('.stat-card', {
            opacity: 0,
            y: 40,
            duration: 0.8,
            stagger: 0.2
        }, '-=0.3');
    
    // ========================================
    // COUNTERS
    // ========================================
    const counters = document.querySelectorAll('.stat-number');
    let countersAnimated = false;
    
    function animateCounters() {
        if (countersAnimated) return;
        countersAnimated = true;
        
        counters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-count'));
            const duration = 2000;
            const startTime = performance.now();
            
            function updateCounter(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const eased = 1 - Math.pow(1 - progress, 3);
                const current = Math.floor(eased * target);
                
                counter.textContent = current.toLocaleString();
                
                if (progress < 1) {
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target.toLocaleString();
                }
            }
            
            requestAnimationFrame(updateCounter);
        });
    }
    
    const statsContainer = document.querySelector('.hero-stats');
    if (statsContainer) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateCounters();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });
        
        observer.observe(statsContainer);
    }
    
    // ========================================
    // ABOUT PREVIEW
    // ========================================
    gsap.from('.about-image', {
        scrollTrigger: {
            trigger: '.about-preview',
            start: 'top 80%',
            toggleActions: 'play none none none'
        },
        opacity: 0,
        x: -50,
        duration: 1,
        ease: 'power3.out'
    });
    
    gsap.from('.about-content', {
        scrollTrigger: {
            trigger: '.about-preview',
            start: 'top 80%',
            toggleActions: 'play none none none'
        },
        opacity: 0,
        x: 50,
        duration: 1,
        ease: 'power3.out'
    });
    
    // ========================================
    // SERVICES
    // ========================================
    const serviceCards = document.querySelectorAll('.service-card');
    
    serviceCards.forEach((card, index) => {
        gsap.from(card, {
            scrollTrigger: {
                trigger: card,
                start: 'top 85%',
                toggleActions: 'play none none none'
            },
            opacity: 0,
            y: 40,
            duration: 0.8,
            delay: index * 0.1,
            ease: 'power3.out'
        });
    });
    
    // ========================================
    // JAMB BOX
    // ========================================
    gsap.from('.jamb-box', {
        scrollTrigger: {
            trigger: '.jamb-box',
            start: 'top 80%',
            toggleActions: 'play none none none'
        },
        opacity: 0,
        scale: 0.96,
        duration: 1,
        ease: 'power3.out'
    });
    
    // ========================================
    // FLASH MESSAGES
    // ========================================
    const flashMessages = document.querySelectorAll('.flash-message');
    flashMessages.forEach(msg => {
        setTimeout(() => {
            msg.style.opacity = '0';
            msg.style.transform = 'translateX(40px)';
            msg.style.transition = 'all 0.5s ease';
            setTimeout(() => msg.remove(), 500);
        }, 5000);
    });
    
    // ========================================
    // PAGE-SPECIFIC: About Page Counters
    // ========================================
    const aboutCounters = document.querySelectorAll('.story-stats .stat-number');
    let aboutCountersAnimated = false;
    
    function animateAboutCounters() {
        if (aboutCountersAnimated) return;
        aboutCountersAnimated = true;
        
        aboutCounters.forEach(counter => {
            const target = parseInt(counter.getAttribute('data-count'));
            const duration = 2000;
            const startTime = performance.now();
            
            function updateCounter(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const eased = 1 - Math.pow(1 - progress, 3);
                const current = Math.floor(eased * target);
                
                counter.textContent = current.toLocaleString();
                
                if (progress < 1) {
                    requestAnimationFrame(updateCounter);
                } else {
                    counter.textContent = target.toLocaleString();
                }
            }
            
            requestAnimationFrame(updateCounter);
        });
    }
    
    const storyStats = document.querySelector('.story-stats');
    if (storyStats) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    animateAboutCounters();
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.3 });
        
        observer.observe(storyStats);
    }
    
    // ========================================
    // PAGE-SPECIFIC: Services Tabs
    // ========================================
    const tabBtns = document.querySelectorAll('.tab-btn');
    const serviceCardsGrid = document.querySelectorAll('.service-card');
    
    if (tabBtns.length > 0) {
        tabBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                tabBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                const category = btn.getAttribute('data-category');
                
                serviceCardsGrid.forEach(card => {
                    if (category === 'all' || card.getAttribute('data-category') === category) {
                        card.style.display = 'block';
                        setTimeout(() => {
                            card.style.opacity = '1';
                            card.style.transform = 'translateY(0)';
                        }, 10);
                    } else {
                        card.style.opacity = '0';
                        card.style.transform = 'translateY(20px)';
                        setTimeout(() => {
                            card.style.display = 'none';
                        }, 300);
                    }
                });
            });
        });
    }
    
    // ========================================
    // CONSOLE
    // ========================================
    console.log('🎓 I.A.E™ — INTERDENOMINATIONAL ACADEMIC EXCELLENCE');
    console.log('✅ Modern UI loaded with GSAP');
    console.log('🚀 Excellence is our standard');
});
