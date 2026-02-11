import os
import sys
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

# Ensure the repository root is on sys.path so we can import analyzer.py from the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from analyzer import clean_text, sentiment_scores, generate_wordcloud, interpret_results

import json

@csrf_exempt
def analyze_view(request):
    """Accepts JSON: {"comments": [".."], "subject": "AI"}
    Returns: JSON with summary, interpretations, polarities and wordcloud_url
    """
    # Handle preflight CORS OPTIONS
    if request.method == 'OPTIONS':
        res = HttpResponse()
        res['Access-Control-Allow-Origin'] = '*'
        res['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
        res['Access-Control-Allow-Headers'] = 'Content-Type'
        return res

    try:
        payload = json.loads(request.body.decode('utf-8'))
    except Exception:
        res = JsonResponse({'error': 'invalid json'}, status=400)
        res['Access-Control-Allow-Origin'] = '*'
        return res

    comments = payload.get('comments', [])
    subject = payload.get('subject', 'AI')

    # limit size to avoid abuse
    if not isinstance(comments, list) or len(comments) > 5000:
        return JsonResponse({'error': 'comments must be a list of <= 5000 items'}, status=400)

    cleaned = [clean_text(c) for c in comments]
    polarities, summary = sentiment_scores(comments)
    wc_text = ' '.join(cleaned)
    os.makedirs(settings.MEDIA_ROOT, exist_ok=True)
    wc_filename = f'wc_{subject}.png'
    wc_path = os.path.join(settings.MEDIA_ROOT, wc_filename)
    generate_wordcloud(wc_text, output_path=wc_path)
    interpretations = interpret_results(polarities)

    resp = JsonResponse({
        'summary': summary,
        'interpretations': interpretations,
        'polarities': polarities,
        'wordcloud_url': settings.MEDIA_URL + wc_filename,
    })
    # allow cross-origin requests from the frontend dev server
    resp['Access-Control-Allow-Origin'] = '*'
    return resp
