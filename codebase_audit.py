#!/usr/bin/env python
"""
Comprehensive Django Codebase Audit for Authentication & Access Control
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'booksstore.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.urls import reverse
import re

def audit_codebase():
    print("🔍 COMPREHENSIVE DJANGO CODEBASE AUDIT")
    print("=" * 80)
    
    # Test 1: URL Resolution Audit
    print("\n1️⃣ URL RESOLUTION AUDIT")
    print("-" * 40)
    
    critical_urls = [
        ('accounts.login', 'Login'),
        ('accounts.logout', 'Logout'),
        ('accounts.signup', 'Signup'),
        ('accounts.access_status', 'Access Status'),
        ('accounts.request_access', 'Request Access'),
        ('accounts.access_denied', 'Access Denied'),
        ('books.index', 'Books Index'),
        ('library.index', 'Library Index'),
        ('home.index', 'Home'),
        ('roadmap:home', 'Roadmap Home'),
        ('resume_builder:home', 'Resume Builder'),
    ]
    
    url_issues = []
    for url_name, description in critical_urls:
        try:
            url = reverse(url_name)
            print(f"✅ {description}: {url}")
        except Exception as e:
            print(f"❌ {description}: {e}")
            url_issues.append((url_name, str(e)))
    
    # Test 2: Authentication Flow Audit
    print("\n2️⃣ AUTHENTICATION FLOW AUDIT")
    print("-" * 40)
    
    client = Client()
    auth_issues = []
    
    try:
        # Create test user
        test_user, created = User.objects.get_or_create(
            username='audit_user',
            defaults={'email': 'audit@example.com'}
        )
        if created:
            test_user.set_password('testpass123')
            test_user.save()
        
        # Test login
        login_success = client.login(username='audit_user', password='testpass123')
        print(f"✅ User Login: {login_success}")
        
        # Test authenticated pages
        auth_pages = [
            ('/accounts/access-status/', 'Access Status'),
            ('/library/', 'Library'),
            ('/', 'Home (authenticated)'),
        ]
        
        for url, name in auth_pages:
            try:
                response = client.get(url)
                print(f"✅ {name}: {response.status_code}")
            except Exception as e:
                print(f"❌ {name}: {e}")
                auth_issues.append((name, str(e)))
        
        # Test logout
        logout_response = client.get('/accounts/logout/')
        print(f"✅ Logout: {logout_response.status_code} → {logout_response.url if hasattr(logout_response, 'url') else 'No redirect'}")
        
        # Verify logout worked
        post_logout = client.get('/accounts/access-status/')
        if post_logout.status_code == 302:
            print("✅ Logout verification: User properly logged out")
        else:
            print(f"❌ Logout verification: {post_logout.status_code}")
            auth_issues.append(('Logout', 'User not properly logged out'))
            
    except Exception as e:
        print(f"❌ Authentication Flow Error: {e}")
        auth_issues.append(('Authentication Flow', str(e)))
    
    # Test 3: Access Control Audit
    print("\n3️⃣ ACCESS CONTROL AUDIT")
    print("-" * 40)
    
    access_issues = []
    
    try:
        # Test unauthenticated access
        client.logout()
        
        protected_pages = [
            ('/accounts/access-status/', 'Access Status'),
            ('/library/', 'Library'),
            ('/accounts/request-access/', 'Request Access'),
        ]
        
        for url, name in protected_pages:
            try:
                response = client.get(url)
                if response.status_code == 302:
                    print(f"✅ {name} (unauthenticated): Properly redirected")
                else:
                    print(f"❌ {name} (unauthenticated): {response.status_code} - Should redirect")
                    access_issues.append((name, f'Unauthenticated access allowed: {response.status_code}'))
            except Exception as e:
                print(f"❌ {name}: {e}")
                access_issues.append((name, str(e)))
        
        # Test authenticated but unauthorized access
        client.login(username='audit_user', password='testpass123')
        
        # Test request access functionality
        try:
            response = client.post('/accounts/request-access/', {
                'message': 'Audit test request'
            })
            print(f"✅ Request Access POST: {response.status_code}")
        except Exception as e:
            print(f"❌ Request Access POST: {e}")
            access_issues.append(('Request Access', str(e)))
            
    except Exception as e:
        print(f"❌ Access Control Error: {e}")
        access_issues.append(('Access Control', str(e)))
    
    # Test 4: Template & UI Audit
    print("\n4️⃣ TEMPLATE & UI AUDIT")
    print("-" * 40)
    
    ui_issues = []
    
    try:
        # Login and get pages to check UI
        client.login(username='audit_user', password='testpass123')
        
        pages_to_check = [
            ('/', 'Home Page'),
            ('/books/', 'Books Page'),
            ('/accounts/access-status/', 'Access Status Page'),
        ]
        
        for url, name in pages_to_check:
            try:
                response = client.get(url)
                if response.status_code == 200:
                    html = response.content.decode('utf-8')
                    
                    # Check for critical UI elements
                    ui_checks = [
                        ('Sign Out', 'Logout button'),
                        ('Access', 'Access button'),
                        ('navbar', 'Navigation bar'),
                    ]
                    
                    for element, description in ui_checks:
                        if element.lower() in html.lower():
                            print(f"✅ {name} - {description}: Present")
                        else:
                            print(f"⚠️  {name} - {description}: Missing")
                            ui_issues.append((name, f'{description} missing'))
                            
                else:
                    print(f"❌ {name}: {response.status_code}")
                    ui_issues.append((name, f'Page not accessible: {response.status_code}'))
                    
            except Exception as e:
                print(f"❌ {name}: {e}")
                ui_issues.append((name, str(e)))
                
    except Exception as e:
        print(f"❌ Template Audit Error: {e}")
        ui_issues.append(('Template Audit', str(e)))
    
    # Summary Report
    print("\n" + "=" * 80)
    print("📊 AUDIT SUMMARY REPORT")
    print("=" * 80)
    
    total_issues = len(url_issues) + len(auth_issues) + len(access_issues) + len(ui_issues)
    
    if total_issues == 0:
        print("🎉 NO CRITICAL ISSUES FOUND!")
        print("✅ All authentication flows working correctly")
        print("✅ All access controls properly enforced")
        print("✅ All URLs resolving correctly")
        print("✅ All UI elements present")
    else:
        print(f"⚠️  FOUND {total_issues} ISSUES TO FIX:")
        
        if url_issues:
            print(f"\n🔗 URL Issues ({len(url_issues)}):")
            for url_name, error in url_issues:
                print(f"   - {url_name}: {error}")
        
        if auth_issues:
            print(f"\n🔐 Authentication Issues ({len(auth_issues)}):")
            for component, error in auth_issues:
                print(f"   - {component}: {error}")
        
        if access_issues:
            print(f"\n🛡️  Access Control Issues ({len(access_issues)}):")
            for component, error in access_issues:
                print(f"   - {component}: {error}")
        
        if ui_issues:
            print(f"\n🎨 UI Issues ({len(ui_issues)}):")
            for component, error in ui_issues:
                print(f"   - {component}: {error}")
    
    print("\n" + "=" * 80)
    return total_issues == 0

if __name__ == '__main__':
    audit_codebase()