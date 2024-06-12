from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import pickle

app = Flask(__name__)

# Load the dataset and preprocessing
df = pd.read_csv("World_Dataset_After_preprossing.csv")
df.set_index("Date", inplace=True)
df.index = pd.to_datetime(df.index)

# Normalize CO2 emissions
scaler = MinMaxScaler()
CO2_emissions = df["value of Co2 emissions"].values.reshape(-1, 1)
CO2_emissions_normalized = scaler.fit_transform(CO2_emissions)
df["value of Co2 emissions"] = CO2_emissions_normalized

# Define COVID-19 period
start_date = pd.to_datetime("2020-04-01")
end_date = pd.to_datetime("2020-08-01")
df["covid"] = [1 if start_date <= x <= end_date else 0 for x in df.index]


def create_features(Temp_df):
    """
    Create time series features based on time series index.

    Parameters:
    Temp_df (DataFrame): Input DataFrame with datetime index.

    Returns:
    DataFrame: DataFrame with added time series features.
    """
    Temp_df = Temp_df.copy()
    Temp_df["quarter"] = Temp_df.index.quarter
    Temp_df["month"] = Temp_df.index.month
    Temp_df["year"] = Temp_df.index.year
    return Temp_df


df = create_features(df)

# Load models
models = {}
model_names = [
    "Linear_Regression",
    "Ridge_Regression",
    "Lasso_Regression",
    "Decision_Tree",
    "Random_Forest",
    "Support_Vector_Machine",
]
for name in model_names:
    with open(f"./models/{name}.pkl", "rb") as f:
        models[name.replace("_", " ")] = pickle.load(f)


@app.route("/")
def index():
    """
    Render the main page of the web application.

    Returns:
    HTML: Rendered HTML template with model names.
    """
    return render_template("index.html", model_names=models.keys())


@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict CO2 emissions for a specific year and month using the selected model.

    Returns:
    JSON: JSON response containing the predicted CO2 emissions.
    """
    model_name = request.form["model"]
    year = int(request.form["year"])
    month = int(request.form["month"])

    date = pd.to_datetime(f"{year}-{month:02d}-01")
    temp_df = pd.DataFrame([date], index=[date])
    temp_df = create_features(temp_df)
    temp_df["covid"] = 0

    X = temp_df[["quarter", "month", "year", "covid"]]
    model = models[model_name]
    prediction = model.predict(X)[0]
    prediction_rescaled = scaler.inverse_transform([[prediction]])[0][0]

    return jsonify({"prediction": prediction_rescaled})


if __name__ == "__main__":
    app.run(debug=True)
