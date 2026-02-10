# AI Data Analyst Web Application

A Django-based web application that allows users to upload CSV files, automatically generates statistical analysis and visualization charts, and provides an AI-powered Q&A interface using Google Gemini.

## Features

- **CSV Upload**: Upload any CSV file for instant analysis.
- **Data Summary**: View rows, columns, missing values, and data types.
- **Auto Visualization**: Automatically generates Bar Charts, Histograms, and Correlation Heatmaps.
- **AI Insights**: Get plain English insights about your data from Google Gemini.
- **Chat with Data**: Ask questions about your dataset and get AI-generated answers.

## Prerequisites

- Python 3.8+
- Google Gemini API Key

## Setup Instructions

1.  **Clone the repository** (or navigate to the project folder).

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Environment Configuration**:
    Create a `.env` file in the root directory (`ai_data_analyst/`) and add your Gemini API Key:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

4.  **Apply Migrations**:
    ```bash
    python manage.py migrate
    ```

5.  **Run the Server**:
    ```bash
    python manage.py runserver
    ```

6.  **Access the App**:
    Open your browser and go to `http://127.0.0.1:8000/`.

## Project Structure

- `analyst/`: Main application app.
    - `models.py`: Defines the `Dataset` model.
    - `utils.py`: Contains logic for Pandas analysis, chart generation, and Gemini API calls.
    - `views.py`: API endpoints for upload, analysis, and chat.
    - `templates/dashboard.html`: The frontend interface.
- `config/`: Django project settings.
- `media/`: Stores uploaded CSVs and generated charts.

## Usage

1.  Upload a CSV file (e.g., `titanic.csv`).
2.  Wait for the analysis to complete.
3.  View the summary statistics and sample data.
4.  Click "Generate Charts" to see visualizations.
5.  Click "Get AI Insights" to read an AI-generated summary.
6.  Use the Chat interface to ask specific questions like "What is the average age?" or "Find the trend in sales".
