/**
 * Page Transition System
 * Smooth, enterprise-grade page transitions for modern UX
 */

class PageTransitions {
    constructor() {
        this.overlay = null;
        this.pageContent = null;
        this.isTransitioning = false;
        this.init();
    }

    init() {
        // Wait for DOM to be ready
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }

    setup() {
        this.overlay = document.getElementById('page-transition-overlay');
        this.pageContent = document.getElementById('page-content');
        
        // Add initial page load animation
        this.animatePageIn();
        
        // Intercept navigation clicks
        this.interceptNavigation();
        
        // Handle browser back/forward
        window.addEventListener('popstate', (e) => {
            if (e.state && e.state.url) {
                this.navigateToPage(e.state.url, false);
            }
        });
    }

    interceptNavigation() {
        // Intercept all internal links
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            
            if (!link) return;
            
            // Check if it's an internal link
            if (this.isInternalLink(link)) {
                e.preventDefault();
                this.navigateToPage(link.href, true);
            }
        });
    }

    isInternalLink(link) {
        // Skip if it's an external link, has target="_blank", or is a download
        if (link.target === '_blank' || 
            link.download || 
            link.href.startsWith('mailto:') || 
            link.href.startsWith('tel:') ||
            link.href.includes('#') ||
            !link.href.startsWith(window.location.origin)) {
            return false;
        }

        // Skip if it's the current page
        if (link.href === window.location.href) {
            return false;
        }

        return true;
    }

    async navigateToPage(url, addToHistory = true) {
        if (this.isTransitioning) return;
        
        this.isTransitioning = true;
        
        try {
            // Start transition out
            await this.animatePageOut();
            
            // Fetch new page content
            const response = await fetch(url);
            const html = await response.text();
            
            // Parse the new page
            const parser = new DOMParser();
            const newDoc = parser.parseFromString(html, 'text/html');
            const newContent = newDoc.getElementById('page-content');
            const newTitle = newDoc.title;
            
            if (newContent) {
                // Update page content
                this.pageContent.innerHTML = newContent.innerHTML;
                document.title = newTitle;
                
                // Update URL
                if (addToHistory) {
                    history.pushState({ url }, newTitle, url);
                }
                
                // Animate new content in
                await this.animatePageIn();
                
                // Reinitialize any page-specific scripts
                this.reinitializeScripts();
            }
        } catch (error) {
            console.error('Navigation error:', error);
            // Fallback to normal navigation
            window.location.href = url;
        } finally {
            this.isTransitioning = false;
        }
    }

    async animatePageOut() {
        return new Promise((resolve) => {
            // Show overlay
            this.overlay.style.display = 'flex';
            this.overlay.style.opacity = '0';
            
            // Fade out content
            this.pageContent.style.opacity = '0';
            this.pageContent.style.transform = 'translateY(20px)';
            
            // Fade in overlay
            requestAnimationFrame(() => {
                this.overlay.style.opacity = '1';
                
                setTimeout(resolve, 200);
            });
        });
    }

    async animatePageIn() {
        return new Promise((resolve) => {
            // Reset content position
            this.pageContent.style.opacity = '0';
            this.pageContent.style.transform = 'translateY(30px)';
            
            requestAnimationFrame(() => {
                // Fade out overlay
                if (this.overlay) {
                    this.overlay.style.opacity = '0';
                }
                
                // Fade in content
                this.pageContent.style.opacity = '1';
                this.pageContent.style.transform = 'translateY(0)';
                
                setTimeout(() => {
                    if (this.overlay) {
                        this.overlay.style.display = 'none';
                    }
                    
                    // Animate page elements
                    this.animatePageElements();
                    resolve();
                }, 300);
            });
        });
    }

    animatePageElements() {
        // Animate roadmap cards if present
        const roadmapCards = document.querySelectorAll('.roadmap-card');
        roadmapCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.4s ease-out';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });

        // Animate phase cards if present
        const phaseCards = document.querySelectorAll('.phase-card');
        phaseCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.4s ease-out';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 150);
        });

        // Animate transition cards if present
        const transitionCards = document.querySelectorAll('.transition-card');
        transitionCards.forEach((card, index) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(30px)';
            
            setTimeout(() => {
                card.style.transition = 'all 0.4s ease-out';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, index * 100);
        });

        // Animate path header if present
        const pathHeader = document.querySelector('.path-header');
        if (pathHeader) {
            pathHeader.style.opacity = '0';
            pathHeader.style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                pathHeader.style.transition = 'all 0.5s ease-out';
                pathHeader.style.opacity = '1';
                pathHeader.style.transform = 'translateY(0)';
            }, 100);
        }

        // Animate breadcrumb if present
        const breadcrumb = document.querySelector('.breadcrumb-nav');
        if (breadcrumb) {
            breadcrumb.style.opacity = '0';
            breadcrumb.style.transform = 'translateX(-20px)';
            
            setTimeout(() => {
                breadcrumb.style.transition = 'all 0.3s ease-out';
                breadcrumb.style.opacity = '1';
                breadcrumb.style.transform = 'translateX(0)';
            }, 50);
        }
    }

    reinitializeScripts() {
        // Reinitialize roadmap functionality if present
        if (window.RoadmapJS && typeof window.RoadmapJS.initializeAll === 'function') {
            window.RoadmapJS.initializeAll();
        }

        // Reinitialize any other page-specific functionality
        const event = new CustomEvent('pageTransitionComplete');
        document.dispatchEvent(event);
    }
}

// Initialize page transitions
const pageTransitions = new PageTransitions();

// Export for external use
window.PageTransitions = PageTransitions;