import os
import requests
import json
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv
from flask_cors import CORS

# Load environment variables from .env file for local development
load_dotenv()

# Initialize the Flask application
app = Flask(__name__)

# Enable CORS. This is necessary for local testing and doesn't harm the Vercel deployment.
CORS(app)

# --- LLM Integration ---
# (This section is unchanged)
DEFAULT_PROMPT_TEMPLATE = """
You are a world-class project manager AI. Your task is to break down a user's goal into a detailed project plan. Analyze the following goal and decompose it into a series of actionable tasks. For each task, provide a concise name, a brief description, a list of dependencies (using the `id` of other tasks), and an estimated timeline. The user's goal is: '{goal_text}'.

Important: Respond with ONLY a valid JSON array of objects. Do not include any explanatory text, markdown formatting, or code block syntax before or after the JSON. The structure for each task object in the array should be:
{{
  "id": <unique integer for the task, starting from 1>,
  "taskName": "<A short, clear name for the task>",
  "description": "<A one-sentence description of what needs to be done>",
  "dependencies": [<array of integer ids of tasks that must be completed first>],
  "timeline": "<A suggested duration or deadline, e.g., 'Day 1-2' or 'By Oct 15'>"
}}
"""

def generate_plan_with_llm(goal_text, prompt_template=None):
    """
    Calls the Gemini API with a specific prompt to break down a goal into a JSON plan.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set.")
        return None

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    
    prompt = (prompt_template or DEFAULT_PROMPT_TEMPLATE).format(goal_text=goal_text)
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        response_json = response.json()

        if 'candidates' in response_json and len(response_json['candidates']) > 0:
            raw_text = response_json['candidates'][0]['content']['parts'][0]['text']
            clean_json_str = raw_text.strip().lstrip('```json').rstrip('```').strip()
            plan = json.loads(clean_json_str)
            return plan
        else:
            print("API response did not contain any valid candidates.")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        return None
    except json.JSONDecodeError as json_err:
        print(f"Failed to decode JSON from API response: {json_err}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None

# --- API Endpoint (Works everywhere) ---
@app.route('/api/generate-plan', methods=['POST'])
def generate_plan_endpoint():
    """
    API endpoint to generate a project plan.
    """
    data = request.get_json()
    if not data or 'goal' not in data:
        return jsonify({"error": "Missing 'goal' in request body"}), 400

    plan = generate_plan_with_llm(data['goal'])

    if plan:
        return jsonify(plan)
    else:
        return jsonify({"error": "Failed to generate plan from LLM."}), 500


# --- Environment-Aware Routing ---
# This block adds the root route ONLY when running locally (not on Vercel).
# Vercel sets the 'VERCEL' environment variable, so we check for its absence.
if os.getenv('VERCEL') is None:
    @app.route('/')
    def serve_index():
        # Serves the index.html from the parent directory (project root)
        return send_from_directory('..', 'index.html')

# This allows running the app directly for local development
if __name__ == '__main__':
    app.run(debug=True, port=5000)