import os
import requests
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables for local testing.
# On Vercel, these will be set in the project settings.
load_dotenv()

# Initialize the FastAPI application
app = FastAPI()

# This Pydantic model ensures that any request to our endpoint
# MUST have a 'goal' field that is a string. This provides automatic data validation.
class GoalRequest(BaseModel):
    goal: str

# This is the prompt that instructs the AI on how to behave and what to return.
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

def generate_plan_with_llm(goal_text: str):
    """
    Contacts the Gemini API to generate a project plan.
    """
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: GEMINI_API_KEY not found in environment.")
        raise HTTPException(status_code=500, detail="Server configuration error: Missing API key.")

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={api_key}"

    prompt = DEFAULT_PROMPT_TEMPLATE.format(goal_text=goal_text)
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {'Content-Type': 'application/json'}

    result_json_str = ""
    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=60)
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
        result_json_str = response.json()['candidates'][0]['content']['parts'][0]['text']

        # Robustly clean the JSON response to remove markdown wrappers
        if result_json_str.strip().startswith("```json"):
            result_json_str = result_json_str.strip()[7:-3].strip()

        plan = json.loads(result_json_str)
        return plan
    except requests.exceptions.RequestException as e:
        print(f"ERROR: Request to Gemini API failed: {e}")
        raise HTTPException(status_code=502, detail="Failed to communicate with the AI service.")
    except (json.JSONDecodeError, KeyError, IndexError) as e:
        print(f"ERROR: Failed to decode or parse JSON from Gemini API response: {e}")
        print(f"--- Raw response from AI ---\n{result_json_str}\n--------------------")
        raise HTTPException(status_code=500, detail="Invalid response format from the AI service.")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An unexpected server error occurred.")

# This is the API endpoint. It listens for POST requests at /api/generate-plan.
@app.post("/api/generate-plan")
async def generate_plan_endpoint(request: GoalRequest):
    # FastAPI automatically validates the incoming request using the GoalRequest model.
    # If the 'goal' field is missing or not a string, it will return a 422 error.
    plan = generate_plan_with_llm(request.goal)
    return plan