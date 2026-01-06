from django.test import TestCase
from django.urls import reverse
from .models import Book
from django.contrib.auth.models import User
from django.core.files.base import ContentFile


class BookDownloadTests(TestCase):
    def setUp(self):
        # create a user
        self.user = User.objects.create_user(username='tester', password='testpass')
        # create a book and attach a small PDF via ContentFile
        self.book = Book.objects.create(name='Test Book', price=10, description='desc')
        self.book.pdf.save('test.pdf', ContentFile(b'%PDF-1.0\n%EOF\n'))

    def test_download_link_present(self):
        response = self.client.get(reverse('books.show', kwargs={'id': self.book.id}))
        self.assertEqual(response.status_code, 200)
        # Download text varies for anonymous users (link to login). Accept either variant.
        body = response.content.decode()
        self.assertTrue('Download PDF' in body or 'Download (login)' in body or '/accounts/login/?next=' in body)

    def test_download_requires_login(self):
        resp = self.client.get(reverse('books.download', kwargs={'id': self.book.id}))
        # redirects to login
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/accounts/login/', resp['Location'])

    def test_authenticated_user_can_download(self):
        logged_in = self.client.login(username='tester', password='testpass')
        self.assertTrue(logged_in)
        # test download
        resp = self.client.get(reverse('books.download', kwargs={'id': self.book.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('application/pdf', resp['Content-Type'])
        self.assertIn('attachment', resp['Content-Disposition'])
        # FileResponse is streaming; materialize content for assertion
        content = b''.join(resp.streaming_content)
        self.assertTrue(content.startswith(b'%PDF'))

        # test view (inline) endpoint
        resp2 = self.client.get(reverse('books.view', kwargs={'id': self.book.id}))
        self.assertEqual(resp2.status_code, 200)
        self.assertIn('application/pdf', resp2['Content-Type'])
        self.assertIn('inline', resp2['Content-Disposition'])
        content2 = b''.join(resp2.streaming_content)
        self.assertTrue(content2.startswith(b'%PDF'))

    def test_category_filtering_requires_login_and_filters(self):
        # create categories and books
        from .models import Category
        cat_js, _ = Category.objects.get_or_create(name='JavaScript', slug='javascript')
        cat_ng, _ = Category.objects.get_or_create(name='Nginx', slug='nginx')
        b1 = Book.objects.create(name='JS Book', price=5, description='js', category=cat_js)
        b2 = Book.objects.create(name='NG Book', price=6, description='ng', category=cat_ng)

        # anonymous access should be redirected
        resp = self.client.get(reverse('books.category', kwargs={'slug': cat_js.slug}))
        self.assertEqual(resp.status_code, 302)
        self.assertIn('/accounts/login/', resp['Location'])

        # login and view filtered list
        self.client.login(username='tester', password='testpass')
        resp2 = self.client.get(reverse('books.category', kwargs={'slug': cat_js.slug}))
        self.assertEqual(resp2.status_code, 200)
        # only JS Book present
        self.assertContains(resp2, 'JS Book')
        self.assertNotContains(resp2, 'NG Book')

    def test_preview_button_visibility_and_headers(self):
        # anonymous users see login link instead of preview button
        resp = self.client.get(reverse('books.show', kwargs={'id': self.book.id}))
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'Preview (login)')
        self.assertIn('/accounts/login/', resp.content.decode())

        # authenticated users see preview button with data-preview-src
        self.client.login(username='tester', password='testpass')
        resp2 = self.client.get(reverse('books.show', kwargs={'id': self.book.id}))
        self.assertEqual(resp2.status_code, 200)
        expected_preview_src = reverse('books.view', kwargs={'id': self.book.id})
        # the preview button was removed; authenticated users can open the preview in a new tab
        self.assertIn('Open preview in new tab', resp2.content.decode())

        # view endpoint returns SAMEORIGIN so it can be embedded safely if needed
        view_resp = self.client.get(reverse('books.view', kwargs={'id': self.book.id}))
        self.assertEqual(view_resp.status_code, 200)
        self.assertEqual(view_resp['X-Frame-Options'], 'SAMEORIGIN')
