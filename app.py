import numpy as np
import pandas as pd
import streamlit as st
import joblib
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
ARIMA_DIR = OUTPUT_DIR / "arima_models"
RF_PATH = OUTPUT_DIR / "random_forest_risk_model.joblib"

PARAMETERS = {
    "DO (mg/L)": {
        "healthy": lambda x: x >= 5.0,
        "conditional": lambda x: 3.7 <= x < 5.0,
        "unit": "mg/L",
    },
    "pH": {
        "healthy": lambda x: 7.5 <= x <= 8.5,
        "conditional": lambda x: 6.5 <= x < 7.5 or 8.5 < x <= 9.0,
        "unit": "",
    },
    "Temp (OC)": {
        "healthy": lambda x: 26.0 <= x <= 30.0,
        "conditional": lambda x: 25.0 <= x < 26.0 or 30.0 < x <= 31.0,
        "unit": "°C",
    },
    "Salinity (ppt)": {
        "healthy": lambda x: 15.0 <= x <= 25.0,
        "conditional": lambda x: 10.0 <= x < 15.0 or 25.0 < x <= 30.0,
        "unit": "ppt",
    },
}

PARAM_COLS = list(PARAMETERS.keys())
STATUS_NAMES = {0: "Healthy", 1: "Conditional", 2: "Unhealthy"}
RISK_NAMES = {"Low": "Low Risk", "Moderate": "Moderate Risk", "High": "High Risk"}


@st.cache_resource
def load_models():
    if not RF_PATH.exists():
        raise FileNotFoundError(f"Random Forest model not found: {RF_PATH}")

    rf_bundle = joblib.load(RF_PATH)
    arima_models = {}

    if ARIMA_DIR.exists():
        for path in ARIMA_DIR.glob("*.joblib"):
            bundle = joblib.load(path)
            parameter = bundle.get("parameter")
            if parameter:
                arima_models[parameter] = bundle

    return rf_bundle, arima_models


def parameter_status(value, parameter):
    rules = PARAMETERS[parameter]
    if rules["healthy"](value):
        return 0
    if rules["conditional"](value):
        return 1
    return 2


def risk_from_score(score):
    if score <= 1:
        return "Low"
    if score <= 3:
        return "Moderate"
    return "High"


def build_rf_input(do, ph, temperature, salinity, timestamp, features):
    hour = timestamp.hour + timestamp.minute / 60
    month = timestamp.month

    row = {
        "DO (mg/L)": do,
        "pH": ph,
        "Temp (OC)": temperature,
        "Salinity (ppt)": salinity,
        "hour_sin": np.sin(2 * np.pi * hour / 24),
        "hour_cos": np.cos(2 * np.pi * hour / 24),
        "month_sin": np.sin(2 * np.pi * month / 12),
        "month_cos": np.cos(2 * np.pi * month / 12),
    }

    return pd.DataFrame([row])[features]


def detect(do, ph, temperature, salinity, timestamp, rf_bundle):
    model = rf_bundle["model"]
    features = rf_bundle["features"]
    x = build_rf_input(do, ph, temperature, salinity, timestamp, features)

    prediction = str(model.predict(x)[0])

    probabilities = {}
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(x)[0]
        probabilities = {
            str(cls): float(prob)
            for cls, prob in zip(model.classes_, probs)
        }

    values = {
        "DO (mg/L)": do,
        "pH": ph,
        "Temp (OC)": temperature,
        "Salinity (ppt)": salinity,
    }

    statuses = {
        p: parameter_status(values[p], p)
        for p in PARAM_COLS
    }

    score = sum(statuses.values())
    rule_risk = risk_from_score(score)

    return prediction, probabilities, statuses, score, rule_risk


def forecast_arima(arima_models, periods):
    result = pd.DataFrame({"Forecast Period": range(1, periods + 1)})

    for parameter in PARAM_COLS:
        bundle = arima_models.get(parameter)

        if bundle is None:
            result[parameter] = np.nan
            continue

        forecast = bundle["model"].get_forecast(steps=periods)
        result[parameter] = np.asarray(forecast.predicted_mean)

    for parameter in PARAM_COLS:
        result[parameter + " Status"] = result[parameter].apply(
            lambda x, p=parameter: parameter_status(x, p)
            if pd.notna(x) else np.nan
        )

    status_columns = [p + " Status" for p in PARAM_COLS]
    result["Risk Score"] = result[status_columns].sum(axis=1)

    result["Projected Risk"] = result["Risk Score"].apply(
        lambda x: risk_from_score(int(x)) if pd.notna(x) else "Unknown"
    )

    return result


st.set_page_config(
    page_title="Shrimp Water-Quality ML",
    page_icon="",
    layout="wide",
)

st.title("Shrimp Water-Quality Detection & Forecasting")
st.caption("Random Forest risk-condition classification + ARIMA water-quality forecasting")

try:
    rf_bundle, arima_models = load_models()
except Exception as e:
    st.error("Model loading failed.")
    st.code(str(e))
    st.info("Place this app.py in the same project folder as the outputs/ directory.")
    st.stop()

tab1, tab2, tab3 = st.tabs(
    ["Current Detection", "ARIMA Forecast", "Reference Thresholds"]
)

with tab1:
    st.subheader("Current Water-Quality Risk Detection")

    left, right = st.columns(2)

    with left:
        selected_date = st.date_input(
            "Observation date",
            value=pd.Timestamp.today().date(),
        )
        selected_time = st.time_input(
            "Observation time",
            value=pd.Timestamp.now().time().replace(second=0, microsecond=0),
        )
        do = st.number_input(
            "Dissolved Oxygen (mg/L)",
            min_value=0.0,
            max_value=20.0,
            value=5.0,
            step=0.1,
        )
        ph = st.number_input(
            "pH",
            min_value=0.0,
            max_value=14.0,
            value=8.0,
            step=0.1,
        )

    with right:
        temperature = st.number_input(
            "Temperature (°C)",
            min_value=0.0,
            max_value=50.0,
            value=28.0,
            step=0.1,
        )
        salinity = st.number_input(
            "Salinity (ppt)",
            min_value=0.0,
            max_value=50.0,
            value=20.0,
            step=0.1,
        )
        analyze = st.button(
            "Analyze Water Quality",
            type="primary",
            use_container_width=True,
        )

    if analyze:
        timestamp = pd.Timestamp.combine(selected_date, selected_time)

        prediction, probabilities, statuses, score, rule_risk = detect(
            do, ph, temperature, salinity, timestamp, rf_bundle
        )

        st.divider()

        c1, c2, c3 = st.columns(3)
        c1.metric("Random Forest Prediction", RISK_NAMES.get(prediction, prediction))
        c2.metric("Rule-Based Risk", RISK_NAMES[rule_risk])
        c3.metric("Risk Score", f"{score} / 8")

        st.subheader("Parameter Conditions")

        values = {
            "DO (mg/L)": do,
            "pH": ph,
            "Temp (OC)": temperature,
            "Salinity (ppt)": salinity,
        }

        rows = [
            {
                "Parameter": p,
                "Value": values[p],
                "Condition": STATUS_NAMES[statuses[p]],
            }
            for p in PARAM_COLS
        ]

        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        if probabilities:
            st.subheader("Random Forest Class Probabilities")
            probability_df = pd.DataFrame({
                "Risk Level": list(probabilities.keys()),
                "Probability": [f"{p * 100:.2f}%" for p in probabilities.values()],
            })
            st.dataframe(
                probability_df,
                use_container_width=True,
                hide_index=True,
            )

        st.warning(
            "Research note: the Random Forest target is an environmental "
            "risk-condition label derived from the supplied thresholds. "
            "It is not a validated biological shrimp-mortality label."
        )

with tab2:
    st.subheader("ARIMA Water-Quality Forecast")

    st.info(
        "The saved ARIMA models forecast DO, pH, temperature, and salinity. "
        "Forecasted values are then evaluated against the same thresholds."
    )

    st.write(f"Loaded ARIMA models: **{len(arima_models)}/{len(PARAM_COLS)}**")

    periods = st.slider("Forecast periods", 1, 30, 7)

    if st.button("Generate Forecast", type="primary", use_container_width=True):
        forecast_df = forecast_arima(arima_models, periods)

        st.subheader("Forecasted Water Quality")

        display_columns = [
            "Forecast Period",
            *PARAM_COLS,
            "Risk Score",
            "Projected Risk",
        ]

        st.dataframe(
            forecast_df[display_columns].round(3),
            use_container_width=True,
            hide_index=True,
        )

        st.subheader("Forecast Charts")

        for parameter in PARAM_COLS:
            st.line_chart(
                forecast_df.set_index("Forecast Period")[[parameter]]
            )

        st.subheader("Projected Risk")

        risk_counts = (
            forecast_df["Projected Risk"]
            .value_counts()
            .rename_axis("Risk Level")
            .reset_index(name="Periods")
        )

        st.dataframe(risk_counts, use_container_width=True, hide_index=True)

        st.download_button(
            "Download Forecast CSV",
            data=forecast_df.to_csv(index=False),
            file_name="water_quality_forecast.csv",
            mime="text/csv",
        )

with tab3:
    st.subheader("Water-Quality Reference Thresholds")

    rows = [
        {
            "Parameter": "DO",
            "Healthy": "≥ 5.0 mg/L",
            "Conditional": "3.7–4.9 mg/L",
            "Unhealthy": "< 3.7 mg/L",
        },
        {
            "Parameter": "pH",
            "Healthy": "7.5–8.5",
            "Conditional": "6.5–7.4 / 8.6–9.0",
            "Unhealthy": "< 6.5 / > 9.0",
        },
        {
            "Parameter": "Temperature",
            "Healthy": "26–30 °C",
            "Conditional": "25–25.9 / 30.1–31 °C",
            "Unhealthy": "< 25 / > 31 °C",
        },
        {
            "Parameter": "Salinity",
            "Healthy": "15–25 ppt",
            "Conditional": "10–14.9 / 25.1–30 ppt",
            "Unhealthy": "< 10 / > 30 ppt",
        },
    ]

    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

    st.subheader("Composite Risk Scoring")
    st.markdown(
        """
        - Healthy parameter = **0 points**
        - Conditional parameter = **1 point**
        - Unhealthy parameter = **2 points**
        - **Low Risk:** total score 0–1
        - **Moderate Risk:** total score 2–3
        - **High Risk:** total score 4 or more
        """
    )
