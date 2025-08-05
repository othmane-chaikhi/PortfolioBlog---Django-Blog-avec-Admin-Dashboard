// ===== MODERN PORTFOLIO JAVASCRIPT =====

// DOM Elements
const themeToggle = document.getElementById('themeToggle');
const themeIcon = document.querySelector('.theme-icon');
const body = document.body;

// Theme Management
let currentTheme = localStorage.getItem('theme') || 'light';

// Initialize theme
function initTheme() {
    body.setAttribute('data-theme', currentTheme);
    updateThemeIcon();
}

// Update theme icon
function updateThemeIcon() {
    if (currentTheme === 'dark') {
        themeIcon.className = 'bi bi-sun-fill theme-icon';
    } else {
        themeIcon.className = 'bi bi-moon-fill theme-icon';
    }
}

// Toggle theme
function toggleTheme() {
    currentTheme = currentTheme === 'light' ? 'dark' : 'light';
    body.setAttribute('data-theme', currentTheme);
    localStorage.setItem('theme', currentTheme);
    updateThemeIcon();

    // Add theme transition effect
    body.style.transition = 'all 0.3s ease';
    setTimeout(() => {
        body.style.transition = '';
    }, 300);
}

 // Typing Animation with Typed.js
   function initTypingAnimation() {
    const typedElement = document.getElementById('typed-text');
    console.log('typedElement:', typedElement);
    console.log('Typed is:', typeof Typed);

    if (typedElement && typeof Typed !== 'undefined') {
        console.log("Creating Typed instance...");
        const typed = new Typed('#typed-text', {
            strings: [
                'Bonjour, je suis Othmane Chaikhi',
                'Ingénieur en Informatique',
                'Développeur Full Stack',
                'Passionné par la Tech'
            ],
            typeSpeed: 80,
            backSpeed: 50,
            backDelay: 1500,
            startDelay: 400,
            loop: true,
            showCursor: false
        });
    } else {
        console.warn('Typed.js or element not available.');
    }
}


// Intersection Observer for animations
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');

                // Trigger skill bars animation
                if (entry.target.id === 'about-section') {
                    animateSkillBars();
                }
            }
        });
    }, observerOptions);

    // Observe all fade-in sections
    document.querySelectorAll('.fade-in-section').forEach(section => {
        observer.observe(section);
    });
}

// Animate skill progress bars
function animateSkillBars() {
    const skillBars = document.querySelectorAll('.progress-bar');

    skillBars.forEach((bar, index) => {
        const width = bar.getAttribute('data-width');
        setTimeout(() => {
            bar.style.width = width + '%';
        }, index * 200);
    });
}

// Add ripple effect to buttons
function addRippleEffect() {
    const buttons = document.querySelectorAll('.cta-button');

    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;

            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');

            this.appendChild(ripple);

            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
}

// Add hover effects to skill badges
function initSkillBadges() {
    const badges = document.querySelectorAll('.modern-badge');

    badges.forEach(badge => {
        badge.addEventListener('mouseenter', function() {
            this.style.animationDelay = Math.random() * 0.5 + 's';
            this.style.animation = 'pulse 0.6s ease-in-out';
        });

        badge.addEventListener('animationend', function() {
            this.style.animation = '';
        });
    });
}

// Add floating animation to profile image
function initProfileAnimation() {
    const profileImg = document.querySelector('.profile-img');
    if (profileImg) {
        let isFloating = false;

        profileImg.addEventListener('mouseenter', function() {
            if (!isFloating) {
                isFloating = true;
                this.style.animation = 'float 2s ease-in-out infinite';
            }
        });

        profileImg.addEventListener('mouseleave', function() {
            isFloating = false;
            this.style.animation = '';
        });
    }
}

// Add smooth scrolling for navigation links
function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Add parallax effect to hero section
function initParallaxEffect() {
    const hero = document.querySelector('.hero-section');
    if (hero) {
        window.addEventListener('scroll', () => {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            hero.style.transform = `translateY(${rate}px)`;
        });
    }
}

// Add loading animation to buttons
function initButtonLoading() {
    const buttons = document.querySelectorAll('.modern-btn');

    buttons.forEach(button => {
        button.addEventListener('click', function(e) {
            // Don't add loading for external links
            if (this.getAttribute('href') && this.getAttribute('href').startsWith('http')) {
                return;
            }

            this.classList.add('loading');
            setTimeout(() => {
                this.classList.remove('loading');
            }, 1000);
        });
    });
}

// Add card tilt effect
function initCardTiltEffect() {
    const cards = document.querySelectorAll('.modern-card');

    cards.forEach(card => {
        card.addEventListener('mousemove', function(e) {
            const rect = this.getBoundingClientRect();
            const x = e.clientX - rect.left;
            const y = e.clientY - rect.top;

            const centerX = rect.width / 2;
            const centerY = rect.height / 2;

            const rotateX = (y - centerY) / 10;
            const rotateY = -(x - centerX) / 10;

            this.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) translateY(-10px)`;
        });

        card.addEventListener('mouseleave', function() {
            this.style.transform = '';
        });
    });
}

// Add dynamic background to navigation
function initDynamicNav() {
    const nav = document.querySelector('.modern-nav');

    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            nav.style.background = 'rgba(31, 41, 55, 0.98)';
            nav.style.backdropFilter = 'blur(20px)';
        } else {
            nav.style.background = 'rgba(31, 41, 55, 0.95)';
            nav.style.backdropFilter = 'blur(10px)';
        }
    });
}

// Performance optimization: Throttle scroll events
function throttle(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add CSS keyframes dynamically
function addDynamicKeyframes() {
    const style = document.createElement('style');
    style.textContent = `
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-20px); }
        }

        .ripple {
            position: absolute;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: scale(0);
            animation: rippleAnimation 0.6s linear;
            pointer-events: none;
        }

        @keyframes rippleAnimation {
            to {
                transform: scale(4);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);
}

// Initialize everything when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Core functionality
    initTheme();
    initTypingAnimation();
    initScrollAnimations();

    // Interactive effects
    addRippleEffect();
    initSkillBadges();
    initProfileAnimation();
    initSmoothScrolling();
    initButtonLoading();
    initCardTiltEffect();
    initDynamicNav();

    // Add dynamic styles
    addDynamicKeyframes();

    // Event listeners
    if (themeToggle) {
        themeToggle.addEventListener('click', toggleTheme);
    }

    // Optimize scroll events
    const optimizedScrollHandler = throttle(() => {
        // Any scroll-based animations can be added here
    }, 16); // ~60fps

    window.addEventListener('scroll', optimizedScrollHandler);

    // Add focus styles for accessibility
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            document.body.classList.add('using-keyboard');
        }
    });

    document.addEventListener('mousedown', function() {
        document.body.classList.remove('using-keyboard');
    });

    // Console welcome message
    console.log(`
    🎨 Portfolio moderne chargé avec succès!
    🚀 Animations et interactions activées
    🌙 Mode sombre disponible
    ⚡ Performance optimisée

    Développé avec ❤️ par Othmane Chaikhi
    `);
});

// Handle page visibility changes for performance
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        // Pause animations when page is not visible
        document.body.style.animationPlayState = 'paused';
    } else {
        // Resume animations when page becomes visible
        document.body.style.animationPlayState = 'running';
    }
});

// Add error handling for typing animation
window.addEventListener('error', function(e) {
    if (e.message.includes('Typed')) {
        console.warn('Typed.js not loaded, falling back to simple text display');
        const typedElement = document.getElementById('typed-text');
        if (typedElement) {
            typedElement.textContent = 'Bonjour, je suis Othmane Chaikhi';
        }
    }
});