# Python microservice (Gemini bridge) for Jac 0.18 project.
# Flow: Frontend -> this proxy -> Gemini (if configured) -> call Jac walkers via subprocess to store/log -> return response to frontend.
#
# Requirements:
#   pip install flask requests python-dotenv
#
# Set environment variables:
#   GEMINI_API_KEY (your Gemini API key)
#   GEMINI_URL (optional, default will be used if unset)
#
from flask import Flask, request, jsonify
import subprocess, json, os, requests, time
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')  # set in .env or environment
GEMINI_URL = os.getenv('GEMINI_URL', '')  # optional custom endpoint

JAC_MAIN = 'jaseci/walkers/main.jac'  # path to jac walkers

def call_jac_walker(walker, payload, timeout=10):
    try:
        cmd = f"jac run {JAC_MAIN} --walker {walker}"
        proc = subprocess.run(cmd, input=json.dumps(payload), text=True, capture_output=True, shell=True, timeout=timeout)
        out = proc.stdout.strip() or proc.stderr.strip()
        try:
            return json.loads(out)
        except:
            return {'raw': out}
    except Exception as e:
        return {'error': str(e)}

def call_gemini(mood, note):
    # Simple Gemini call helper. Users must set GEMINI_API_KEY. This example uses a generic REST POST.
    if not GEMINI_API_KEY:
        return None
    # If a GEMINI_URL provided, use it; otherwise use a placeholder endpoint.
    url = GEMINI_URL or 'https://api.example-gemini.com/v1/generate'  # <-- replace with real Gemini endpoint
    prompt = f"""You are a calm empathetic assistant. Create a supportive message and 3 short affirmations in JSON:
    {{ "supportive": "...", "affirmations": ["a","b","c"] }}
    Mood: {mood}
    Note: {note}
    Return strictly valid JSON only."""
    headers = {'Authorization': f'Bearer {GEMINI_API_KEY}', 'Content-Type': 'application/json'}
    body = {'prompt': prompt, 'max_tokens': 300}
    try:
        resp = requests.post(url, headers=headers, json=body, timeout=15)
        if resp.status_code == 200:
            # Attempt to parse JSON from response directly or from 'text' field
            try:
                data = resp.json()
                # Heuristic: dig for a string reply
                if isinstance(data, dict) and 'text' in data:
                    return json.loads(data['text'])
                return data
            except Exception:
                text = resp.text
                try:
                    return json.loads(text)
                except:
                    return None
        else:
            return None
    except Exception as e:
        print('Gemini call failed:', e)
        return None

@app.route('/support', methods=['POST'])
def support():
    payload = request.get_json() or {}
    mood = payload.get('mood', 'okay')
    note = payload.get('note', '')

    # 1) Ask Jac to analyze the mood (Jac-side deterministic analysis)
    analysis = call_jac_walker('analyze_mood_walker', {'mood': mood, 'note': note})

    # 2) Call Gemini (if configured) to generate supportive text
    gem = call_gemini(mood, note)
    if gem is None:
        # fallback deterministic support
        fallback_map = {
            'happy': {'supportive':'Glad you are happy!','affirmations':['I deserve joy.','I celebrate small wins.','My happiness matters.']},
            'sad': {'supportive':'I am sorry you feel sad. You are not alone.','affirmations':['I allow myself to feel.','This feeling will pass.','I am worthy of care.']},
            'stressed': {'supportive':'Stress can be overwhelming — try a breathing exercise.','affirmations':['I can handle this.','One step at a time.','I am stronger than stress.']},
            'tired': {'supportive':'You sound tired — rest if you can.','affirmations':['Rest is productive.','My needs are valid.','I can rest and return refreshed.']},
            'okay': {'supportive':'You are doing okay — small steps matter.','affirmations':['I am on my way.','Small steps count.','I am present.']}
        }
        gen = fallback_map.get(mood, fallback_map['okay'])
    else:
        gen = gem

    # 3) Log the mood in Jac (calls log_mood walker)
    log_res = call_jac_walker('log_mood', payload)

    # 4) Store suggestion in Jac (so the graph contains the generated suggestion)
    store_res = call_jac_walker('store_suggestion_walker', {'text': gen.get('supportive') if isinstance(gen, dict) else str(gen)})

    # 5) Optionally call trend agent asynchronously (here we call it synchronously for demo)
    trend = call_jac_walker('trend_agent', {})

    response = {'analysis': analysis, 'support': gen, 'log': log_res, 'store': store_res, 'trend': trend}
    return jsonify(response)

if __name__ == '__main__':
    print('Starting proxy on http://127.0.0.1:3000 - ensure jac CLI is installed and GEMINI_API_KEY (optional) is set.')
    app.run(port=3000, debug=True)
