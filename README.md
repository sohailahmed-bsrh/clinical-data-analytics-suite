# 🫀 Clinical Data Analytics Suite & Cardiovascular Diagnostic Engine

A clinical decision support and epidemiological risk assessment web application built with Python and Streamlit. This project analyzes clinical trial records from the UCI Cleveland Clinic Heart Disease benchmark to profile hemodynamic biomarkers, evaluate electrocardiogram markers, and provide a machine learning cardiovascular screening engine.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## 🌟 Key Features

- **Clinical Epidemiological Dashboard:** Screened patient cohort metrics, prevalence tracking, and symptom presentation breakdowns.
- **Biomarker & Hemodynamic Matrix:** Cross-analysis of resting blood pressure, serum cholesterol, exercise-induced angina, and ST depression (`oldpeak`).
- **Live Cardiovascular Risk Screener:** Clinical input calculator generating diagnostic risk probability gauges and evidence-based clinical next steps.
- **Model Evaluation & Diagnostics:** Random Forest Classifier performance with ROC-AUC validation, confusion matrix, and biomarker importance hierarchy.

---

## 📊 Analytical Methodology

1. **Clinical Ingestion:** Ingested multi-center clinical patient trial data including resting blood pressure, serum cholesterol, electrocardiogram markers, and exercise stress testing outcomes.
2. **Key Insight:** Exercise-induced ST depression (`oldpeak`) and asymptomatic chest pain presentation represent the strongest diagnostic predictors of significant coronary artery disease.

---

## 💻 Local Setup & Execution

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sohailahmed-bsrh/clinical-data-analytics-suite.git
   cd clinical-data-analytics-suite
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Streamlit app:**
   ```bash
   streamlit run app.py
   ```

---

## 🚀 Deployment on Streamlit Community Cloud

1. Fork or push this repository to your GitHub account (`https://github.com/sohailahmed-bsrh/clinical-data-analytics-suite`).
2. Visit [share.streamlit.io](https://share.streamlit.io/) and log in with your GitHub account.
3. Click **New app**.
4. Select repository: `sohailahmed-bsrh/clinical-data-analytics-suite`
5. Branch: `main`
6. Main file path: `app.py`
7. Click **Deploy!**

---

## 👤 Author

**Sohail Ahmed**
- **GitHub:** [@sohailahmed-bsrh](https://github.com/sohailahmed-bsrh)
- **Portfolio:** [https://sohail.devsil.com](https://sohail.devsil.com)
