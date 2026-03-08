from django.test import TestCase, Client
from django.urls import reverse


class BrowseViewTest(TestCase):
    def test_browse_returns_200(self):
        response = self.client.get(reverse('library:browse'))
        self.assertEqual(response.status_code, 200)


class SearchViewTest(TestCase):
    def test_search_returns_200(self):
        response = self.client.get(reverse('library:search'))
        self.assertEqual(response.status_code, 200)


class CategoriesViewTest(TestCase):
    def test_categories_returns_200(self):
        response = self.client.get(reverse('library:categories'))
        self.assertEqual(response.status_code, 200)


class AboutUsViewTest(TestCase):
    def test_about_us_returns_200(self):
        response = self.client.get(reverse('library:about_us'))
        self.assertEqual(response.status_code, 200)


class FAQViewTest(TestCase):
    def test_faq_returns_200(self):
        response = self.client.get(reverse('library:faq'))
        self.assertEqual(response.status_code, 200)


class ContactsViewTest(TestCase):
    def test_contacts_returns_200(self):
        response = self.client.get(reverse('library:contacts'))
        self.assertEqual(response.status_code, 200)


class LoginViewTest(TestCase):
    def test_login_returns_200(self):
        response = self.client.get(reverse('library:login'))
        self.assertEqual(response.status_code, 200)


class RegisterTabTest(TestCase):
    def test_register_tab_returns_200(self):
        response = self.client.get(reverse('library:login') + '?tab=register')
        self.assertEqual(response.status_code, 200)


class PrivacyPolicyViewTest(TestCase):
    def test_privacy_policy_returns_200(self):
        response = self.client.get(reverse('library:privacy_policy'))
        self.assertEqual(response.status_code, 200)


class TermsOfServiceViewTest(TestCase):
    def test_terms_of_service_returns_200(self):
        response = self.client.get(reverse('library:terms_of_service'))
        self.assertEqual(response.status_code, 200)


class ProfileViewTest(TestCase):
    def test_profile_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('library:profile'))
        self.assertEqual(response.status_code, 302)


class MyBooksViewTest(TestCase):
    def test_my_books_redirects_when_not_logged_in(self):
        response = self.client.get(reverse('library:my_books'))
        self.assertEqual(response.status_code, 302)
