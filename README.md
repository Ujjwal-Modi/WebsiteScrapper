# 🚀 AI-Powered Prospect Research Agent

[![Frontend](https://img.shields.io/badge/Frontend-Live-success)](https://website-scrapper-umber.vercel.app/)
[![React](https://img.shields.io/badge/React.js-Frontend-61DAFB)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python-green)](https://fastapi.tiangolo.com/)
[![Groq](https://img.shields.io/badge/Groq-LLM-orange)](https://groq.com/)

An AI-powered web application that automates company research by scraping business websites, extracting key information, and generating structured prospect profiles using Large Language Models (LLMs).

---

## 🌐 Live Demo

### Frontend

🔗 **Live Application:**
https://website-scrapper-umber.vercel.app/

---

## ✨ Features

* 🌍 Company website scraping and content extraction
* 🔎 Intelligent page discovery (About, Contact, Services, Products, etc.)
* 🗺️ Sitemap.xml support for enhanced website coverage
* 📧 Email extraction
* 📱 Phone number extraction
* 🤖 AI-powered company profiling using Groq LLMs
* 🎯 Target customer identification
* ⚡ Business pain point analysis
* 💬 Personalized outreach opener generation
* 🔗 REST API backend with FastAPI
* 🎨 Interactive frontend built with React
* 💾 Result persistence using JSON storage
* ☁️ Full cloud deployment with Render and Vercel

---

## 🏗️ Project Architecture

```text
User Input (Company URL)
          │
          ▼
React Frontend
          │
          ▼
FastAPI Backend
          │
          ▼
Website Scraper
          │
          ▼
Content Extraction
          │
          ▼
Groq LLM Analysis
          │
          ▼
Structured Company Profile
          │
          ▼
Results Storage & Display
```

---

## 🛠️ Tech Stack

### Frontend

* React.js
* JavaScript
* Axios
* CSS

### Backend

* FastAPI
* Python
* REST APIs

### AI & Data Processing

* Groq API
* Llama 3.3 70B Versatile
* Prompt Engineering
* RapidFuzz

### Web Scraping

* Requests
* BeautifulSoup4
* XML Sitemap Parsing
* HTML Parsing

### Deployment & Tools

* Render (Backend)
* Vercel (Frontend)
* Git
* GitHub

---

## 📸 Application Workflow

1. Enter a company name and website URL.
2. Click **Enrich**.
3. The system scrapes the company website.
4. AI analyzes the content.
5. Generates:

   * Company Profile
   * Core Services
   * Target Customers
   * Contact Information
   * Business Pain Points
   * Personalized Outreach Opener
6. View all enriched companies using **Show All Results**.

---

## 🔌 API Endpoints

### GET /

Health Check Endpoint

#### Response

```json
{
  "message": "Backend Working"
}
```

---

### POST /enrich

Generate a structured company profile.

#### Request

```json
{
  "website_name": "OpenAI",
  "url": "https://openai.com"
}
```

---

### GET /results

Returns all previously enriched company profiles.

---

## 📄 Example Output

```json
{
  "website_name": "OpenAI",
  "company_name": "OpenAI",
  "address": "",
  "mobile_number": "",
  "mail": [],
  "core_service": "Artificial Intelligence Research and Products",
  "target_customer": "Businesses and Developers",
  "probable_pain_point": "Need for advanced AI solutions and automation",
  "outreach_opener": "I noticed OpenAI is actively advancing AI adoption across industries..."
}
```

---

## ⚙️ Local Setup

### Clone Repository

```bash
git clone https://github.com/Ujjwal-Modi/WebsiteScrapper
cd WebsiteScrapper
```

---

### Backend Setup

```bash
cd Backend

pip install -r requirements.txt

python -m uvicorn main:app --reload
```

Backend runs at:

```text
http://127.0.0.1:8000
```

Swagger Docs:

```text
http://127.0.0.1:8000/docs
```

---

### Frontend Setup

```bash
cd Frontend

npm install

npm run dev
```

Frontend runs at:

```text
http://localhost:5173
```

---

## 🔐 Environment Variables

Create a `.env` file inside the Backend folder:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## 📂 Project Structure

```text
WebsiteScrapper/
│
├── Backend/
│   ├── main.py
│   ├── scraper.py
│   ├── requirements.txt
│   ├── results.json
│   └── .env
│
├── Frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## 🚀 Future Improvements

* MongoDB / PostgreSQL integration
* User Authentication
* Bulk URL Processing
* CSV / Excel Export
* CRM Integration
* Lead Scoring Engine
* AI Email Generation
* Outreach Automation
* Company Comparison Dashboard

---

## 👨‍💻 Author

### Ujjwal Modi

B.Tech Computer Science Engineering | KIIT University

Passionate about:

* Artificial Intelligence
* Machine Learning
* Full Stack Development
* Large Language Models
* Building Real-World Products

### Connect With Me

* LinkedIn: https://www.linkedin.com/in/ujjawalmodi/
* GitHub: https://github.com/Ujjwal-Modi

---

⭐ If you found this project interesting, consider giving it a star!
