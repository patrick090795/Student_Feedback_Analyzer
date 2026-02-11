"""Flask frontend for Student Feedback Analyzer

Provides a minimal UI to paste/upload feedback, select subject (AI/OT), run analysis and view results.
"""

from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os
import pandas as pd
from analyzer import clean_text, sentiment_scores, generate_wordcloud, interpret_results, compute_correlations

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['WORDCLOUD_FOLDER'] = 'static/wordclouds'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['WORDCLOUD_FOLDER'], exist_ok=True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['POST'])
def analyze():
    # Accept either uploaded Excel or pasted comments
    subject = request.form.get('subject', 'AI')
    pasted = request.form.get('pasted_comments', '').strip()
    comments = []

    if 'file' in request.files and request.files['file'].filename:
        file = request.files['file']
        path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(path)
        try:
            df = pd.read_excel(path)
            # try auto-detect a free-text column: pick the first object dtype column
            text_cols = [c for c in df.columns if df[c].dtype == 'object']
            if text_cols:
                comments = df[text_cols[0]].fillna('').astype(str).tolist()
            else:
                comments = df.astype(str).stack().tolist()
        except Exception:
            comments = [pasted] if pasted else []
    else:
        if pasted:
            comments = [c for c in pasted.split('\n') if c.strip()]

    cleaned = [clean_text(c) for c in comments]
    polarities, summary = sentiment_scores(comments)
    wc_text = " ".join(cleaned)
    wc_path = os.path.join(app.config['WORDCLOUD_FOLDER'], f'wc_{subject}.png')
    generate_wordcloud(wc_text, output_path=wc_path)
    interpretations = interpret_results(polarities)

    # simple correlation attempt if the user supplied a ratings column name
    rating_col = request.form.get('rating_col')
    correlations = {}
    if rating_col and 'df' in locals():
        correlations = compute_correlations(df.assign(Sentiment=polarities), 'Sentiment', [rating_col])

    return render_template('results.html',
                           subject=subject,
                           summary=summary,
                           interpretations=interpretations,
                           wordcloud_url='/' + wc_path,
                           correlations=correlations)


if __name__ == '__main__':
    app.run(debug=True)
