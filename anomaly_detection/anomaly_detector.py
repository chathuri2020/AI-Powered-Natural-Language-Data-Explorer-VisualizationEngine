import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import random
from datetime import datetime, timedelta
from django.db import connection
from anomaly_detection.models import Transaction
import matplotlib.pyplot as plt
import io
import base64

# Parameters for the dataset


def fetch_data_from_db():
    query = Transaction.objects.all()[:300]
    # `values()` gives a list of dictionarie
    df = pd.DataFrame(list(query.values()))
    return df


def detect_anomalies():
    
    df = fetch_data_from_db()

    # Ensure 'timestamp' or similar column exists for plotting
    if 'date' not in df.columns:
        df['date'] = pd.date_range(
            start=datetime.now(), periods=len(df), freq='D')

    # Select numerical columns for anomaly detection
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    X = df[numeric_columns]

    # Apply Isolation Forest for anomaly detection
    model = IsolationForest(
        n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X)
    df['anomaly'] = model.predict(X)

    # Filter anomalies (-1 = anomaly, 1 = normal)
    anomalies = df[df['anomaly'] == -1]

    # Plot the data with anomalies highlighted
    plt.figure(figsize=(12, 6))
    for column in numeric_columns:
        plt.plot(df['date'], df[column], label=column)

    # Highlight anomalies for each numerical column
    for column in numeric_columns:
        plt.scatter(anomalies['date'], anomalies[column],
                    color='red', label=f'Anomaly in {column}', zorder=5)

    plt.title('Anomaly Detection Line Chart')
    plt.xlabel('Timestamp')
    plt.ylabel('Values')
    plt.legend()
    plt.grid(True)

    # Save the plot as a Base64 string for embedding in web apps
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    buf.close()

    return anomalies, img_base64
