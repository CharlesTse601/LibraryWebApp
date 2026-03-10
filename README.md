# LibraryWebApp
### developed by Charles Tse, Andrei Gog, Karim Oudeh, Lucas McPike

## How to run
```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```
Then open `http://127.0.0.1:8000/`

## TODO LIST
- [ ] Define models — Category, Book, Searcher, BookList, BookListItem, Review, Vote
- [ ] Run makemigrations and migrate after models are done
- [ ] Register models in admin.py
- [x] Implement browse view — skeleton in place
- [x] Implement search view — skeleton in place
- [x] Implement categories view — skeleton in place
- [x] Implement category_detail view — skeleton in place
- [x] Implement book_detail view — skeleton in place
- [x] Implement recently_published view — skeleton in place
- [x] Implement user_login — skeleton in place (login + register tab at /login/)
- [x] Implement register — combined into /login/?tab=register
- [x] Implement profile — skeleton in place at /login/myaccount/
- [x] Implement my_books — skeleton in place at /login/myaccount/mybooks/
- [ ] Implement contacts — handle form POST
- [ ] Add Bootstrap to all templates
- [ ] Style navbar and footer
- [ ] Style browse page — hero banner, category tiles, hot books grid
- [ ] Style search page — filter panel and result cards
- [ ] Style categories page — filter pills, featured banner, card grid
- [ ] Style book detail page — cover, metadata box, reviews section
- [ ] Style login/register page — split-screen layout
- [ ] Style profile page — stats bar, sidebar, book list
- [ ] Make layout responsive (mobile/tablet/desktop)
- [ ] Replace all placeholder text with real data from DB
- [ ] Add pagination where needed
- [ ] Add AJAX for add to list, mark as read, reviews, votes
- [ ] Write population_script.py with sample data
- [ ] Unit test — test all views return correct status codes
- [ ] Unit test — test login redirects authenticated users
- [ ] Unit test — test profile and my_books redirect when not logged in
- [ ] Unit test — test search returns results for valid query
- [ ] Unit test — test category_detail returns 404 for unknown slug
- [ ] Unit test — test book_detail returns 404 for unknown ISBN
- [ ] Unit test — test register creates a new user
- [ ] Unit test — test login authenticates a valid user
- [ ] Unit test — test review can be submitted by logged in user
- [ ] Unit test — test book can be added to wishlist
- [ ] Deploy on PythonAnywhere
