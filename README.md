# Smartfolio Python AI Service

The Smartfolio Python Service acts as the dedicated AI and Web Scraping engine for the Smartfolio platform. It is completely decoupled from the main NestJS backend and runs as a separate **FastAPI** microservice.

## 🚀 Live Deployment
- **Python API**: [https://mahrooshishaq-smartfolio-python.hf.space](https://mahrooshishaq-smartfolio-python.hf.space)
- **API Documentation**: [https://mahrooshishaq-smartfolio-python.hf.space/docs](https://mahrooshishaq-smartfolio-python.hf.space/docs) (Interactive Swagger UI)

## 🏗 Architecture & Technologies

1. **FastAPI**: Provides a high-performance asynchronous API layer.
2. **Web Scraping (Selenium)**: Automates headless browsers to fetch real-time Job postings and Course catalogs.
3. **Resume Parsing**: Uses `pdfminer.six` and specialized NLP pipelines to extract raw text and structured data from uploaded PDF resumes.
4. **LLM Integration (Groq)**: Connects to the `llama-3.3-70b-versatile` model to provide intelligent insights, resume formatting tips, and skill gap analyses.
5. **Security**: Validates an `API_KEY` passed from the NestJS backend to ensure only authorized traffic reaches the AI engine.

---

## 🛠 Features

### 1. Resume Analysis API
Receives a raw PDF file as `multipart/form-data` from the NestJS backend, extracts the text content safely in memory, and passes it to the Llama3 model to generate:
- A tailored summary of the candidate.
- Hard/Soft skills extraction.
- A score representing the resume's ATS-readiness.
- Actionable improvements for formatting and impact.

### 2. Jobs Scraper
Accepts a search query and location to dynamically launch a headless Chromium instance, scraping the latest relevant roles across various job boards.

### 3. Courses Scraper
Fetches highly relevant upskilling courses and certifications based on the user's identified skill gaps from the resume analysis.

---

## ⚙️ Environment Configuration

To run the Python service locally, set up the following environment variables in a `.env` file:

```env
# Server
PORT=7860

# Security
# This key must match the PYTHON_API_KEY set in the NestJS backend
API_KEY=your-secure-secret-key

# LLM Integrations
GROQ_API_KEY=your-groq-api-key
```

---

## 📦 Deployment (Hugging Face Docker)

This application uses a custom `Dockerfile` because it requires a complex environment with **Chromium** and **Selenium webdriver** dependencies installed natively on the Linux host.

1. Create a new Space on Hugging Face and select the **Docker** template.
2. Link your GitHub repository or push the Python code directly.
3. Hugging Face will read the provided `Dockerfile`, which:
   - Installs `python3.9`, `chromium`, and `chromium-driver`.
   - Installs the Python requirements (`pip install -r requirements.txt`).
   - Starts the Uvicorn server on port `7860` using host `0.0.0.0`.
4. Go to **Settings -> Variables and secrets** and add `API_KEY` and `GROQ_API_KEY`.
5. Your service is now live!

### Running Locally
To avoid installing Chromium natively on your local machine, running via Docker is recommended.

```bash
# Build the Docker image
docker build -t smartfolio-python .

# Run the container
docker run -p 7860:7860 --env-file .env smartfolio-python
```
