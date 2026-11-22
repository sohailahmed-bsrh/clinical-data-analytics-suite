# Clinical Data Analytics Suite

## Overview
The Clinical Data Analytics Suite provides statistical evaluation, exploratory data analysis, and operational reporting on hospital emergency department patient flows and wait times. Designed for clinical operations analysts, the suite surfaces triage bottlenecks, patient volume surges, and physician resource allocation dynamics.

## System Architecture

```mermaid
flowchart TD
    A[Raw Clinical Records: ER Wait Time Dataset.csv] --> B[Data Cleaning & Missing Value Imputation]
    B --> C[Feature Engineering & Triage Classification]
    C --> D[Statistical Exploratory Data Analysis]
    D --> E[Wait Time vs Acuity Correlation Analysis]
    E --> F[Resource Utilization & Peak Hour Heatmaps]
    F --> G[Operational Insights & Resource Allocation Recommendations]
```

## Core Features
- **Patient Flow Analysis**: Quantitative tracking of patient journey stages from triage intake to clinical consultation.
- **Triage Acuity Stratification**: Evaluation of emergency severity levels against standardized waiting thresholds.
- **Temporal Volume Decomposition**: Hourly, daily, and seasonal heatmaps isolating clinical surge intervals.
- **Statistical Significance Testing**: Hypothesis testing evaluating wait duration differentials across clinical departments.

## Repository Structure
```
clinical-data-analytics-suite/
|-- archive/
|   |-- ER Wait Time Data Overview.txt
|   +-- ER Wait Time Dataset.csv
|-- notebooks/
|   +-- ER.ipynb
|-- requirements.txt
+-- README.md
```

## Technology Stack
| Layer | Technologies |
| :--- | :--- |
| Core Language | Python 3.10+ |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib, Seaborn, Plotly |
| Statistical Computing | SciPy, Statsmodels |
| Notebook Environment | JupyterLab |

## Installation & Execution
```bash
# Clone the repository
git clone https://github.com/sohailahmed-bsrh/clinical-data-analytics-suite.git
cd clinical-data-analytics-suite

# Install dependencies
pip install -r requirements.txt

# Launch exploratory analysis notebook
jupyter notebook notebooks/ER.ipynb
```

---

## Author & Contact Information

<table width="100%" align="center">
  <tr>
    <td align="center" style="padding: 20px;">
      <h3>Sohail Ahmed</h3>
      <p><strong>Full-Stack Artificial Intelligence & Computer Vision Engineer</strong></p>
      <p>
        <a href="https://sohail.devsil.com"><img src="https://img.shields.io/badge/Live_Portfolio-sohail.devsil.com-0052FF?style=for-the-badge&logo=google-chrome&logoColor=white" alt="Portfolio"/></a>
        <a href="https://github.com/sohailahmed-bsrh"><img src="https://img.shields.io/badge/GitHub-Profile-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/></a>
        <a href="https://linkedin.com/in/sohail-ahmed-dev"><img src="https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white" alt="LinkedIn"/></a>
        <a href="mailto:sohail.bsrh@gmail.com"><img src="https://img.shields.io/badge/Email-Contact_Me-EA4335?style=for-the-badge&logo=gmail&logoColor=white" alt="Email"/></a>
      </p>
      <p><em>Available for technical roles in Artificial Intelligence, Computer Vision, and Full-Stack Engineering.</em></p>
      <hr style="border: 0; height: 1px; background: #30363d; margin: 15px 0;">
      <small>Distributed under the MIT License.</small>
    </td>
  </tr>
</table>
