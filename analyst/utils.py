import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for server-side rendering
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64
import os
import requests
import json
from django.conf import settings

def analyze_csv(file_path):
    """
    Reads a CSV file and returns a summary of the data.
    """
    try:
        df = pd.read_csv(file_path)
        
        summary = {
            "rows": df.shape[0],
            "columns": df.shape[1],
            "column_names": df.columns.tolist(),
            "missing_values": df.isnull().sum().to_dict(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "statistical_summary": df.describe().to_dict(),
            "head": df.head(5).to_dict(orient='records')
        }
        return summary, df
    except Exception as e:
        return {"error": str(e)}, None

def generate_charts(df):
    """
    Generates comprehensive charts from the dataframe and returns them as base64 strings.
    """
    charts = {}
    
    try:
        numerical_cols = df.select_dtypes(include=['number']).columns
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns
        
        # 1. Bar Chart - First numerical column
        if len(numerical_cols) > 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            data_to_plot = df[numerical_cols[0]].head(10)
            ax.bar(range(len(data_to_plot)), data_to_plot, color='#667eea', edgecolor='black', alpha=0.8)
            ax.set_title(f'Bar Chart of {numerical_cols[0]} (First 10 rows)', fontsize=14, fontweight='bold')
            ax.set_xlabel('Index', fontsize=12)
            ax.set_ylabel(numerical_cols[0], fontsize=12)
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            charts['bar_chart'] = get_image_base64(fig)
            plt.close(fig)

        # 2. Histogram with KDE
        if len(numerical_cols) > 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            data = df[numerical_cols[0]].dropna()
            ax.hist(data, bins=30, color='#4facfe', edgecolor='black', alpha=0.7, density=True)
            # Add KDE line
            from scipy import stats
            kde = stats.gaussian_kde(data)
            x_range = np.linspace(data.min(), data.max(), 100)
            ax.plot(x_range, kde(x_range), 'r-', linewidth=2, label='KDE')
            ax.set_title(f'Histogram with KDE - {numerical_cols[0]}', fontsize=14, fontweight='bold')
            ax.set_xlabel(numerical_cols[0], fontsize=12)
            ax.set_ylabel('Density', fontsize=12)
            ax.legend()
            ax.grid(alpha=0.3)
            plt.tight_layout()
            charts['histogram'] = get_image_base64(fig)
            plt.close(fig)

        # 3. Box Plot - All numerical columns
        if len(numerical_cols) > 0:
            fig, ax = plt.subplots(figsize=(12, 6))
            df[numerical_cols[:5]].boxplot(ax=ax, patch_artist=True)
            ax.set_title('Box Plot - Distribution Analysis', fontsize=14, fontweight='bold')
            ax.set_ylabel('Values', fontsize=12)
            ax.grid(alpha=0.3)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            charts['box_plot'] = get_image_base64(fig)
            plt.close(fig)

        # 4. Correlation Heatmap
        if len(numerical_cols) > 1:
            fig, ax = plt.subplots(figsize=(10, 8))
            correlation = df[numerical_cols].corr()
            sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax, fmt='.2f', 
                       linewidths=0.5, cbar_kws={'shrink': 0.8}, center=0)
            ax.set_title('Correlation Heatmap', fontsize=14, fontweight='bold')
            plt.tight_layout()
            charts['heatmap'] = get_image_base64(fig)
            plt.close(fig)

        # 5. Scatter Plot - First two numerical columns
        if len(numerical_cols) >= 2:
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.scatter(df[numerical_cols[0]], df[numerical_cols[1]], 
                      alpha=0.6, c='#667eea', edgecolors='black', s=50)
            ax.set_title(f'Scatter Plot: {numerical_cols[0]} vs {numerical_cols[1]}', 
                        fontsize=14, fontweight='bold')
            ax.set_xlabel(numerical_cols[0], fontsize=12)
            ax.set_ylabel(numerical_cols[1], fontsize=12)
            ax.grid(alpha=0.3)
            plt.tight_layout()
            charts['scatter_plot'] = get_image_base64(fig)
            plt.close(fig)

        # 6. Violin Plot - First numerical column
        if len(numerical_cols) > 0:
            fig, ax = plt.subplots(figsize=(10, 6))
            parts = ax.violinplot([df[numerical_cols[0]].dropna()], positions=[0], 
                                 showmeans=True, showmedians=True)
            for pc in parts['bodies']:
                pc.set_facecolor('#f093fb')
                pc.set_alpha(0.7)
            ax.set_title(f'Violin Plot - {numerical_cols[0]}', fontsize=14, fontweight='bold')
            ax.set_ylabel(numerical_cols[0], fontsize=12)
            ax.set_xticks([0])
            ax.set_xticklabels([numerical_cols[0]])
            ax.grid(alpha=0.3)
            plt.tight_layout()
            charts['violin_plot'] = get_image_base64(fig)
            plt.close(fig)

        # 7. Pie Chart - First categorical column (if exists)
        if len(categorical_cols) > 0:
            fig, ax = plt.subplots(figsize=(10, 8))
            value_counts = df[categorical_cols[0]].value_counts().head(10)
            colors = plt.cm.Set3(range(len(value_counts)))
            ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', 
                  startangle=90, colors=colors, textprops={'fontsize': 10})
            ax.set_title(f'Distribution of {categorical_cols[0]} (Top 10)', 
                        fontsize=14, fontweight='bold')
            plt.tight_layout()
            charts['pie_chart'] = get_image_base64(fig)
            plt.close(fig)

        # 8. Line Plot - Trend over index
        if len(numerical_cols) > 0:
            fig, ax = plt.subplots(figsize=(12, 6))
            for i, col in enumerate(numerical_cols[:3]):  # Plot first 3 numerical columns
                ax.plot(df.index[:50], df[col].head(50), marker='o', 
                       label=col, linewidth=2, markersize=4)
            ax.set_title('Trend Analysis (First 50 rows)', fontsize=14, fontweight='bold')
            ax.set_xlabel('Index', fontsize=12)
            ax.set_ylabel('Values', fontsize=12)
            ax.legend()
            ax.grid(alpha=0.3)
            plt.tight_layout()
            charts['line_plot'] = get_image_base64(fig)
            plt.close(fig)

        # 9. Count Plot - Categorical distribution
        if len(categorical_cols) > 0:
            fig, ax = plt.subplots(figsize=(12, 6))
            value_counts = df[categorical_cols[0]].value_counts().head(10)
            ax.bar(range(len(value_counts)), value_counts.values, 
                  color='#fa709a', edgecolor='black', alpha=0.8)
            ax.set_xticks(range(len(value_counts)))
            ax.set_xticklabels(value_counts.index, rotation=45, ha='right')
            ax.set_title(f'Count Plot - {categorical_cols[0]} (Top 10)', 
                        fontsize=14, fontweight='bold')
            ax.set_ylabel('Count', fontsize=12)
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            charts['count_plot'] = get_image_base64(fig)
            plt.close(fig)

        # 10. Pair Plot Matrix (for first 3 numerical columns)
        if len(numerical_cols) >= 2:
            num_cols_subset = numerical_cols[:min(3, len(numerical_cols))]
            fig, axes = plt.subplots(len(num_cols_subset), len(num_cols_subset), 
                                    figsize=(12, 12))
            for i, col1 in enumerate(num_cols_subset):
                for j, col2 in enumerate(num_cols_subset):
                    ax = axes[i, j] if len(num_cols_subset) > 1 else axes
                    if i == j:
                        # Diagonal: histogram
                        ax.hist(df[col1].dropna(), bins=20, color='#4facfe', 
                               edgecolor='black', alpha=0.7)
                    else:
                        # Off-diagonal: scatter
                        ax.scatter(df[col2], df[col1], alpha=0.5, s=20, c='#667eea')
                    
                    if i == len(num_cols_subset) - 1:
                        ax.set_xlabel(col2, fontsize=10)
                    if j == 0:
                        ax.set_ylabel(col1, fontsize=10)
            
            plt.suptitle('Pair Plot Matrix', fontsize=14, fontweight='bold', y=0.995)
            plt.tight_layout()
            charts['pair_plot'] = get_image_base64(fig)
            plt.close(fig)
            
    except Exception as e:
        print(f"Error generating charts: {str(e)}")
        import traceback
        traceback.print_exc()
        
    return charts

def get_image_base64(fig):
    """
    Helper to convert plot to base64 string.
    """
    buffer = io.BytesIO()
    fig.savefig(buffer, format='png', dpi=100, bbox_inches='tight')
    buffer.seek(0)
    image_png = buffer.getvalue()
    buffer.close()
    graphic = base64.b64encode(image_png)
    return graphic.decode('utf-8')

def get_gemini_insights(summary):
    """
    Generates insights using OpenRouter API with 2026 free models.
    """
    # Updated list of working free models as of 2026
    models_to_try = [
        "openrouter/free",  # Auto-selects best free model
        "meta-llama/llama-3.3-70b-instruct:free",
        "deepseek/deepseek-r1:free",
        "openai/gpt-oss-120b:free",
        "nvidia/nemotron-3-nano-30b-a3b:free"
    ]
    
    prompt = f"""
    Analyze the following dataset summary and provide insights:
    
    Dataset Summary:
    {summary}
    
    Please provide:
    1. Key Trends
    2. Anomalies (if any)
    3. Recommendations based on the data
    4. Summary of the data distribution
    
    Keep it concise and easy to understand for a non-technical user.
    """
    
    last_error = None
    for model in models_to_try:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "AI Data Analyst"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
            else:
                last_error = f"Model {model}: HTTP {response.status_code}"
                continue
            
        except Exception as e:
            last_error = str(e)
            continue
    
    # If all models fail, return helpful error
    return f"⚠️ AI service temporarily unavailable. Last error: {last_error}. Please try again in a moment."

def chat_with_gemini(question, context_summary):
    """
    Answers user questions based on the dataset context with 2026 free models.
    """
    # Updated list of working free models as of 2026
    models_to_try = [
        "openrouter/free",  # Auto-selects best free model
        "meta-llama/llama-3.3-70b-instruct:free",
        "deepseek/deepseek-r1:free",
        "openai/gpt-oss-120b:free",
        "nvidia/nemotron-3-nano-30b-a3b:free"
    ]
    
    prompt = f"""
    You are a data analyst. Answer the user's question based on the following dataset summary.
    
    Dataset Summary:
    {context_summary}
    
    User Question: {question}
    
    Answer:
    """
    
    last_error = None
    for model in models_to_try:
        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "http://localhost:8000",
                    "X-Title": "AI Data Analyst"
                },
                json={
                    "model": model,
                    "messages": [
                        {"role": "user", "content": prompt}
                    ]
                },
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    return result['choices'][0]['message']['content']
            else:
                last_error = f"Model {model}: HTTP {response.status_code}"
                continue
            
        except Exception as e:
            last_error = str(e)
            continue
    
    # If all models fail, return helpful error
    return f"⚠️ AI service temporarily unavailable. Last error: {last_error}. Please try again in a moment."
