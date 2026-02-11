OVERVIEW

README = """
# AI Data Analyst Web Application

Live Demo: https://ai-data-analyst-n54v.onrender.com

An AI-powered Django web application that allows users to upload CSV files, automatically generate statistical analysis and visualizations, and interact with their data using natural language via OpenRouter LLM integration.

---

# Live Website

Access the deployed application here:

https://ai-data-analyst-n54v.onrender.com

---

# Screenshot

Add your screenshot inside docs/screenshot.png and GitHub will display it:

![AI Data Analyst Screenshot](docs/image1.png)

---

# Features

• CSV Upload and Analysis  
Upload any CSV file and instantly analyze it  

• Automated Data Summary  
Displays:
- Total rows and columns  
- Column names  
- Sample data preview  

• Automatic Visualizations  
Generates:
- Histograms  
- Bar charts  
- Correlation heatmaps  
- Distribution plots  

• AI-Generated Insights  
Uses OpenRouter API to generate plain-English insights  

• Chat with Your Data  
Ask questions like:
- What is the average salary?
- Which category has highest sales?
- Find trends in the data

• Production Deployment  
Hosted on Render  

---

# Tech Stack

Backend
- Django
- Django REST Framework
- Pandas
- NumPy
- Matplotlib
- Seaborn

AI Integration
- OpenRouter API

Frontend
- HTML
- Bootstrap 5
- JavaScript

Deployment
- Render
- Gunicorn
- WhiteNoise

---

# Installation

Clone repository:

git clone https://github.com/VatsalNegi/ai-data-analyst.git

cd ai-data-analyst

Install dependencies:

pip install -r requirements.txt

---

# Environment Variables

Create .env file:

OPENROUTER_API_KEY=your_openrouter_api_key_here
SECRET_KEY=your_secret_key_here
DEBUG=True

Get API key from:
https://openrouter.ai/keys

---

# Run Locally

python manage.py migrate

python manage.py runserver

Open browser:
http://127.0.0.1:8000

---

# API Endpoints

Upload dataset
POST /upload/

Generate charts
GET /charts/<dataset_id>/

Generate insights
GET /insights/<dataset_id>/

Chat with data
POST /chat/<dataset_id>/

---

# Deployment

Live URL:
https://ai-data-analyst-n54v.onrender.com

---

# Author

Vatsal Negi

GitHub:
https://github.com/VatsalNegi

LinkedIn:
https://www.linkedin.com/in/vatsal-negi-3624a12b6/

---

# License

MIT License
"""

# This will create README.md automatically
with open("README.md", "w", encoding="utf-8") as f:
    f.write(README)

print("README.md generated successfully!")
