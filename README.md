# DashGraph 2.0

**Turn raw data into insights with a click. No code. No stress. Just powerful GPT-powered visualizations and EDA.**

---

## 🔍 Overview
**DashGraph 2.0** is an intelligent, user-friendly desktop application designed to simplify data exploration for everyone. Built with PyQt5 and powered by OpenAI's GPT models, DashGraph lets you load CSV files, filter and visualize data using natural language, and generate professional-grade Exploratory Data Analysis (EDA) reports with the help of AI.

Whether you're a data novice or a pro, DashGraph makes working with data easy, elegant, and insightful.

---

## ✨ Key Features

### 📂 CSV Loader
- Drag-and-drop or browse to load your dataset instantly
- Smart parsing of boolean, datetime, and categorical fields

### 🔍 Filter & Query
- Apply pandas-style filters with a visual interface
- One-click reset to return to the original dataset

### 🧠 Smart EDA Summary
- Generates a beautiful HTML report
- Includes correlation heatmaps, missing value maps, cardinality, skewness, and statistical summaries
- Auto-generates a natural language summary using GPT-4

### 📊 Natural Language Graph Generator
- Describe your plot in plain English (e.g., "show average salary by department")
- DashGraph interprets and generates matplotlib code using OpenAI's GPT models
- View and save the plot with one click

### 🎨 Themes
- Toggle between light and dark mode with a single click

### 📋 Copy & Save
- Export the latest chart or EDA report to your preferred directory

---

## 🧱 Tech Stack
- **Frontend:** PyQt5 (cross-platform UI)
- **Backend:** pandas, matplotlib, seaborn, OpenAI's Azure GPT endpoint
- **EDA:** missingno, seaborn, custom logic for skewness, cardinality, etc.

---

## ⚙️ Installation

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/dashgraph.git
cd dashgraph
```

### 2. Create virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install requirements
```bash
pip install -r requirements.txt
```

### 4. Set your OpenAI Azure API credentials
Create a `.env` file in the root folder:
```env
AZURE_API_KEY=your_api_key_here
AZURE_ENDPOINT=https://your-azure-endpoint.openai.azure.com/
AZURE_DEPLOYMENT=gpt-4o
```

### 5. Run the app
```bash
python main.py
```

---

## 📁 Project Structure
```
dashgraph/
├── main.py               # Entry point
├── ui.py                 # PyQt5 GUI logic
├── eda.py                # Top-level EDA runner
├── eda_logic.py          # Data profiling logic
├── eda_report.py         # HTML EDA report builder
├── eda_plots.py          # Plots (correlation, missingno)
├── gpt_handler.py        # Handles GPT prompt + response
├── helpers.py            # Utility functions (load CSV, display table)
├── config.py             # Loads environment variables
├── styles/
│   ├── light.qss         # Light theme
│   └── dark.qss          # Dark theme
├── assets/
│   └── icon.ico          # App icon
├── eda_reports/          # Output folder for EDA reports
├── .env                  # API secrets (excluded from git)
└── requirements.txt      # Python dependencies
```

---
## 📸 UI explanations
![image](https://github.com/user-attachments/assets/d1fbbd68-f29c-4728-9799-25718a732d61)

## 📄 Sample Reports
sample smart EDA reports can be found in the eda_reports folder

---

## 🛠 Requirements

Content of `requirements.txt`:
```txt
PyQt5
pandas
matplotlib
seaborn
missingno
openai
python-dotenv
```

---

## 🤖 Powered By
- [OpenAI GPT](https://platform.openai.com/)
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/cognitive-services/openai/overview)

---

## 📜 License
MIT License

---

## 🙌 Contributing
If you'd like to contribute or suggest a feature, open an issue or PR.
All suggestions are welcome!

---

## 💡 Inspiration
I built DashGraph 2.0 for **anyone intimidated by code** — analysts, students, product managers, and even curious business owners. Let LLMs turn your questions into insights.

---

## 🧠 Fun Idea?
Try asking: _"Compare sales and returns by product category using a grouped bar chart."_ DashGraph will do the rest!

---

> Designed for humans. Powered by AI.

## 📸 Screenshots
![image](https://github.com/user-attachments/assets/b798b3f9-112c-4a51-803b-cf254cbd8f91)
![image](https://github.com/user-attachments/assets/89f56a8c-3c5a-49c4-9250-9b6cd66f6822)
![image](https://github.com/user-attachments/assets/15c24f48-d037-46aa-acda-caf785669a27)
![image](https://github.com/user-attachments/assets/938a49e3-16fa-4f28-87da-03642d8d806b)
![image](https://github.com/user-attachments/assets/2555ef46-648c-42c4-bca5-3dd3c621e964)

