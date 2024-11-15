import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import random
from datetime import datetime, timedelta
from django.db import connection

# Parameters for the dataset


def fetch_data_from_db():
    query = "SELECT * FROM transaction"
    with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=columns)
    return df


def detect_anomalies():
    df = fetch_data_from_db()

    # Select numerical columns for anomaly detection
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    X = df[numeric_columns]

    # Isolation Forest Algorithm
    model = IsolationForest(
        n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X)
    df['anomaly'] = model.predict(X)

    # Label anomalies (-1 = anomaly, 1 = normal)
    anomalies = df[df['anomaly'] == -1]
    return anomalies
