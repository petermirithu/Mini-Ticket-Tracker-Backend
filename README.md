# Mini Ticket Tracker Backend

A Django REST Framework API backed by PostgreSQL for creating, listing, updating, and summarizing support tickets.

## Requirements

- Git
- Python 3.12+
- PostgreSQL 14+ with the `psql` command available

## Setup

Complete these steps in order.

### 1. Clone the repository

```bash
git clone https://github.com/petermirithu/Mini-Ticket-Tracker-Backend.git
cd Mini-Ticket-Tracker-Backend
```

### 2. Create and activate a Python environment

On macOS or Linux:

```bash
python3.12 -m venv virtual
source virtual/bin/activate
python -m pip install -r requirements.txt
```

On Windows PowerShell:

```powershell
py -3.12 -m venv virtual
.\virtual\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, allow local scripts for the current user and retry:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

On Windows Command Prompt:

```bat
py -3.12 -m venv virtual
virtual\Scripts\activate.bat
python -m pip install -r requirements.txt
```

### 3. Create the PostgreSQL database

Ensure PostgreSQL is running and `psql` is available in the terminal, then connect:

```bash
psql -U postgres
```

Run this SQL at the PostgreSQL prompt, then exit with `\q`:

```sql
CREATE DATABASE ticket_tracker;
```

### 4. Create the environment file

Create a `.env` file in the project root with values matching the local PostgreSQL installation:

```dotenv
DJANGO_SECRET_KEY="replace-with-a-secret-key"
DJANGO_DEBUG="true"
DJANGO_ALLOWED_HOSTS="127.0.0.1,localhost"
CORS_ALLOWED_ORIGINS="http://localhost:3000,http://localhost:5173"
POSTGRES_DB="ticket_tracker"
POSTGRES_USER="postgres"
POSTGRES_PASSWORD="replace-with-your-password"
POSTGRES_HOST="localhost"
POSTGRES_PORT="5432"
```

### 5. Run database migrations

With the virtual environment active:

```bash
python manage.py migrate
```

### 6. Start the backend

```bash
python manage.py runserver
```

The API is available at `http://127.0.0.1:8000`.

## Working with migrations

After changing a model, generate and apply a migration:

```bash
python manage.py makemigrations ticket_tracker
python manage.py migrate
```

Useful inspection commands:

```bash
python manage.py showmigrations
python manage.py sqlmigrate ticket_tracker 0001
```

Model changes should normally be made through migrations rather than by manually modifying PostgreSQL tables.

## Django administrator

Create an administrator account after applying the migrations:

```bash
python manage.py createsuperuser
```

Enter the requested username, email address, and password, ensure the server is running, then open `http://127.0.0.1:8000/admin/` to sign in. The `Ticket` model is available in Django Admin because it is registered in `ticket_tracker/admin.py`.

## API

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/tickets` | Create a ticket |
| `GET` | `/tickets?status=open&page=1&limit=10` | List, filter, and paginate tickets |
| `PATCH` | `/tickets/:id` | Update a ticket's status and/or priority |
| `GET` | `/tickets/stats` | Count tickets grouped by status |

Ticket status values are `open`, `in_progress`, and `closed`. Priority values are `low`, `medium`, and `high`.

### Create a ticket

```bash
curl -X POST http://127.0.0.1:8000/tickets \
  -H 'Content-Type: application/json' \
  -d '{"title":"Printer is offline","description":"Reception printer cannot connect","priority":"high"}'
```

### Update a ticket

```bash
curl -X PATCH http://127.0.0.1:8000/tickets/1 \
  -H 'Content-Type: application/json' \
  -d '{"status":"in_progress"}'
```

A paginated list response has this structure:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": []
}
```

The statistics endpoint includes every status, including statuses with no tickets:

```json
{
  "open": 2,
  "in_progress": 0,
  "closed": 1
}
```

## Tests

Run the test suite with:

```bash
python manage.py test
```

The configured PostgreSQL user must have permission to create the temporary test database used by Django.

## Decisions & Tradeoffs

Django REST Framework was selected because its generic views and model serializers provide consistent validation, JSON responses, and HTTP error handling with relatively little code. PostgreSQL is used in development and testing so database behaviour remains consistent across environments. Integer primary keys were kept because the application is small and does not require distributed ID generation. Ticket lists are ordered newest first and use page-number pagination capped at 100 records per page to prevent unbounded responses. A separate update serializer restricts PATCH requests to status and priority, trading flexibility for a smaller and safer update surface. The statistics endpoint explicitly includes zero-count statuses so clients always receive a predictable response shape. CORS is restricted to the configured frontend origins. Authentication, authorization, and user ownership of tickets were omitted because they are outside the current scope. With more time, the API would add authentication and permissions, title and description update support, OpenAPI documentation, structured logging, containerized deployment, and broader edge-case and PostgreSQL integration testing.
