# Shrimp Water-Quality Detection and Forecasting Model

## Files

-   `shrimp_water_quality_detection_forecasting.ipynb` --- main VS
    Code/Jupyter notebook.
-   `MLDATASET - cleaned.xlsx` --- input dataset.
-   `requirements_shrimp_ml.txt` --- Python packages.

## VS Code setup

1.  Install Python 3.10+.
2.  Install the VS Code extensions:
    -   Python
    -   Jupyter
3.  Put the notebook and Excel dataset in the same folder.
4.  Open the notebook in VS Code.
5.  Select a Python kernel.
6.  Run the package-install cell, or in the VS Code terminal run:

``` bash
pip install -r requirements_shrimp_ml.txt
```

7.  Run the notebook from top to bottom.

## Model outputs

The notebook creates an `outputs/` folder containing:

-   `random_forest_risk_model.joblib`
-   `arima_validation_metrics.csv`
-   `water_quality_forecast_and_projected_risk.csv`

## Research interpretation

The Random Forest classifies environmental conditions into Low,
Moderate, and High Risk using a composite score derived from the
supplied Healthy/Conditional/Unhealthy thresholds.

Because the dataset does not contain observed shrimp mortality labels,
the model should be described as an **environmental risk-condition
classifier**, not as a validated shrimp-mortality predictor.

The ARIMA module forecasts DO, pH, temperature, and salinity for the
next seven monitoring periods and evaluates the forecast using MAE and
RMSE.
