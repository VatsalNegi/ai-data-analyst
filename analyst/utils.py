import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os
import requests
import traceback

from django.conf import settings


# =====================================================
# CSV ANALYSIS
# =====================================================

def analyze_csv(file_path):
    """
    Reads CSV and returns structured summary.
    """
    try:
        df = pd.read_csv(file_path)

        summary = {
            "rows": int(df.shape[0]),
            "columns": int(df.shape[1]),
            "column_names": df.columns.tolist(),
            "missing_values": df.isnull().sum().to_dict(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "statistical_summary": df.describe().to_dict(),
            "head": df.head(5).to_dict(orient="records")
        }

        return summary, df

    except Exception as e:
        return {"error": str(e)}, None


# =====================================================
# IMAGE HELPER
# =====================================================

def fig_to_base64(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight", dpi=100)
    buffer.seek(0)
    image = base64.b64encode(buffer.read()).decode("utf-8")
    buffer.close()
    return image


# =====================================================
# CHART GENERATION
# =====================================================

def generate_charts(df):

    charts = {}

    try:

        numeric_cols = df.select_dtypes(include=np.number).columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns


        # Bar Chart
        if len(numeric_cols) > 0:
            fig, ax = plt.subplots(figsize=(8, 5))
            df[numeric_cols[0]].head(10).plot(kind="bar", ax=ax)
            ax.set_title(f"{numeric_cols[0]} Bar Chart")
            charts["bar_chart"] = fig_to_base64(fig)
            plt.close(fig)


        # Histogram
        if len(numeric_cols) > 0:
            fig, ax = plt.subplots(figsize=(8, 5))
            df[numeric_cols[0]].plot(kind="hist", bins=30, ax=ax)
            ax.set_title(f"{numeric_cols[0]} Histogram")
            charts["histogram"] = fig_to_base64(fig)
            plt.close(fig)


        # Correlation Heatmap
        if len(numeric_cols) > 1:
            fig, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm", ax=ax)
            charts["heatmap"] = fig_to_base64(fig)
            plt.close(fig)


        # Scatter Plot
        if len(numeric_cols) >= 2:
            fig, ax = plt.subplots(figsize=(8, 5))
            ax.scatter(df[numeric_cols[0]], df[numeric_cols[1]])
            ax.set_xlabel(numeric_cols[0])
            ax.set_ylabel(numeric_cols[1])
            charts["scatter"] = fig_to_base64(fig)
            plt.close(fig)


    except Exception as e:
        print("Chart error:", e)
        traceback.print_exc()

    return charts


# =====================================================
# OPENROUTER HELPER
# =====================================================

def get_openrouter_headers():

    api_key = settings.OPENROUTER_API_KEY

    if not api_key:
        raise Exception("OPENROUTER_API_KEY not found in environment variables")

    referer = os.environ.get(
        "RENDER_EXTERNAL_URL",
        "http://localhost:8000"
    )

    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "HTTP-Referer": referer,
        "X-Title": "AI Data Analyst"
    }


# =====================================================
# AI INSIGHTS GENERATION
# =====================================================

def get_ai_insights(summary):

    prompt = f"""
    Analyze this dataset summary and provide insights:

    {summary}

    Provide:

    - Key trends
    - Anomalies
    - Recommendations
    - Easy explanation
    """

    models = [
        "openrouter/free",
        "meta-llama/llama-3.3-70b-instruct:free",
        "deepseek/deepseek-r1:free"
    ]

    headers = get_openrouter_headers()

    for model in models:

        try:

            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json={
                    "model": model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                },
                timeout=60
            )

            if response.status_code == 200:

                data = response.json()

                return data["choices"][0]["message"]["content"]

            else:
                print("Model failed:", model, response.text)

        except Exception as e:
            print("AI error:", e)

    return "AI service temporarily unavailable."


# =====================================================
# CHAT WITH DATASET
# =====================================================

def chat_with_ai(question, summary):

    prompt = f"""
    Dataset Summary:
    {summary}

    Question:
    {question}

    Answer clearly.
    """

    headers = get_openrouter_headers()

    try:

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json={
                "model": "openrouter/free",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            },
            timeout=60
        )

        if response.status_code == 200:

            data = response.json()

            return data["choices"][0]["message"]["content"]

        else:
            return f"Error: {response.status_code}"

    except Exception as e:
        return str(e)
