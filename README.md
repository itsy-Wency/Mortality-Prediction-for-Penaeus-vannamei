<div align="center">

<img src="assets/animated-banner.svg" alt="Shrimp Water-Quality Detection and Forecasting" width="100%">

<br>

<a href="https://forecasting-mortality-prediction-for-penaeus-vannamei.streamlit.app/">
  <img src="https://img.shields.io/badge/LIVE%20APPLICATION-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Live application">
</a>
&nbsp;
<a href="https://github.com/itsy-Wency/Mortality-Prediction-for-Penaeus-vannamei">
  <img src="https://img.shields.io/badge/SOURCE%20CODE-GitHub-181717?style=for-the-badge&logo=github&logoColor=white" alt="Source code">
</a>

<br><br>

<img src="https://readme-typing-svg.demolab.com?font=Inter&weight=600&size=18&duration=2600&pause=800&color=36CFC9&center=true&vCenter=true&width=760&lines=Detect+environmental+risk;Forecast+future+water-quality+conditions;Visualize+model-driven+aquaculture+insights" alt="Animated project description">

</div>

---

## Project Overview

This project implements a **water-quality detection and short-term forecasting prototype** for *Penaeus vannamei* aquaculture.

It combines a Random Forest classification model with parameter-specific ARIMA forecasting models and exposes the trained models through a Streamlit web application.

### Core capabilities

| Component | Function | Result |
|---|---|---|
| Random Forest | Environmental risk-condition classification | Low / Moderate / High Risk |
| ARIMA | Short-term water-quality forecasting | Future DO, pH, temperature, salinity |
| Threshold engine | Parameter condition interpretation | Healthy / Conditional / Unhealthy |
| Streamlit | Interactive simulation interface | Browser-based model demonstration |

---

## Live Application

<div align="center">

<a href="https://forecasting-mortality-prediction-for-penaeus-vannamei.streamlit.app/">
  <img src="https://img.shields.io/badge/Open%20the%20Live%20Application-View%20Demo-0B7285?style=for-the-badge&logo=streamlit&logoColor=white" alt="Open live application">
</a>

<br><br>

<strong>https://forecasting-mortality-prediction-for-penaeus-vannamei.streamlit.app/</strong>

</div>

---

## Application Preview

Then the preview will render below:

<div align="center">

<img src="assets/preview.png" alt="Streamlit application preview" width="92%">

<br>

<sub>Interactive water-quality detection and forecasting interface.</sub>

</div>

---

## Model Architecture

```mermaid
flowchart LR
    A["Water-quality measurements"] --> B["Preprocessing"]

    B --> C["Random Forest"]
    B --> D["ARIMA models"]

    C --> E["Environmental risk classification"]
    E --> F["Low / Moderate / High"]

    D --> G["DO forecast"]
    D --> H["pH forecast"]
    D --> I["Temperature forecast"]
    D --> J["Salinity forecast"]

    G --> K["Threshold evaluation"]
    H --> K
    I --> K
    J --> K

    K --> L["Projected environmental risk"]
```

---

## Water-Quality Thresholds

| Parameter | Healthy | Conditional | Unhealthy |
|---|---|---|---|
| **Dissolved Oxygen** | ≥ 5.0 mg/L | 3.7–4.9 mg/L | < 3.7 mg/L |
| **pH** | 7.5–8.5 | 6.5–7.4 / 8.6–9.0 | < 6.5 / > 9.0 |
| **Temperature** | 26–30 °C | 25–25.9 / 30.1–31 °C | < 25 / > 31 °C |
| **Salinity** | 15–25 ppt | 10–14.9 / 25.1–30 ppt | < 10 / > 30 ppt |

### Composite Risk Scoring

```text
Healthy      = 0 points
Conditional  = 1 point
Unhealthy    = 2 points

0–1 points   → Low Risk
2–3 points   → Moderate Risk
4+ points    → High Risk
```

---

## Machine Learning Pipeline

```text
Historical water-quality dataset
            |
            v
      Data preparation
            |
      +-----+-----+
      |           |
      v           v
 Random Forest   ARIMA
      |           |
      v           v
 Current risk   Forecasts
      |           |
      +-----+-----+
            |
            v
    Threshold evaluation
            |
            v
 Environmental interpretation
```

---

## Project Structure

```text
Mortality-Prediction-for-Penaeus-vannamei/
│
├── assets/
│   ├── animated-banner.svg
│   └── preview.png
│
├── outputs/
│   ├── arima_models/
│   │   ├── arima_DO_mg_L.joblib
│   │   ├── arima_pH.joblib
│   │   ├── arima_Salinity_ppt.joblib
│   │   └── arima_Temp_OC.joblib
│   │
│   ├── random_forest_risk_model.joblib
│   ├── arima_validation_metrics.csv
│   └── water_quality_forecast_and_projected_risk.csv
│
├── app.py
├── requirements.txt
├── requirements_shrimp_ml.txt
├── MLDATASET - cleaned.xlsx
├── shrimp_water_quality_detection_forecasting.ipynb
├── shrimp_water_quality_detection_forecasting_executed.ipynb
├── README.md
└── LICENSE
```

---

## Technology Stack

<div align="center">

<a href="https://www.python.org/">
  <img src="https://cdn.simpleicons.org/python/3776AB" alt="Python" width="48" height="48">
</a>
&nbsp;&nbsp;&nbsp;

<a href="https://streamlit.io/">
  <img src="https://cdn.simpleicons.org/streamlit/FF4B4B" alt="Streamlit" width="48" height="48">
</a>
&nbsp;&nbsp;&nbsp;

<a href="https://scikit-learn.org/">
  <img src="https://cdn.simpleicons.org/scikitlearn/F7931E" alt="Scikit-learn" width="48" height="48">
</a>
&nbsp;&nbsp;&nbsp;

<a href="https://pandas.pydata.org/">
  <img src="https://cdn.simpleicons.org/pandas/150458" alt="Pandas" width="48" height="48">
</a>
&nbsp;&nbsp;&nbsp;

<a href="https://numpy.org/">
  <img src="https://cdn.simpleicons.org/numpy/013243" alt="NumPy" width="48" height="48">
</a>
&nbsp;&nbsp;&nbsp;

<a href="https://matplotlib.org/">
  <img src="https://cdn.simpleicons.org/matplotlib/11557C" alt="Matplotlib" width="48" height="48">
</a>
&nbsp;&nbsp;&nbsp;

<a href="https://www.statsmodels.org/">
  <img src="https://cdn.simpleicons.org/statsmodels/4051B5" alt="Statsmodels" width="48" height="48">
</a>
&nbsp;&nbsp;&nbsp;

<a href="https://jupyter.org/">
  <img src="https://cdn.simpleicons.org/jupyter/F37626" alt="Jupyter" width="48" height="48">
</a>
&nbsp;&nbsp;&nbsp;

<a href="https://code.visualstudio.com/">
  <img src="https://cdn.simpleicons.org/visualstudiocode/007ACC" alt="Visual Studio Code" width="48" height="48">
</a>
&nbsp;&nbsp;&nbsp;

<a href="https://github.com/">
  <img src="https://cdn.simpleicons.org/github/FFFFFF" alt="GitHub" width="48" height="48">
</a>

<br><br>

<sub>
Python · Streamlit · Scikit-learn · Pandas · NumPy · Matplotlib · Statsmodels · Jupyter · VS Code · GitHub
</sub>

</div>
---

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/itsy-Wency/Mortality-Prediction-for-Penaeus-vannamei.git
cd Mortality-Prediction-for-Penaeus-vannamei
```

### 2. Create the virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install application dependencies

```powershell
python -m pip install -r requirements.txt
```

For notebook/model development:

```powershell
python -m pip install -r requirements_shrimp_ml.txt
```

### 4. Run the Streamlit application

```powershell
streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

## Notebook Workflow

Open the main notebook in VS Code:

```text
shrimp_water_quality_detection_forecasting.ipynb
```

Select the project virtual environment as the Python kernel and execute the notebook from top to bottom.

The notebook trains and exports the model artifacts used by the Streamlit application.

---

## Model Artifacts

The deployed application loads serialized models using Joblib:

```text
outputs/
├── random_forest_risk_model.joblib
└── arima_models/
    ├── arima_DO_mg_L.joblib
    ├── arima_pH.joblib
    ├── arima_Salinity_ppt.joblib
    └── arima_Temp_OC.joblib
```

Using serialized models allows the web application to perform inference without retraining the models each time the application starts.

For reproducibility, keep the Python and model-library versions compatible with the environment used during training.

---

## Forecast Evaluation

The ARIMA workflow evaluates forecasts using:

- **MAE** — Mean Absolute Error
- **RMSE** — Root Mean Squared Error

Generated evaluation files include:

```text
outputs/arima_validation_metrics.csv
outputs/water_quality_forecast_and_projected_risk.csv
```

---

## Demonstration Scenarios

### Baseline healthy condition

```text
DO          = 5.0 mg/L
pH          = 8.0
Temperature = 28 °C
Salinity    = 20 ppt
```

### High-stress simulation

```text
DO          = 2.0 mg/L
pH          = 6.0
Temperature = 33 °C
Salinity    = 35 ppt
```

These values are intended for **application demonstration and model simulation**, not as biological treatment recommendations.

---

## Research Scope and Limitation

The current dataset does not contain verified observed shrimp mortality/event labels.

Consequently, the Random Forest output should be interpreted as an:

> **Environmental risk-condition classification**

rather than a validated biological shrimp-mortality prediction.

The system should not be presented as:

- a validated shrimp mortality predictor;
- a guaranteed mortality warning system;
- a replacement for aquaculture expert assessment; or
- a validated production decision-support system.

A validated mortality prediction model would require appropriately labeled historical mortality/event data and independent biological validation.

---

## Research Interpretation

The overall research workflow combines:

```text
Water-quality monitoring
        +
Environmental threshold interpretation
        +
Random Forest classification
        +
ARIMA time-series forecasting
        =
Environmental risk-condition intelligence
```

The system is intended to demonstrate how machine-learning classification and time-series forecasting can be integrated into an interactive aquaculture monitoring prototype.

---

## License

This project is distributed under the MIT License.

See [`LICENSE`](LICENSE) for details.

---

<div align="center">

<a href="https://forecasting-mortality-prediction-for-penaeus-vannamei.streamlit.app/">
  <img src="https://img.shields.io/badge/OPEN%20LIVE%20APPLICATION-0B7285?style=for-the-badge&logo=streamlit&logoColor=white" alt="Open live application">
</a>

<br><br>

<sub>Research prototype for water-quality detection and forecasting in Penaeus vannamei aquaculture.</sub>

</div>
