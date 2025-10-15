
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
# (The prompt is simplified as the schema now handles the strict output requirement)
DEFAULT_PROMPT_TEMPLATE = """
You are a world-class project manager AI. Your task is to break down a user's goal into a detailed project plan. Analyze the following goal and decompose it into a series of actionable tasks. For each task, provide a concise name, a brief description, a list of dependencies (using the 'id' of other tasks), and an estimated timeline. The user's goal is: '{goal_text}'.
"""

def generate_plan_with_llm(goal_text, prompt_template=None):
    """
    Calls the Gemini API with a specific prompt and JSON Mode to break down a goal into a JSON plan.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY is not set.")
        return None

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    
    prompt = (prompt_template or DEFAULT_PROMPT_TEMPLATE).format(goal_text=goal_text)
    
    # 1. Define the desired JSON structure for the model
    response_schema = {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "description": "Unique integer ID for the task, starting from 1"},
                "taskName": {"type": "string", "description": "A short, clear name for the task"},
                "description": {"type": "string", "description": "A one-sentence description of what needs to be done"},
                "dependencies": {"type": "array", "items": {"type": "integer"}, "description": "Array of integer IDs of tasks that must be completed first"},
                "timeline": {"type": "string", "description": "A suggested duration or deadline, e.g., 'Day 1-2' or 'By Oct 15'"}
            },
            "required": ["id", "taskName", "description", "dependencies", "timeline"]
        }
    }
    
    # 2. Configure the payload to use JSON Mode and the schema
    #    FIX: 'generationConfig' is the correct field name instead of 'config'
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": response_schema
        }
    }

    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        response_json = response.json()

        if 'candidates' in response_json and len(response_json['candidates']) > 0:
            # Parsing logic is simple as JSON Mode guarantees a clean JSON string
            json_text = response_json['candidates'][0]['content']['parts'][0]['text']
            plan = json.loads(json_text)
            return plan
        else:
            print("API response did not contain any valid candidates.")
            return None
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        # Print the response text for better debugging
        print(f"API Response Text: {response.text}")
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
        # The 500 status will correctly trigger the frontend error display
        return jsonify({"error": "Failed to generate plan from LLM. Check server logs for API errors or JSON parsing issues."}), 500


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
