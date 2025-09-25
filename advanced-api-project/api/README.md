### API Endpoints for Books

- `GET /books/` → List all books (public)
- `GET /books/<id>/` → Retrieve a single book (public)
- `POST /books/create/` → Create a new book (auth required)
- `PUT/PATCH /books/<id>/update/` → Update a book (auth required)
- `DELETE /books/<id>/delete/` → Delete a book (auth required)

### Permissions
- List & Detail → Open to all users
- Create, Update, Delete → Restricted to authenticated users
- Can extend with custom roles using DRF permissions
