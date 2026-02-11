# Student_Feedback_Analyzer
 To analyze feedback from students to their respective faculties using machine learning, you can approach the problem as a text classification task.
 Specifically, you can train a machine learning model to classify the feedback as positive, negative, or neutral.

This project analyzes student feedback and computes sentiment polarity, generates wordclouds, and computes simple correlations between sentiment and numeric ratings.

Originally this was implemented as a Colab notebook. The repository now includes a small Flask demo UI and a refactored analyzer module to make the workflow reusable.

Demo/Files added
- `analyzer.py` — core reusable functions (cleaning, sentiment, wordcloud, interpretation).
- `app.py` — minimal Flask app with upload/paste UI.
- `templates/` and `static/` — frontend templates and CSS.
- `requirements.txt` — Python dependencies.

Quick start

1. Create and activate a virtual environment (recommended).

2. Install dependencies:

```bash
python -m pip install -r requirements.txt
```

3. Download required NLTK resources (run once):

```bash
python - <<'PY'
import nltk
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
PY
```

4. Run the Flask app:

```bash
python app.py
```

Open http://127.0.0.1:5000/ in your browser. You can upload an Excel feedback file or paste comments (one per line), select a subject, and run analysis.

Notes and next steps
- The demo uses TextBlob for sentiment; consider VADER or transformer models for better accuracy.
- If you'd like, I can:
	## Student Feedback Analyzer

	A lightweight system to analyze student feedback. It provides:

	- Text cleaning and simple sentiment scoring (TextBlob)
	- Wordcloud generation for quick topic visualization
	- Simple correlations between computed sentiment and numeric ratings

	This repository contains two working stacks to explore the analysis:

	- A Django backend (API) that exposes an `/api/analyze/` endpoint using the refactored `analyzer.py` module.
	- A React frontend (dev server) that sends comments to the backend and displays results (summary, interpretations and wordcloud).

	Project layout (important files)

	- `analyzer.py` — core processing functions (clean_text, sentiment_scores, compute_correlations, generate_wordcloud, interpret_results).
	- `backend/` — Django project and `api` app providing the analyze API.
	- `backend/requirements-backend.txt` — Python packages for the backend.
	- `frontend/` — React app (development UI).

	Requirements

	- Python 3.8+ and a virtual environment for the backend
	- Node.js and npm for the frontend
	- System packages for some Python wheels (on Debian/Ubuntu: `build-essential python3-dev libfreetype6-dev libpng-dev`)

	Quick local setup (recommended)

	1) Create and activate a Python virtual environment (optional but recommended):

	```bash
	python -m venv .venv
	source .venv/bin/activate
	```

	2) Install backend dependencies and run migrations:

	```bash
	cd backend
	python -m pip install -r requirements-backend.txt
	python manage.py migrate
	```

	3) Download NLTK resources (run once):

	```bash
	python - <<'PY'
	import nltk
	nltk.download('punkt')
	nltk.download('punkt_tab')
	nltk.download('wordnet')
	nltk.download('stopwords')
	PY
	```

	4) Start the Django backend (development):

	```bash
	python manage.py runserver
	```

	The analyze API will be available at: http://127.0.0.1:8000/api/analyze/

	API usage example (curl):

	```bash
	curl -X POST http://127.0.0.1:8000/api/analyze/ \
		-H "Content-Type: application/json" \
		-d '{"subject":"AI","comments":["Great lecture","Too fast"]}'
	```

	5) Frontend (React) setup and run (separate terminal):

	```bash
	cd frontend
	npm install
	npm start
	```

	Open http://localhost:3000. The React UI posts comments to the Django backend and displays the returned summary and generated wordcloud (ensure the backend is running).

	Notes about connectivity and CORS

	- The backend includes `django-cors-headers` and is configured to allow requests from the frontend dev server during development. If you change ports, update CORS settings or the frontend API base URL in `frontend/src/App.js`.
	- Browsers send an OPTIONS preflight request before POST; the backend handles OPTIONS and POST.

	Troubleshooting

	- 500 errors mentioning NLTK LookupError (e.g. `punkt_tab` not found): run the NLTK downloads shown above. The backend also tries to download missing NLTK resources on import, but running the explicit download is more reliable.
	- `ModuleNotFoundError` for packages (numpy, pandas, etc.): ensure you installed backend dependencies inside the same virtualenv that runs Django:
		```bash
		which python
		python -m pip install -r backend/requirements-backend.txt
		```
	- `wordcloud` build failures: on Debian/Ubuntu install system libs first:
		```bash
		sudo apt-get install -y build-essential python3-dev libfreetype6-dev libpng-dev
		```
	- React dev server shows `index.html not found`: ensure `frontend/public/index.html` exists (the scaffold includes one).

	What the API returns

	The `/api/analyze/` endpoint returns JSON:

	```json
	{
		"summary": {"mean": ..., "positive_pct": ...},
		"interpretations": [...],
		"polarities": [0.1, -0.2, ...],
		"wordcloud_url": "/media/wc_AI.png"
	}
	```

	

	
