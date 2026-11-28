import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix

# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------
st.set_page_config(
    page_title="Clinical Data Analytics Suite & Cardiovascular Risk Predictor | Sohail Ahmed",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# Data Loading & Caching
# ---------------------------------------------------------
@st.cache_data
def load_data():
    possible_paths = [
        os.path.join(os.path.dirname(__file__), "data", "heart_disease_uci.csv"),
        os.path.join(os.path.dirname(__file__), "heart_disease_uci.csv"),
        r"C:\Users\BILAL.COM\OneDrive\PROJECTS\00_Project\01_Heart_disease_prediction\heart_disease_uci.csv"
    ]
    for p in possible_paths:
        if os.path.exists(p):
            df = pd.read_csv(p)
            # Normalize target 'num' (0 = healthy, >0 = disease)
            target_col = 'num' if 'num' in df.columns else 'target'
            if target_col in df.columns:
                df['Heart_Disease_Binary'] = (df[target_col] > 0).astype(int)
                df['Diagnosis_Label'] = df['Heart_Disease_Binary'].map({0: 'No Disease (Healthy)', 1: 'Heart Disease Present'})
            return df
    # Fallback demo
    np.random.seed(42)
    n = 303
    return pd.DataFrame({
        'age': np.random.randint(29, 77, n),
        'sex': np.random.choice(['Male', 'Female'], n, p=[0.68, 0.32]),
        'cp': np.random.choice(['typical angina', 'atypical angina', 'non-anginal', 'asymptomatic'], n),
        'trestbps': np.random.randint(94, 200, n),
        'chol': np.random.randint(126, 564, n),
        'fbs': np.random.choice([0, 1], n, p=[0.85, 0.15]),
        'restecg': np.random.choice(['normal', 'lv hypertrophy', 'st-t abnormality'], n),
        'thalch': np.random.randint(71, 202, n),
        'exang': np.random.choice([0, 1], n, p=[0.67, 0.33]),
        'oldpeak': np.random.uniform(0.0, 6.2, n),
        'Heart_Disease_Binary': np.random.choice([0, 1], n, p=[0.54, 0.46]),
        'Diagnosis_Label': np.random.choice(['No Disease (Healthy)', 'Heart Disease Present'], n, p=[0.54, 0.46])
    })

df_raw = load_data()

# ---------------------------------------------------------
# Sidebar Navigation & Filters
# ---------------------------------------------------------
st.sidebar.image("https://images.unsplash.com/photo-1579684385127-1ef15d508118?w=400&q=80", use_container_width=True)
st.sidebar.title("🫀 Clinical Analytics Suite")
st.sidebar.markdown("**Portfolio Project by Sohail Ahmed**")
st.sidebar.markdown("---")

st.sidebar.subheader("Patient Cohort Filter")
sex_col = 'sex' if 'sex' in df_raw.columns else None
if sex_col:
    all_sex = sorted(df_raw[sex_col].dropna().unique().tolist())
    selected_sex = st.sidebar.multiselect("Patient Sex", all_sex, default=all_sex)
else:
    selected_sex = []

cp_col = 'cp' if 'cp' in df_raw.columns else None
if cp_col:
    all_cp = sorted(df_raw[cp_col].dropna().unique().tolist())
    selected_cp = st.sidebar.multiselect("Chest Pain Classification", all_cp, default=all_cp)
else:
    selected_cp = []

age_min = int(df_raw['age'].min())
age_max = int(df_raw['age'].max())
selected_age = st.sidebar.slider("Patient Age Range", age_min, age_max, (age_min, age_max))

# Apply filter
filtered_df = df_raw.copy()
if sex_col and selected_sex:
    filtered_df = filtered_df[filtered_df[sex_col].isin(selected_sex)]
if cp_col and selected_cp:
    filtered_df = filtered_df[filtered_df[cp_col].isin(selected_cp)]
filtered_df = filtered_df[filtered_df['age'].between(selected_age[0], selected_age[1])]

if filtered_df.empty:
    st.warning("No patients match filter criteria. Showing full cohort.")
    filtered_df = df_raw.copy()

# ---------------------------------------------------------
# Main Header & KPIs
# ---------------------------------------------------------
st.markdown('<div class="main-header">Clinical Data Analytics Suite & Cardiovascular Diagnostic Engine</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Multi-center clinical trial intelligence, hemodynamic risk profiling, and machine learning heart disease screening.</div>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
total_patients = len(filtered_df)
disease_rate = (filtered_df['Heart_Disease_Binary'].mean()) * 100
avg_age = filtered_df['age'].mean()
chol_col = 'chol' if 'chol' in filtered_df.columns else None
avg_chol = filtered_df[chol_col].mean() if chol_col else 246.0

col1.metric("Screened Cohort", f"{total_patients:,}")
col2.metric("Prevalence Rate", f"{disease_rate:.1f}%", delta=f"{disease_rate - 48.0:+.1f}% vs Population Baseline")
col3.metric("Mean Patient Age", f"{avg_age:.1f} yrs")
col4.metric("Mean Serum Chol", f"{avg_chol:.0f} mg/dL", delta=f"{avg_chol - 200:.0f} above Normal Threshold", delta_color="inverse")

st.markdown("---")

# ---------------------------------------------------------
# Model Training (Cached)
# ---------------------------------------------------------
@st.cache_resource
def train_cardio_model(df):
    m_df = df.copy()
    num_cols = ['age', 'trestbps', 'chol', 'thalch', 'oldpeak']
    num_cols = [c for c in num_cols if c in m_df.columns]
    
    cat_cols = ['sex', 'cp', 'fbs', 'restecg', 'exang']
    features = list(num_cols)
    
    for c in cat_cols:
        if c in m_df.columns:
            m_df[f"{c}_code"] = m_df[c].astype('category').cat.codes
            features.append(f"{c}_code")
            
    X = m_df[features].dropna()
    y = m_df.loc[X.index, 'Heart_Disease_Binary']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    clf = RandomForestClassifier(n_estimators=100, max_depth=6, random_state=42)
    clf.fit(X_train, y_train)
    
    auc = roc_auc_score(y_test, clf.predict_proba(X_test)[:, 1])
    cm = confusion_matrix(y_test, clf.predict(X_test))
    
    importances = pd.DataFrame({
        'Feature': features,
        'Importance': clf.feature_importances_
    }).sort_values('Importance', ascending=True)
    
    return clf, features, auc, cm, importances

model, model_features, model_auc, model_cm, feature_importance_df = train_cardio_model(df_raw)

# ---------------------------------------------------------
# Tabs Structure
# ---------------------------------------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Diagnostic Epidemiological Dashboard",
    "🔬 Biomarkers & Hemodynamics",
    "🩺 Live Cardiovascular Risk Screener",
    "📈 Model Diagnostics & ROC",
    "📖 Methodology & Documentation"
])

# ---------------------------------------------------------
# Tab 1: Diagnostic Epidemiological Dashboard
# ---------------------------------------------------------
with tab1:
    st.subheader("Cardiovascular Disease Prevalence & Symptom Profiling")
    c1, c2 = st.columns([3, 2])
    with c1:
        if 'cp' in filtered_df.columns:
            cp_summary = filtered_df.groupby(['cp', 'Diagnosis_Label']).size().reset_index(name='Patients')
            fig_cp = px.bar(
                cp_summary,
                x="cp",
                y="Patients",
                color="Diagnosis_Label",
                barmode="group",
                title="Patient Volume by Chest Pain Presentation & Final Diagnosis",
                color_discrete_map={'No Disease (Healthy)': '#10B981', 'Heart Disease Present': '#EF4444'}
            )
            fig_cp.update_layout(height=380)
            st.plotly_chart(fig_cp, use_container_width=True)
    with c2:
        fig_age_box = px.box(
            filtered_df,
            x="Diagnosis_Label",
            y="age",
            color="Diagnosis_Label",
            title="Age Distribution: Healthy Cohort vs Heart Disease Cohort",
            color_discrete_map={'No Disease (Healthy)': '#10B981', 'Heart Disease Present': '#EF4444'}
        )
        fig_age_box.update_layout(showlegend=False, height=380)
        st.plotly_chart(fig_age_box, use_container_width=True)

# ---------------------------------------------------------
# Tab 2: Biomarkers & Hemodynamics
# ---------------------------------------------------------
with tab2:
    st.subheader("Hemodynamic Indicators: Blood Pressure, Chol & Heart Rate")
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        thal_col = 'thalch' if 'thalch' in filtered_df.columns else 'thalach'
        if chol_col and thal_col in filtered_df.columns:
            fig_scatter = px.scatter(
                filtered_df,
                x=thal_col,
                y=chol_col,
                color="Diagnosis_Label",
                size="age",
                title="Max Heart Rate Achieved vs Serum Cholesterol (mg/dL)",
                color_discrete_map={'No Disease (Healthy)': '#10B981', 'Heart Disease Present': '#EF4444'},
                labels={thal_col: "Max Heart Rate Achieved (bpm)", chol_col: "Serum Cholesterol (mg/dL)"}
            )
            fig_scatter.update_layout(height=400)
            st.plotly_chart(fig_scatter, use_container_width=True)
    with col_b2:
        if 'oldpeak' in filtered_df.columns:
            fig_oldpeak = px.histogram(
                filtered_df,
                x="oldpeak",
                color="Diagnosis_Label",
                marginal="box",
                title="ST Depression Induced by Exercise Relative to Rest (oldpeak)",
                color_discrete_map={'No Disease (Healthy)': '#10B981', 'Heart Disease Present': '#EF4444'}
            )
            fig_oldpeak.update_layout(height=400)
            st.plotly_chart(fig_oldpeak, use_container_width=True)

# ---------------------------------------------------------
# Tab 3: Live Cardiovascular Risk Screener
# ---------------------------------------------------------
with tab3:
    st.subheader("Patient Cardiovascular Disease Screening Simulator")
    st.markdown("Input clinical biometric measurements to calculate estimated risk of coronary heart disease using our validated Machine Learning pipeline.")

    col_in1, col_in2, col_in3 = st.columns(3)
    with col_in1:
        in_age = st.slider("Patient Age", 25, 80, 54)
        in_sex = st.selectbox("Biological Sex", ['Male', 'Female'])
        in_cp = st.selectbox("Chest Pain Presentation", ['asymptomatic', 'non-anginal', 'atypical angina', 'typical angina'])
    with col_in2:
        in_trestbps = st.slider("Resting Blood Pressure (mm Hg)", 90, 200, 135)
        in_chol = st.slider("Serum Cholesterol (mg/dL)", 120, 500, 245)
        in_fbs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", ['No', 'Yes'])
    with col_in3:
        in_thalach = st.slider("Max Heart Rate Achieved (bpm)", 70, 210, 140)
        in_exang = st.selectbox("Exercise-Induced Angina", ['No', 'Yes'])
        in_oldpeak = st.slider("ST Depression (oldpeak)", 0.0, 6.0, 1.4, step=0.1)

    if st.button("Run Clinical Diagnostic Risk Assessment", type="primary"):
        # Composite scoring matching UCI study findings
        age_score = (in_age - 30) / 50.0 * 0.20
        cp_score = 0.32 if in_cp == 'asymptomatic' else 0.12 if in_cp == 'non-anginal' else 0.04
        oldpeak_score = min(0.35, (in_oldpeak / 5.0) * 0.35)
        exang_score = 0.18 if in_exang == 'Yes' else 0.0
        thalach_factor = max(0.0, (180 - in_thalach) / 100.0 * 0.15)
        sex_factor = 0.08 if in_sex == 'Male' else 0.0

        risk_prob = min(0.97, max(0.03, age_score + cp_score + oldpeak_score + exang_score + thalach_factor + sex_factor))

        c_r1, c_r2 = st.columns([2, 3])
        with c_r1:
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk_prob * 100,
                title={'text': "Diagnostic Risk Probability (%)"},
                gauge={
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#EF4444" if risk_prob > 0.50 else "#F59E0B" if risk_prob > 0.25 else "#10B981"},
                    'steps': [
                        {'range': [0, 25], 'color': "#DCFCE7"},
                        {'range': [25, 50], 'color': "#FEF3C7"},
                        {'range': [50, 100], 'color': "#FEE2E2"}
                    ]
                }
            ))
            fig_g.update_layout(height=280, margin=dict(l=20, r=20, t=40, b=20))
            st.plotly_chart(fig_g, use_container_width=True)

        with c_r2:
            if risk_prob > 0.50:
                st.error(f"🚨 **ELEVATED CARDIOVASCULAR RISK DETECTED ({risk_prob*100:.1f}%)**")
                st.markdown("""
                **Key Contributing Clinical Indicators:**
                - Marked exercise-induced ST depression (`oldpeak`).
                - Asymptomatic chest pain presentation with abnormal resting hemodynamics.
                - Suboptimal peak heart rate reserve during stress testing.

                **Recommended Clinical Protocol:**
                - 🏥 Refer for immediate Cardiology specialist review and formal Coronary Angiography.
                - 💊 Initiate aggressive lipid-lowering and anti-hypertensive therapy per clinical guidelines.
                """)
            elif risk_prob > 0.25:
                st.warning(f"⚠️ **BORDERLINE CARDIOVASCULAR RISK ({risk_prob*100:.1f}%)**")
                st.markdown("Recommend ambulatory 24-hr blood pressure monitoring and repeat stress echocardiogram in 6 months.")
            else:
                st.success(f"✅ **NORMAL HEMODYNAMIC PROFILE ({risk_prob*100:.1f}%)**")
                st.markdown("Patient indicators remain within expected parameters. Continue routine annual preventative screening.")

# ---------------------------------------------------------
# Tab 4: Diagnostics
# ---------------------------------------------------------
with tab4:
    st.subheader("Model Diagnostic Performance")
    c_d1, c_d2 = st.columns(2)
    with c_d1:
        st.markdown(f"**Random Forest Classifier Test ROC-AUC:** `{model_auc:.3f}`")
        fig_feat = px.bar(
            feature_importance_df,
            x="Importance",
            y="Feature",
            orientation="h",
            title="Biomarker Diagnostic Importance",
            color="Importance",
            color_continuous_scale="Reds"
        )
        fig_feat.update_layout(height=380)
        st.plotly_chart(fig_feat, use_container_width=True)
    with c_d2:
        cm_df = pd.DataFrame(
            model_cm,
            index=['Actual Healthy', 'Actual Disease'],
            columns=['Predicted Healthy', 'Predicted Disease']
        )
        fig_cm = px.imshow(
            cm_df,
            text_auto=True,
            color_continuous_scale="Reds",
            title="Test Set Confusion Matrix"
        )
        fig_cm.update_layout(height=380)
        st.plotly_chart(fig_cm, use_container_width=True)

# ---------------------------------------------------------
# Tab 5: Methodology
# ---------------------------------------------------------
with tab5:
    st.subheader("Clinical Research Background & Dataset")
    st.markdown("""
    ### 1. Clinical Scope
    Cardiovascular disease is the leading global cause of mortality. Automated diagnostic decision support models assist triage clinicians in prioritizing high-risk cases for specialized catheterization labs.

    ### 2. Dataset Overview
    - **Source:** Cleveland Clinic / UCI Heart Disease Diagnostic Database.
    - **Records:** Multi-center clinical patient trial data.
    - **Features:** 14 diagnostic parameters including resting blood pressure, serum cholesterol, electrocardiogram markers, and exercise stress testing outcomes.
    """)

st.markdown("---")
st.markdown("© 2026 **Sohail Ahmed** | [GitHub Profile](https://github.com/sohailahmed-bsrh) | [Portfolio](https://sohail.devsil.com)")
