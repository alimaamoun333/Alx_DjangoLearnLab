# 📚 LibraryProject

A Django-based library management application with custom user authentication and book management.

---

## 🚀 Features
- **Custom User Model**
  - Extends Django’s `AbstractUser`
  - Extra fields: `date_of_birth`, `profile_photo`
  - Custom manager (`CustomUserManager`) with `create_user` and `create_superuser`
  - Custom permissions: `can_create`, `can_delete`

- **Book Management**
  - `Book` model with `title`, `author`, `publication_year`
  - Admin panel with search, filters, and custom actions
  - Book list view (`book_list`) with permission checks

- **Permissions**
  - `can_create`: Required to view the book list
  - `can_delete`: For deleting books (future feature)

---

## 🛠️ Tech Stack
- Python 3.12+
- Django 5.2+
- SQLite (default, can be swapped with MySQL/PostgreSQL)
- Bootstrap/Tailwind (optional for frontend styling)

---

## ⚙️ Installation

1. **Clone the repo**
   ```bash
   git clone https://github.com/your-username/LibraryProject.git
   cd LibraryProject
