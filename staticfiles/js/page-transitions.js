/**
 * Page Transition System
 * Smooth, enterprise-grade page transitions for modern UX
 * DISABLED: Causing navigation issues - using standard browser navigation
 */

class PageTransitions {
    constructor() {
        this.overlay = null;
        this.pageContent = null;
        this.isTransitioning = false;
        // Disable transitions to fix navigation issues
        this.enabled = false;
        this.init();
    }

    init() {
        if (!this.enabled) {
            // Just add page load animation, don't intercept navigation
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', () => this.setupBasicAnimations());
            } else {
                this.setupBasicAnimations();
            }
            return;
        }
        
        // Original transition code (disabled)
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.setup());
        } else {
            this.setup();
        }
    }

    setupBasicAnimations() {
        this.pageContent = document.getElementById('page-content');
        
        // Skip animation for auth pages to prevent disappearing content
        if (window.location.pathname.includes('/login') || 
            window.location.pathname.includes('/signup') ||
            window.location.pathname.includes('/accounts/')) {
            // Ensure content is visible
            if (this.pageContent) {
                this.pageContent.style.opacity = '1';
                this.pageContent.style.transform = 'none';
            }
            return;
        }
        
        // Add initial page load animation only for non-auth pages
        this.animatePageIn();
    }

    setup() {
        this.overlay = document.getElementById('page-transition-overlay');
        this.pageContent = document.getElementById('page-content');
        
        // Add initial page load animation
        this.animatePageIn();
        
        // DON'T intercept navigation - this was causing the double-click issue
        // this.interceptNavigation();
        
        // Handle browser back/forward
        window.addEventListener('popstate', (e) => {
            if (e.state && e.state.url) {
                this.navigateToPage(e.state.url, false);
            }
        });
    }

    interceptNavigation() {
        // DISABLED: This was causing the double-click navigation issue
        // Let the browser handle navigation normally
        return;
        
        // Original code (commented out):
        /*
        document.addEventListener('click', (e) => {
            const link = e.target.closest('a');
            
            if (!link) return;
            
            if (this.isInternalLink(link)) {
                e.preventDefault();
                this.navigateToPage(link.href, true);
            }
        });
        */
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
        // Disabled - use normal browser navigation
        window.location.href = url;
        return;
        
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
            if (this.overlay) {
                this.overlay.style.display = 'flex';
                this.overlay.style.opacity = '0';
            }
            
            // Fade out content
            if (this.pageContent) {
                this.pageContent.style.opacity = '0';
                this.pageContent.style.transform = 'translateY(20px)';
            }
            
            // Fade in overlay
            requestAnimationFrame(() => {
                if (this.overlay) {
                    this.overlay.style.opacity = '1';
                }
                
                setTimeout(resolve, 200);
            });
        });
    }

    async animatePageIn() {
        return new Promise((resolve) => {
            if (!this.pageContent) {
                resolve();
                return;
            }
            
            // Skip animation for auth pages - keep content visible
            if (window.location.pathname.includes('/login') || 
                window.location.pathname.includes('/signup') ||
                window.location.pathname.includes('/accounts/')) {
                this.pageContent.style.opacity = '1';
                this.pageContent.style.transform = 'none';
                if (this.overlay) {
                    this.overlay.style.display = 'none';
                }
                resolve();
                return;
            }
            
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
        // Clear any existing roadmap state
        if (window.roadmapManager) {
            window.roadmapManager.cleanup();
        }
        
        // Reinitialize roadmap functionality if present
        if (window.RoadmapJS && typeof window.RoadmapJS.initializeAll === 'function') {
            // Add a small delay to ensure DOM is ready
            setTimeout(() => {
                window.RoadmapJS.initializeAll();
            }, 100);
        }

        // Reinitialize any other page-specific functionality
        const event = new CustomEvent('pageTransitionComplete');
        document.dispatchEvent(event);
    }
}

// Initialize page transitions (disabled mode)
const pageTransitions = new PageTransitions();

// Export for external use
window.PageTransitions = PageTransitions;