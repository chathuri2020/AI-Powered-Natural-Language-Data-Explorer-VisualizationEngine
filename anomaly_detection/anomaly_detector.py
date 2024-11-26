import base64
from io import BytesIO
from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
import random
from datetime import datetime, timedelta
from django.db import connection
from anomaly_detection.models import Transaction
from anomaly_detection.models import Loan
from anomaly_detection.models import Order

# Parameters for the dataset


#def fetch_data_from_db():
    #query = Transaction.objects.all()[:100]
   
    #df = pd.DataFrame(list(query.values()))  # `values()` gives a list of dictionaries
    
    #return df
    
def fetch_data_from_db(table_name):
    if table_name == "transaction":
        query = Transaction.objects.all()[:100]
    elif table_name == "loan":
        # Assuming there's a Loan model
        query = Loan.objects.all()[:100]
    elif table_name == "order":
        # Assuming there's an Order model
        query = Order.objects.all()[:100]
    else:
        return pd.DataFrame()  # Return empty DataFrame for unsupported tables
    
    return pd.DataFrame(list(query.values()))


def detect_anomalies():
    df = fetch_data_from_db("transaction")

    # Select numerical columns for anomaly detection
    numeric_columns = df.select_dtypes(include=[np.number]).columns
    X = df[numeric_columns]

    # Isolation Forest Algorithm
    model = IsolationForest(
        n_estimators=100, contamination=0.05, random_state=42)
    model.fit(X)
    df['anomaly'] = model.predict(X)
    plot_anomalies(df, numeric_columns)
    # Label anomalies (-1 = anomaly, 1 = normal)
    anomalies = df[df['anomaly'] == -1]
    return anomalies


def plot_anomalies(df, numeric_columns):
    # Ensure 'anomaly' column is in the dataframe
    if 'anomaly' not in df.columns:
        raise ValueError("'anomaly' column not found in the DataFrame")

    # Select two numerical columns for the scatter plot
    if len(numeric_columns) < 2:
        raise ValueError("At least two numerical columns are required for a scatter plot")

    x_col, y_col = numeric_columns[:2]  # Use the first two numeric columns for the plot
    normal_data = df[df['anomaly'] == 1]
    anomaly_data = df[df['anomaly'] == -1]

    # Plotting the data
    plt.figure(figsize=(10, 6))
    plt.scatter(normal_data[x_col], normal_data[y_col], c='blue', label='Normal', alpha=0.7)
    plt.scatter(anomaly_data[x_col], anomaly_data[y_col], c='red', label='Anomaly', alpha=0.7)
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title('Anomalies Detection')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    plt.close()

    return image_base64
