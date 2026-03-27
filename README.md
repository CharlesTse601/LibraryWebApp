# LibraryWebApp
### developed by Charles Tse, Andrei Gogu, Karim Oudeh, Lucas McPike

## How to run
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python population_script.py
python api_population.py
python manage.py runserver
```
Then open `http://127.0.0.1:8000/` or https://team3ewad.pythonanywhere.com

## Completed Features

### Models
- [x] Define models — Category, Book, Searcher, BookList, BookListItem, Review, Vote
- [x] Run makemigrations and migrate after models are done
- [x] Register models in admin.py

### Views
> ChatGPT has been used for privacy_policy.html and terms_of_service.html to give ideas for the text to put inside there.
- [x] Implement browse view
- [x] Implement search view (with title, author, ISBN, date range, and category filters)
- [x] Implement categories view (with featured category logic)
- [x] Implement category_detail view
- [x] Implement book_detail view (with sort parameter support)
- [x] Implement recently_published view
- [x] Implement user_login — login + register tab at /login/
- [x] Implement register — combined into /login/?tab=register
- [x] Implement profile — at /login/myaccount/
- [x] Implement my_books — at /login/myaccount/mybooks/
- [x] Implement edit_profile
- [x] Implement contacts, about us, FAQ, privacy policy, terms of service pages

### Data & Integration
- [x] Populate database via Open Library API
- [x] Write population_script.py with sample data
- [x] Replace all placeholder text with real data from DB

### User Functionality
- [x] Add AJAX for add to list, mark as read, reviews
- [x] Review submission (login required)
- [x] Review voting — like/dislike with toggle and switching (login required)
- [x] Add book to wishlist / custom lists
- [x] Mark book as read / remove from read history
- [x] Create, view, and delete custom book lists
- [x] Profile stats — books read, review count, total upvotes received
- [x] Edit profile — username, email, password

### Styling
- [x] Add Bootstrap to all templates
- [x] Style navbar and footer
- [x] Style browse page — hero banner, category tiles, hot books grid
- [x] Style search page — filter panel and result cards
- [x] Style categories page — filter pills, featured banner, card grid
- [x] Style book detail page — cover, metadata box, reviews section
- [x] Style login/register page
- [x] Style profile page — stats bar, sidebar, book list

### Testing
> Unit tests were written with assistance from Claude (Anthropic's AI), which helped generate comprehensive test coverage across models and views.

- [x] Model tests — User, Category, Book, BookList, Review, Vote
- [x] View tests — all public views return correct status codes and templates
- [x] Search tests — title, author, ISBN, date range, and category filters
- [x] Auth tests — login success/failure, register (incl. duplicate username/email, password mismatch)
- [x] Redirect tests — profile, my_books, edit_profile redirect unauthenticated users to /login
- [x] Review tests — submit review, AJAX response, login required
- [x] Vote tests — like/dislike, toggle off, switch vote type, login required
- [x] Book list tests — mark as read, add to list, remove book, delete list, ownership enforcement
- [x] Profile tests — stats context (books_read, review_count, total_upvotes), edit profile fields
- [x] category_detail returns 404 for unknown category
- [x] book_detail returns 404 for unknown ISBN

## Remaining / Optional
- [ ] Make layout fully responsive (mobile/tablet/desktop)
- [ ] Add pagination where needed
- [x] Deploy on PythonAnywhere
