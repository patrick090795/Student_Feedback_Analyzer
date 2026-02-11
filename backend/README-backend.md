Backend (Django) quick start

1. Create and activate a virtualenv

2. Install backend dependencies:

```bash
python -m pip install -r requirements-backend.txt
```

3. Run migrations (creates sqlite db):

```bash
python manage.py migrate
```

4. Download NLTK resources (run once):

```bash
python - <<'PY'
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
PY
```

5. Start the development server:

```bash
python manage.py runserver
```

The API endpoint will be at http://127.0.0.1:8000/api/analyze/ and expects JSON POST:

{
  "subject": "AI",
  "comments": ["...", "..."]
}

It returns JSON with `summary`, `interpretations`, `polarities`, and `wordcloud_url`.
