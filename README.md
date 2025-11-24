🧠 AI Interview Preparation Tool

  Welcome to the AI Interview Preparation Tool — your personal AI-powered assistant for preparing for technical interviews.
  This tool generates context-aware, scenario-based, and role-specific interview questions to help candidates practice confidently.

🚀 Features
  ✔ Role-based Question Generation
  
  SDE / Python / DevOps / MLOps / Cloud / Data Engineer
  
  Behavioral + Technical + System Design
  
  ✔ Real-time AI Responses
  
  Auto-generated questions & answers
  
  Scenario-based answers
  
  Customizable depth
  
  ✔ Upload Resume to Personalize Questions
  ✔ Streamlit UI (clean & responsive)
  ✔ Modular Code Structure
  
  models/ – AI models
  
  config/ – prompt templates
  
  utils/ – helpers
  
  data/ – examples & assets

🗂️ Project Structure
  AI_UseCase/
  │
  ├── app.py                 # Streamlit UI
  ├── config/                # Prompt templates
  ├── models/                # LLM wrapper / model configs
  ├── utils/                 # Helper functions
  ├── data/                  # Example inputs
  │
  ├── requirements.txt
  └── README.md

⚙️ Installation & Setup
  1️⃣ Clone the repository
  git clone https://github.com/akp2301/ai-interview-preparation-tool.git
  cd ai-interview-preparation-tool/AI_UseCase
  
  2️⃣ Create virtual environment
  python3 -m venv venv
  source venv/bin/activate
  
  3️⃣ Install dependencies
  pip install -r requirements.txt
  
  ▶️ Run Locally
  streamlit run app.py
  
  🌐 Deployment: Streamlit Cloud
  
  Push your code to GitHub
  
  Go to share.streamlit.io
  
  Select this GitHub repo
  
  Set entry point:
  
  AI_UseCase/app.py
  
  
  Add secrets if needed (like API keys)
  
  Deploy 🎉

📦 Requirements

  This project uses:
  
  Python 3.10+
  
  Streamlit
  
  LangChain / OpenAI / Huggingface models
  
  dotenv
  
  Pydantic
  
  📘 How It Works
  
  User selects a role
  
  User adds custom context (e.g., "I am interviewing for SDE1")
  
  LLM generates tailored interview questions
  
  Follow-up questions and explanations are produced in real-time
  
  Optionally, the tool analyzes your resume to personalize questions

🌱 Future Enhancements

  Add voice-based Q&A
  
  Add coding interview generator
  
  Store user progress
  
  Export interview sets to PDF
  
  Add MCQ quiz mode

🤝 Contributing

  Pull requests are welcome!
  If you’d like to add new templates or features, feel free to fork and submit PRs.

📄 License

MIT License.
