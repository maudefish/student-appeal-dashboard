🚀 Getting Started
This tool visualizes student appeal data using an interactive Streamlit dashboard.

🧰 Requirements
Python 3.8–3.12 (recommended)

pip or venv for environment management

📦 Installation
bash
Copy
Edit
# 1. Clone the repository
git clone https://github.com/maudefish/student-appeal-dashboard.git
cd student-appeal-dashboard

# 2. (Optional) Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
# .venv\Scripts\activate    # On Windows

# 3. Install dependencies
pip install -r requirements.txt
🖥️ Running the App
bash
Copy
Edit
streamlit run app.py
Then open the link that appears (usually http://localhost:8501) in your browser.

📄 Input Format
Upload a .csv file with the following required columns:

text
Copy
Edit
First Name, Last Name, Grade Level,
I do not meet the grade prerequisite for,
Department Notes, Cum GPA, Fab 5 GPA,
Math PSAT9F, Math PSAT9S, Math PSAT10F,
Math PSAT10S, Math PSAT11F
Additional columns like and have registered for will be used if present.

