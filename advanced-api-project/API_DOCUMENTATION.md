# API Documentation - Filtering, Searching, and Ordering

## Book List Endpoint: `/api/books/`

### Filtering
Filter books using various criteria:

**By Publication Year:**
- Exact: `?publication_year=2020`
- Greater than: `?publication_year__gt=2000`
- Less than: `?publication_year__lt=2010`
- Range: `?publication_year__gte=2000&publication_year__lte=2010`

**By Title:**
- Contains: `?title=potter`
- Exact match: `?title__exact=Harry Potter`
- Starts with: `?title__startswith=The`

**By Author Name:**
- Contains: `?author__name=tolkien`
- Exact match: `?author__name__exact=J.K. Rowling`

### Searching
Full-text search across multiple fields:
- `?search=harry potter` (searches in title and author name)

### Ordering
Order results by any field:
- Single field: `?ordering=title`
- Descending: `?ordering=-publication_year`
- Multiple fields: `?ordering=author__name,-publication_year`

### Available Ordering Fields:
- `id`, `title`, `publication_year`, `author__name`

### Combining Features
You can combine filtering, searching, and ordering:
`?publication_year__gt=2000&search=fantasy&ordering=-publication_year,title`

## Examples

1. **Get fantasy books published after 2000, ordered by newest first:**

**GET /api/books/?publication_year__gt=2000&search=fantasy&ordering=-publication_year**


2. **Get books by specific author, ordered by title:**

**GET /api/books/?author__name=Rowling&ordering=title**


3. **Get books from a specific year range:**

**GET /api/books/?publication_year__gte=1990&publication_year__lte=2000**

