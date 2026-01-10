/**
 * Roadmap Interactive Functionality
 * Stable, consistent animations with proper state management
 */

class RoadmapManager {
    constructor() {
        this.isInitialized = false;
        this.currentPath = null;
        this.animationQueue = [];
        this.isAnimating = false;
        
        this.init();
    }

    init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }

    setup() {
        if (this.isInitialized) {
            this.cleanup();
        }
        
        this.loadRoadmapCSS();
        this.initializeRoadmapCards();
        this.initializeScrollAnimations();
        this.setupStateManagement();
        
        this.isInitialized = true;
    }

    cleanup() {
        // Clear any existing animations
        this.animationQueue = [];
        this.isAnimating = false;
        
        // Remove event listeners
        const cards = document.querySelectorAll('.roadmap-card');
        cards.forEach(card => {
            card.replaceWith(card.cloneNode(true));
        });
    }

    loadRoadmapCSS() {
        // Only load CSS once
        if (!document.querySelector('link[href*="roadmap.css"]')) {
            const cssLink = document.createElement('link');
            cssLink.rel = 'stylesheet';
            cssLink.href = '/static/css/roadmap.css';
            cssLink.onload = () => {
                // CSS loaded, safe to animate
                this.triggerInitialAnimations();
            };
            document.head.appendChild(cssLink);
        } else {
            this.triggerInitialAnimations();
        }
    }

    setupStateManagement() {
        // Get current page state
        const pageType = document.body.dataset.pageType || 
                        (window.location.pathname.includes('/roadmap/path/') ? 'roadmap_detail' : 'roadmap_home');
        
        const pathSlug = document.body.dataset.pathSlug || 
                        window.location.pathname.split('/').pop();
        
        // Clear previous state if path changed
        if (this.currentPath && this.currentPath !== pathSlug) {
            this.cleanup();
        }
        
        this.currentPath = pathSlug;
        
        // Set page-specific data attributes for CSS targeting
        document.body.setAttribute('data-page-type', pageType);
        if (pathSlug && pathSlug !== 'roadmap') {
            document.body.setAttribute('data-path-slug', pathSlug);
        }
    }

    initializeRoadmapCards() {
        const roadmapCards = document.querySelectorAll('.roadmap-card');
        
        roadmapCards.forEach((card, index) => {
            // Reset any existing styles
            card.style.transform = '';
            card.style.transition = '';
            
            // Add enhanced hover effects
            this.setupCardInteractions(card);
            
            // Set initial state for animation
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
        });
    }

    setupCardInteractions(card) {
        // Remove existing listeners
        const newCard = card.cloneNode(true);
        card.parentNode.replaceChild(newCard, card);
        
        // Mouse interactions
        newCard.addEventListener('mouseenter', function() {
            if (!this.style.transform.includes('translateY(30px)')) {
                this.style.transform = 'translateY(-8px) scale(1.02)';
            }
        });
        
        newCard.addEventListener('mouseleave', function() {
            if (!this.style.transform.includes('translateY(30px)')) {
                this.style.transform = 'translateY(0) scale(1)';
            }
        });
        
        // Keyboard support
        newCard.setAttribute('tabindex', '0');
        newCard.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
        
        // Focus styles
        newCard.addEventListener('focus', function() {
            this.style.outline = '2px solid var(--accent-primary)';
            this.style.outlineOffset = '2px';
        });
        
        newCard.addEventListener('blur', function() {
            this.style.outline = 'none';
        });
    }

    triggerInitialAnimations() {
        if (this.isAnimating) return;
        
        this.isAnimating = true;
        
        // Animate roadmap cards
        const roadmapCards = document.querySelectorAll('.roadmap-card');
        roadmapCards.forEach((card, index) => {
            setTimeout(() => {
                card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
                
                if (index === roadmapCards.length - 1) {
                    setTimeout(() => {
                        this.isAnimating = false;
                    }, 600);
                }
            }, index * 150);
        });

        // Animate transition cards
        const transitionCards = document.querySelectorAll('.transition-card');
        transitionCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, (index * 100) + 200);
        });

        // Animate phase cards if present
        const phaseCards = document.querySelectorAll('.phase-card');
        phaseCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, (index * 100) + 300);
        });
    }

    initializeScrollAnimations() {
        // Only initialize if IntersectionObserver is supported
        if (!window.IntersectionObserver) return;
        
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting && !entry.target.classList.contains('animate-in')) {
                    entry.target.classList.add('animate-in');
                }
            });
        }, observerOptions);
        
        // Observe elements that haven't been animated yet
        document.querySelectorAll('.roadmap-card:not(.animate-in)').forEach(card => {
            observer.observe(card);
        });
        
        document.querySelectorAll('.transition-card:not(.animate-in)').forEach(card => {
            observer.observe(card);
        });
    }

    // Public method to reinitialize (called by page transitions)
    reinitialize() {
        this.setup();
    }
}

// Initialize roadmap manager
let roadmapManager;

document.addEventListener('DOMContentLoaded', function() {
    roadmapManager = new RoadmapManager();
});

// Handle page transition reinitialization
document.addEventListener('pageTransitionComplete', function() {
    if (roadmapManager) {
        roadmapManager.reinitialize();
    }
});

// Export for external use
window.RoadmapJS = {
    initializeAll: () => {
        if (roadmapManager) {
            roadmapManager.reinitialize();
        } else {
            roadmapManager = new RoadmapManager();
        }
    },
    manager: () => roadmapManager
};