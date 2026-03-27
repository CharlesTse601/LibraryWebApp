import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Category, Book, BookList, Review, Vote

User = get_user_model()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def make_user(username='testuser', password='testpass123'):
    return User.objects.create_user(username=username, password=password, email=f'{username}@test.com')


def make_category(name='Fiction'):
    return Category.objects.get_or_create(category_name=name)[0]


def make_book(isbn='1234567890123', title='Test Book', author='Test Author', year=2020):
    return Book.objects.create(
        title=title, author=author, isbn=isbn,
        published_year=year, pages=300,
    )


# ===========================================================================
# Model Tests
# ===========================================================================

class UserModelTest(TestCase):
    def test_create_user_defaults(self):
        user = make_user()
        self.assertEqual(user.role, 'student')
        self.assertTrue(user.check_password('testpass123'))

    def test_str_returns_username(self):
        user = make_user('alice')
        self.assertEqual(str(user), 'alice')

    def test_admin_role(self):
        user = User.objects.create_user(username='admin1', password='pass', role='admin')
        self.assertEqual(user.role, 'admin')


class CategoryModelTest(TestCase):
    def test_str_returns_name(self):
        cat = make_category('Science')
        self.assertEqual(str(cat), 'Science')

    def test_category_name_unique(self):
        make_category('Unique')
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Category.objects.create(category_name='Unique')

    def test_default_views_zero(self):
        cat = make_category('History')
        self.assertEqual(cat.category_views, 0)


class BookModelTest(TestCase):
    def test_str_returns_title(self):
        book = make_book()
        self.assertEqual(str(book), 'Test Book')

    def test_isbn_unique(self):
        make_book(isbn='9999999999999')
        from django.db import IntegrityError
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                title='Duplicate', author='A', isbn='9999999999999',
                published_year=2020, pages=100,
            )

    def test_available_default_true(self):
        book = make_book()
        self.assertTrue(book.available)

    def test_category_many_to_many(self):
        book = make_book()
        cat = make_category('Tech')
        book.categories.add(cat)
        self.assertIn(cat, book.categories.all())


class BookListModelTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.book = make_book()

    def test_create_wishlist(self):
        bl = BookList.objects.create(user=self.user, list_name='My Wishlist', list_type='wishlist')
        self.assertEqual(bl.list_type, 'wishlist')

    def test_add_book_to_list(self):
        bl = BookList.objects.create(user=self.user, list_name='Read', list_type='read')
        bl.books.add(self.book)
        self.assertIn(self.book, bl.books.all())

    def test_list_belongs_to_user(self):
        bl = BookList.objects.create(user=self.user, list_name='Custom', list_type='custom')
        self.assertEqual(bl.user, self.user)


class ReviewModelTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.book = make_book()

    def test_create_review(self):
        r = Review.objects.create(book=self.book, user=self.user, star_rating=4, comment='Good book')
        self.assertEqual(r.star_rating, 4)
        self.assertEqual(r.comment, 'Good book')

    def test_review_linked_to_book_and_user(self):
        r = Review.objects.create(book=self.book, user=self.user, star_rating=3, comment='Ok')
        self.assertEqual(r.book, self.book)
        self.assertEqual(r.user, self.user)


class VoteModelTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.book = make_book()
        self.review = Review.objects.create(book=self.book, user=self.user, star_rating=5, comment='Great')

    def test_create_like(self):
        vote = Vote.objects.create(review=self.review, user=self.user, vote_type='like')
        self.assertEqual(vote.vote_type, 'like')

    def test_create_dislike(self):
        vote = Vote.objects.create(review=self.review, user=self.user, vote_type='dislike')
        self.assertEqual(vote.vote_type, 'dislike')


# ===========================================================================
# Public View Tests
# ===========================================================================

class BrowseViewTest(TestCase):
    def test_returns_200(self):
        response = self.client.get(reverse('library:browse'))
        self.assertEqual(response.status_code, 200)

    def test_uses_correct_template(self):
        response = self.client.get(reverse('library:browse'))
        self.assertTemplateUsed(response, 'library/browse.html')

    def test_context_contains_hot_books_and_categories(self):
        response = self.client.get(reverse('library:browse'))
        self.assertIn('hot_books', response.context)
        self.assertIn('top_categories', response.context)


class SearchViewTest(TestCase):
    def setUp(self):
        self.book = make_book(title='Django Basics', author='Jane Doe', isbn='1111111111111', year=2021)

    def test_returns_200(self):
        response = self.client.get(reverse('library:search'))
        self.assertEqual(response.status_code, 200)

    def test_search_by_title(self):
        response = self.client.get(reverse('library:search') + '?q=Django')
        self.assertIn(self.book, response.context['books'])

    def test_search_by_author(self):
        response = self.client.get(reverse('library:search') + '?q=Jane+Doe')
        self.assertIn(self.book, response.context['books'])

    def test_search_by_isbn(self):
        response = self.client.get(reverse('library:search') + '?q=1111111111111')
        self.assertIn(self.book, response.context['books'])

    def test_search_no_match_returns_empty(self):
        response = self.client.get(reverse('library:search') + '?q=ZZZNOMATCH')
        self.assertEqual(response.context['result_count'], 0)

    def test_date_filter_2020_plus(self):
        old_book = make_book(isbn='2222222222222', year=2005)
        response = self.client.get(reverse('library:search'), {'date': '2020+'})
        books = list(response.context['books'])
        self.assertIn(self.book, books)
        self.assertNotIn(old_book, books)

    def test_date_filter_before_2010(self):
        old_book = make_book(isbn='3333333333333', year=2000)
        response = self.client.get(reverse('library:search') + '?date=before2010')
        books = list(response.context['books'])
        self.assertIn(old_book, books)
        self.assertNotIn(self.book, books)

    def test_category_filter(self):
        cat = make_category('Science')
        self.book.categories.add(cat)
        other = make_book(isbn='4444444444444', title='History Book', year=2020)
        response = self.client.get(reverse('library:search') + '?category=Science')
        books = list(response.context['books'])
        self.assertIn(self.book, books)
        self.assertNotIn(other, books)


class CategoriesViewTest(TestCase):
    def test_returns_200(self):
        response = self.client.get(reverse('library:categories'))
        self.assertEqual(response.status_code, 200)

    def test_featured_is_category_with_most_books(self):
        cat1 = make_category('Big')
        cat2 = make_category('Small')
        for i in range(3):
            b = make_book(isbn=f'100000000000{i}')
            b.categories.add(cat1)
        b2 = make_book(isbn='9000000000001')
        b2.categories.add(cat2)
        response = self.client.get(reverse('library:categories'))
        self.assertEqual(response.context['featured'], cat1)


class CategoryDetailViewTest(TestCase):
    def setUp(self):
        self.cat = make_category('Mystery')
        self.book = make_book()
        self.book.categories.add(self.cat)

    def test_returns_200_for_valid_category(self):
        response = self.client.get(reverse('library:category_detail', args=['Mystery']))
        self.assertEqual(response.status_code, 200)

    def test_returns_404_for_invalid_category(self):
        response = self.client.get(reverse('library:category_detail', args=['DoesNotExist']))
        self.assertEqual(response.status_code, 404)

    def test_books_in_context(self):
        response = self.client.get(reverse('library:category_detail', args=['Mystery']))
        self.assertIn(self.book, response.context['books'])


class BookDetailViewTest(TestCase):
    def setUp(self):
        self.book = make_book()

    def test_returns_200_for_valid_isbn(self):
        response = self.client.get(reverse('library:book_detail', args=[self.book.isbn]))
        self.assertEqual(response.status_code, 200)

    def test_returns_404_for_invalid_isbn(self):
        response = self.client.get(reverse('library:book_detail', args=['0000000000000']))
        self.assertEqual(response.status_code, 404)

    def test_context_contains_reviews_and_avg_rating(self):
        response = self.client.get(reverse('library:book_detail', args=[self.book.isbn]))
        self.assertIn('reviews', response.context)
        self.assertIn('avg_rating', response.context)

    def test_sort_parameter_accepted(self):
        response = self.client.get(
            reverse('library:book_detail', args=[self.book.isbn]) + '?sort=rating_high'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['current_sort'], 'rating_high')


class RecentlyPublishedViewTest(TestCase):
    def test_returns_200(self):
        response = self.client.get(reverse('library:recently_published'))
        self.assertEqual(response.status_code, 200)

    def test_books_ordered_by_year_descending(self):
        make_book(isbn='5000000000001', year=2000)
        make_book(isbn='5000000000002', year=2023)
        response = self.client.get(reverse('library:recently_published'))
        years = [b.published_year for b in response.context['books']]
        self.assertEqual(years, sorted(years, reverse=True))


class StaticPageViewTests(TestCase):
    def test_about_us(self):
        self.assertEqual(self.client.get(reverse('library:about_us')).status_code, 200)

    def test_faq(self):
        self.assertEqual(self.client.get(reverse('library:faq')).status_code, 200)

    def test_contacts(self):
        self.assertEqual(self.client.get(reverse('library:contacts')).status_code, 200)

    def test_privacy_policy(self):
        self.assertEqual(self.client.get(reverse('library:privacy_policy')).status_code, 200)

    def test_terms_of_service(self):
        self.assertEqual(self.client.get(reverse('library:terms_of_service')).status_code, 200)


# ===========================================================================
# Authentication View Tests
# ===========================================================================

class LoginViewTest(TestCase):
    def setUp(self):
        self.user = make_user('loginuser', 'mypassword')

    def test_get_login_page(self):
        response = self.client.get(reverse('library:login'))
        self.assertEqual(response.status_code, 200)

    def test_login_success_redirects_to_browse(self):
        response = self.client.post(reverse('library:login'), {
            'form_type': 'login',
            'username': 'loginuser',
            'password': 'mypassword',
        })
        self.assertRedirects(response, reverse('library:browse'))

    def test_login_invalid_credentials_stays_on_login(self):
        response = self.client.post(reverse('library:login'), {
            'form_type': 'login',
            'username': 'loginuser',
            'password': 'wrongpassword',
        })
        self.assertEqual(response.status_code, 302)
        self.assertIn('login', response['Location'])

    def test_register_success_redirects_to_browse(self):
        response = self.client.post(reverse('library:login'), {
            'form_type': 'register',
            'username': 'newuser',
            'email': 'new@test.com',
            'password1': 'securepass',
            'password2': 'securepass',
            'role': 'student',
        })
        self.assertRedirects(response, reverse('library:browse'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_password_mismatch(self):
        response = self.client.post(reverse('library:login'), {
            'form_type': 'register',
            'username': 'baduser',
            'email': 'bad@test.com',
            'password1': 'pass1',
            'password2': 'pass2',
        })
        self.assertFalse(User.objects.filter(username='baduser').exists())

    def test_register_duplicate_username(self):
        response = self.client.post(reverse('library:login'), {
            'form_type': 'register',
            'username': 'loginuser',  # already exists
            'email': 'other@test.com',
            'password1': 'pass',
            'password2': 'pass',
        })
        # User count should not increase
        self.assertEqual(User.objects.filter(username='loginuser').count(), 1)

    def test_register_duplicate_email(self):
        response = self.client.post(reverse('library:login'), {
            'form_type': 'register',
            'username': 'anotheruser',
            'email': 'loginuser@test.com',  # already registered
            'password1': 'pass',
            'password2': 'pass',
        })
        self.assertFalse(User.objects.filter(username='anotheruser').exists())


class LogoutViewTest(TestCase):
    def test_logout_redirects_to_browse(self):
        make_user('logoutuser', 'pass')
        self.client.login(username='logoutuser', password='pass')
        response = self.client.get(reverse('library:logout'))
        self.assertRedirects(response, reverse('library:browse'))


# ===========================================================================
# Auth-Required View Tests (redirect when not logged in)
# ===========================================================================

class AuthRequiredViewsTest(TestCase):
    def _assert_redirects_to_login(self, url):
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response['Location'])

    def test_profile_requires_login(self):
        self._assert_redirects_to_login(reverse('library:profile'))

    def test_my_books_requires_login(self):
        self._assert_redirects_to_login(reverse('library:my_books'))

    def test_edit_profile_requires_login(self):
        self._assert_redirects_to_login(reverse('library:edit_profile'))


# ===========================================================================
# Review & Voting View Tests
# ===========================================================================

class AddReviewViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.book = make_book()
        self.client.login(username='testuser', password='testpass123')
        self.url = reverse('library:add_review', args=[self.book.isbn])

    def test_add_review_creates_review(self):
        self.client.post(self.url, {'star_rating': 4, 'comment': 'Really good!'})
        self.assertEqual(Review.objects.filter(book=self.book, user=self.user).count(), 1)

    def test_add_review_stores_correct_data(self):
        self.client.post(self.url, {'star_rating': 5, 'comment': 'Excellent'})
        review = Review.objects.get(book=self.book, user=self.user)
        self.assertEqual(review.star_rating, 5)
        self.assertEqual(review.comment, 'Excellent')

    def test_add_review_ajax_returns_json(self):
        response = self.client.post(
            self.url,
            {'star_rating': 3, 'comment': 'Ok'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_add_review_requires_login(self):
        self.client.logout()
        response = self.client.post(self.url, {'star_rating': 4, 'comment': 'Hi'})
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response['Location'])


class VoteReviewViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.other = make_user('other', 'otherpass')
        self.book = make_book()
        self.review = Review.objects.create(book=self.book, user=self.other, star_rating=4, comment='Nice')
        self.client.login(username='testuser', password='testpass123')
        self.url = reverse('library:vote_review', args=[self.review.id])

    def _ajax_post(self, vote_type):
        return self.client.post(
            self.url,
            {'vote_type': vote_type},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )

    def test_like_creates_vote(self):
        self._ajax_post('like')
        self.assertEqual(Vote.objects.filter(review=self.review, vote_type='like').count(), 1)

    def test_ajax_returns_counts(self):
        response = self._ajax_post('like')
        data = json.loads(response.content)
        self.assertIn('likes', data)
        self.assertIn('dislikes', data)
        self.assertEqual(data['likes'], 1)

    def test_voting_same_type_twice_toggles_off(self):
        self._ajax_post('like')
        self._ajax_post('like')
        self.assertEqual(Vote.objects.filter(review=self.review, user=self.user).count(), 0)

    def test_switching_vote_type(self):
        self._ajax_post('like')
        response = self._ajax_post('dislike')
        data = json.loads(response.content)
        self.assertEqual(data['likes'], 0)
        self.assertEqual(data['dislikes'], 1)
        self.assertEqual(Vote.objects.filter(review=self.review, user=self.user).count(), 1)

    def test_vote_requires_login(self):
        self.client.logout()
        response = self._ajax_post('like')
        self.assertEqual(response.status_code, 302)


# ===========================================================================
# Book List View Tests
# ===========================================================================

class MarkAsReadViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.book = make_book()
        self.client.login(username='testuser', password='testpass123')
        self.url = reverse('library:mark_as_read', args=[self.book.isbn])

    def test_creates_read_list_if_not_exists(self):
        self.client.post(self.url, HTTP_REFERER='http://testserver/browse/')
        self.assertTrue(BookList.objects.filter(user=self.user, list_type='read').exists())

    def test_adds_book_to_read_list(self):
        self.client.post(self.url, HTTP_REFERER='http://testserver/browse/')
        read_list = BookList.objects.get(user=self.user, list_type='read')
        self.assertIn(self.book, read_list.books.all())

    def test_ajax_returns_success(self):
        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_mark_as_read_requires_login(self):
        self.client.logout()
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)


class RemoveFromReadHistoryTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.book = make_book()
        self.client.login(username='testuser', password='testpass123')
        self.read_list = BookList.objects.create(user=self.user, list_name='Read History', list_type='read')
        self.read_list.books.add(self.book)

    def test_removes_book_from_read_list(self):
        self.client.post(reverse('library:remove_from_read_history', args=[self.book.isbn]))
        self.assertNotIn(self.book, self.read_list.books.all())

    def test_redirects_to_profile(self):
        response = self.client.post(reverse('library:remove_from_read_history', args=[self.book.isbn]))
        self.assertRedirects(response, reverse('library:profile'))


class CreateNewListViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.login(username='testuser', password='testpass123')

    def test_creates_custom_list(self):
        self.client.post(reverse('library:create_new_list'), {'list_name': 'My List'})
        self.assertTrue(BookList.objects.filter(user=self.user, list_name='My List', list_type='custom').exists())

    def test_empty_name_does_not_create(self):
        self.client.post(reverse('library:create_new_list'), {'list_name': ''})
        self.assertEqual(BookList.objects.filter(user=self.user, list_type='custom').count(), 0)


class CreateListWithBookViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.book = make_book()
        self.client.login(username='testuser', password='testpass123')

    def test_creates_list_and_adds_book(self):
        self.client.post(
            reverse('library:create_list_with_book', args=[self.book.isbn]),
            {'list_name': 'Favourites'},
        )
        bl = BookList.objects.filter(user=self.user, list_name='Favourites').first()
        self.assertIsNotNone(bl)
        self.assertIn(self.book, bl.books.all())


class AddToListViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.book = make_book()
        self.client.login(username='testuser', password='testpass123')
        self.book_list = BookList.objects.create(user=self.user, list_name='Custom', list_type='custom')
        self.url = reverse('library:add_to_list', args=[self.book_list.id, self.book.isbn])

    def test_adds_book_to_list(self):
        self.client.post(self.url, HTTP_REFERER='http://testserver/browse/')
        self.assertIn(self.book, self.book_list.books.all())

    def test_ajax_returns_success(self):
        response = self.client.post(self.url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(response.content)
        self.assertTrue(data['success'])

    def test_cannot_add_to_another_users_list(self):
        other = make_user('other', 'otherpass')
        other_list = BookList.objects.create(user=other, list_name='Other', list_type='custom')
        response = self.client.post(reverse('library:add_to_list', args=[other_list.id, self.book.isbn]))
        self.assertEqual(response.status_code, 404)


class RemoveBookFromListViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.book = make_book()
        self.client.login(username='testuser', password='testpass123')
        self.book_list = BookList.objects.create(user=self.user, list_name='Custom', list_type='custom')
        self.book_list.books.add(self.book)

    def test_removes_book_from_list(self):
        self.client.post(reverse('library:remove_book_from_list', args=[self.book_list.id, self.book.isbn]))
        self.assertNotIn(self.book, self.book_list.books.all())


class RemoveListViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.login(username='testuser', password='testpass123')
        self.book_list = BookList.objects.create(user=self.user, list_name='ToDelete', list_type='custom')

    def test_deletes_list(self):
        self.client.post(reverse('library:remove_list', args=[self.book_list.id]))
        self.assertFalse(BookList.objects.filter(id=self.book_list.id).exists())

    def test_cannot_delete_another_users_list(self):
        other = make_user('other', 'otherpass')
        other_list = BookList.objects.create(user=other, list_name='Other', list_type='custom')
        self.client.post(reverse('library:remove_list', args=[other_list.id]))
        self.assertTrue(BookList.objects.filter(id=other_list.id).exists())


# ===========================================================================
# Profile View Tests
# ===========================================================================

class ProfileViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.login(username='testuser', password='testpass123')

    def test_returns_200_when_logged_in(self):
        response = self.client.get(reverse('library:profile'))
        self.assertEqual(response.status_code, 200)

    def test_stats_in_context(self):
        response = self.client.get(reverse('library:profile'))
        self.assertIn('books_read', response.context)
        self.assertIn('review_count', response.context)
        self.assertIn('total_upvotes', response.context)

    def test_books_read_count_reflects_read_list(self):
        book = make_book()
        read_list = BookList.objects.create(user=self.user, list_name='Read History', list_type='read')
        read_list.books.add(book)
        response = self.client.get(reverse('library:profile'))
        self.assertEqual(response.context['books_read'], 1)

    def test_review_count_reflects_user_reviews(self):
        book = make_book()
        Review.objects.create(book=book, user=self.user, star_rating=5, comment='Great')
        response = self.client.get(reverse('library:profile'))
        self.assertEqual(response.context['review_count'], 1)

    def test_upvote_count_reflects_votes_on_user_reviews(self):
        other = make_user('voter', 'voterpass')
        book = make_book()
        review = Review.objects.create(book=book, user=self.user, star_rating=4, comment='Good')
        Vote.objects.create(review=review, user=other, vote_type='like')
        response = self.client.get(reverse('library:profile'))
        self.assertEqual(response.context['total_upvotes'], 1)


class EditProfileViewTest(TestCase):
    def setUp(self):
        self.user = make_user('editme', 'oldpassword')
        self.client.login(username='editme', password='oldpassword')

    def test_get_edit_page(self):
        response = self.client.get(reverse('library:edit_profile'))
        self.assertEqual(response.status_code, 200)

    def test_change_username(self):
        self.client.post(reverse('library:edit_profile'), {'username': 'newname', 'email': ''})
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'newname')

    def test_change_email(self):
        self.client.post(reverse('library:edit_profile'), {'username': '', 'email': 'new@example.com'})
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, 'new@example.com')

    def test_password_mismatch_does_not_change_password(self):
        response = self.client.post(reverse('library:edit_profile'), {
            'username': '', 'email': '',
            'password1': 'newpass', 'password2': 'different',
        })
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('oldpassword'))


class MyBooksViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.login(username='testuser', password='testpass123')

    def test_returns_200(self):
        response = self.client.get(reverse('library:my_books'))
        self.assertEqual(response.status_code, 200)

    def test_context_contains_lists(self):
        response = self.client.get(reverse('library:my_books'))
        self.assertIn('lists', response.context)


class ListDetailViewTest(TestCase):
    def setUp(self):
        self.user = make_user()
        self.client.login(username='testuser', password='testpass123')
        self.book_list = BookList.objects.create(user=self.user, list_name='My Custom', list_type='custom')

    def test_returns_200_for_own_list(self):
        response = self.client.get(reverse('library:list_detail', args=[self.book_list.id]))
        self.assertEqual(response.status_code, 200)

    def test_returns_404_for_other_users_list(self):
        other = make_user('other', 'otherpass')
        other_list = BookList.objects.create(user=other, list_name='Private', list_type='custom')
        response = self.client.get(reverse('library:list_detail', args=[other_list.id]))
        self.assertEqual(response.status_code, 404)
