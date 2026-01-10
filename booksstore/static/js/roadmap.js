/**
 * Roadmap Interactive Functionality
 * Simplified card-based navigation for modern UX
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize roadmap functionality
    initializeRoadmapCards();
    
    // Load roadmap CSS
    loadRoadmapCSS();
});

/**
 * Load roadmap-specific CSS
 */
function loadRoadmapCSS() {
    const cssLink = document.createElement('link');
    cssLink.rel = 'stylesheet';
    cssLink.href = '/static/css/roadmap.css';
    document.head.appendChild(cssLink);
}

/**
 * Initialize roadmap card interactions
 */
function initializeRoadmapCards() {
    const roadmapCards = document.querySelectorAll('.roadmap-card');
    
    // Add enhanced hover effects and keyboard support
    roadmapCards.forEach(card => {
        // Mouse interactions
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        // Keyboard support
        card.setAttribute('tabindex', '0');
        card.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
        
        // Focus styles
        card.addEventListener('focus', function() {
            this.style.outline = '2px solid var(--accent-primary)';
            this.style.outlineOffset = '2px';
        });
        
        card.addEventListener('blur', function() {
            this.style.outline = 'none';
        });
    });
}

/**
 * Intersection Observer for animations
 */
function initializeScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observe roadmap cards
    document.querySelectorAll('.roadmap-card').forEach(card => {
        observer.observe(card);
    });
    
    // Observe transition cards
    document.querySelectorAll('.transition-card').forEach(card => {
        observer.observe(card);
    });
}

/**
 * Initialize all functionality when DOM is ready
 */
function initializeAll() {
    initializeRoadmapCards();
    initializeScrollAnimations();
}

// Initialize scroll animations
initializeScrollAnimations();

// Export functions for external use
window.RoadmapJS = {
    initializeAll
};