import os
import requests
import json
from flask import Flask, request, jsonify, send_from_directory
from dotenv import load_dotenv

# --- NEW DEBUGGING CODE ---
# Get the absolute path to the directory where this script is located
basedir = os.path.abspath(os.path.dirname(__file__))
# Construct the full path to the .env file
dotenv_path = os.path.join(basedir, '.env')

print(f"--- Debug Info ---")
print(f"Looking for .env file at: {dotenv_path}")

# Explicitly load the .env file from the constructed path
if os.path.exists(dotenv_path):
    print(".env file found! Loading variables.")
    load_dotenv(dotenv_path=dotenv_path)
else:
    print("Warning: .env file not found at the expected location.")

# Check for the API key after attempting to load
api_key_check = os.getenv("GEMINI_API_KEY")
if api_key_check:
    # Print only a part of the key for security
    print(f"Successfully loaded GEMINI_API_KEY, starting with: {api_key_check[:4]}...")
else:
    print("Error: GEMINI_API_KEY was not found after checking .env file.")
print("--- End Debug Info ---\n")
# --- END NEW DEBUGGING CODE ---


# Initialize the Flask application
app = Flask(__name__)

# --- Serve Frontend ---
@app.route('/')
def serve_index():
    """Serves the main index.html file from the parent directory."""
    # Corrected path to look one directory up ('..') from the current script location.
    return send_from_directory(os.path.join(basedir, '..'), 'index.html')

# --- LLM Integration ---

def generate_plan_with_llm(goal_text, prompt_template=None):
    """
    Calls the Gemini API with a specific prompt to break down a goal into a JSON plan.
    Accepts an optional prompt_template to override the default behavior.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        # This check should now be redundant but is kept as a safeguard.
        print("Error inside generate_plan_with_llm: GEMINI_API_KEY is not set.")
        return None

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"
    
    if not prompt_template:
        prompt_template = DEFAULT_PROMPT_TEMPLATE

    prompt = prompt_template.format(goal_text=goal_text)
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status()
        result_json_str = response.json()['candidates'][0]['content']['parts'][0]['text']
        plan = json.loads(result_json_str)
        return plan
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
        print(f"Response text from Google API: {http_err.response.text}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


# --- API Endpoint ---

@app.route('/generate-plan', methods=['POST'])
def generate_plan_endpoint():
    """
    API endpoint to generate a project plan.
    """
    data = request.get_json()
    goal = data.get('goal')
    prompt_template = data.get('prompt_template')

    if not goal:
        return jsonify({"error": "Missing 'goal' field"}), 400

    print(f"Received goal: {goal}")
    print("Generating plan with Gemini...")
    plan = generate_plan_with_llm(goal, prompt_template)

    if plan:
        print("Successfully generated plan.")
        return jsonify(plan)
    else:
        return jsonify({"error": "Failed to generate plan from LLM."}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True, port=5000)


