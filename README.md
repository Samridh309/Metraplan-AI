# Metraplan-AI

Metraplan-AI is an intelligent, web-based task planner that leverages Python, Flask, Google's Gemini API, and a modern frontend stack (HTML & JavaScript). The project empowers users to efficiently organize, prioritize, and track their tasks using AI-powered insights, a friendly web interface, and robust API design.

---

## Features

- **AI-Powered Task Planning:** Uses the Gemini API to interpret and optimize user input for smarter scheduling and prioritization.
- **Intuitive Web Interface:** Built with Flask serving HTML and JavaScript, providing a responsive and user-friendly experience.
- **Natural Language Understanding:** Add tasks, set priorities, and ask questions in plain English.
- **Automated Suggestions:** Receive recommendations for deadlines, task grouping, and productivity tips.
- **RESTful API Design:** The backend exposes APIs for frontend consumption and potential third-party integration.
- **Customizable Workflows:** Adapt task planning to personal or team needs.

---

## Usability

Metraplan-AI streamlines your daily planning:

- **Add Tasks Easily:** Use natural language to add or modify tasks (e.g., "Remind me to submit the report by Friday").
- **Smart Prioritization:** The AI suggests which tasks to tackle first based on urgency, importance, and your working habits.
- **Visualize Your Plan:** Get a clear overview of upcoming tasks and deadlines in a web dashboard.
- **Interactive UI:** The frontend, built with HTML and JavaScript, allows dynamic task management, drag-and-drop, and real-time updates.
- **API Access:** Integrate or automate your workflow by interacting with the backend REST API.

---

## Screenshots

## Demo Video

[![Watch the Demo](https://github.com/Samridh309/Metraplan-AI/blob/main/LandingPage.jpg?raw=true)](https://drive.google.com/file/d/1bRXi_Se3xYPNKut8lFP95vKL8XSAuP9z/view?usp=sharing)
<br>
[Watch Demo Video](https://drive.google.com/file/d/1bRXi_Se3xYPNKut8lFP95vKL8XSAuP9z/view?usp=sharing)

---

**Site Screenshot**

![Site Screenshot](https://github.com/Samridh309/Metraplan-AI/blob/main/img.jpg?raw=true)


---

## Technology Stack

- **Python:** Core language for backend logic and AI integration.
- **Flask:** Lightweight web framework for serving the API endpoints and HTML frontend.
- **Gemini API:** Google's advanced AI API for natural language processing and smart planning features.
- **HTML & JavaScript:** For building a responsive, interactive, and modern web user interface.
- **REST API Design:** Clean, well-documented endpoints for all core functionalities, enabling both web and programmatic access.
- **Vercel:** Used for seamless deployment of the frontend for a fast and reliable user experience.

---

## API Design

The Flask backend exposes RESTful API endpoints for:

- Creating, reading, updating, and deleting tasks.
- Querying AI suggestions.
- Managing user sessions and preferences.
- All endpoints return JSON and are designed for easy frontend and third-party integration.

Refer to the in-repo API documentation or Flask code for details.

---

## Getting Started

### Prerequisites

- Python 3.8+
- pip (Python package manager)
- Google Gemini API key
- Node.js (optional, if building or extending frontend assets)

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Samridh309/Metraplan-AI.git
   cd Metraplan-AI
   ```

2. **Install backend dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your Gemini API key:**
   - Set your API key as an environment variable or update the configuration in the code.

4. **Run the Flask app:**
   ```bash
   flask run
   ```
   By default, the app will be available at `http://127.0.0.1:5000/`.

5. **(Optional) Build/Serve Frontend Assets:**
   - If using a custom build system for JavaScript assets, follow the instructions in the frontend directory (if provided).

6. **Deploy Frontend to Vercel:**
   - The frontend can be deployed on [Vercel](https://vercel.com/) for fast, global delivery. Simply connect your repository and follow the Vercel deployment guide for static or frontend assets.

---

## Usage

- Open the app in your browser.
- Add, edit, or remove tasks using the interactive web interface.
- Ask the planner questions or request suggestions (e.g., "What should I work on next?").
- Review AI-generated recommendations and optimize your workflow.
- Developers can use the REST API endpoints for integration or automation (see API docs in the repo, if available).

---

## Contributing

Contributions are welcome! Please open issues or submit pull requests for improvements, new features, or bug fixes.

---

## License

This project is licensed under the MIT License.

---

**Metraplan-AI**: Plan smarter, achieve more.
