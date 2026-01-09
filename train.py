import os
import json
import pandas as pd
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score


def main():
    # 1. Load the dataset
    red_path = "dataset/wine+quality/winequality-red.csv"
    white_path = "dataset/wine+quality/winequality-white.csv"

    red = pd.read_csv(red_path, sep=";")
    white = pd.read_csv(white_path, sep=";")

    data = pd.concat([red, white], axis=0)

    # 2. Pre-processing & feature selection
    X = data.drop("quality", axis=1)
    y = data["quality"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    # 3. Train the model
    # model = Ridge(alpha=1.0)
    # model = RandomForestRegressor(
    #     n_estimators=100,
    #     random_state=42
    # )
    # model = LinearRegression()
    model = LinearRegression()
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)

    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    # 5. Save model & metrics
    os.makedirs("output", exist_ok=True)

    joblib.dump(model, "output/model.pkl")

    metrics = {
        "Mean Squared Error": mse,
        "R2 Score": r2
    }

    with open("output/metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    # 6. Print metrics
    print("Model Evaluation Results")
    print("------------------------")
    print(f"MSE: {mse:.4f}")
    print(f"R² Score: {r2:.4f}")


if __name__ == "__main__":
    main()
