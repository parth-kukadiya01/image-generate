# Jewelry Image Generator App

This is a full-stack application for generating premium jewelry product and lifestyle images from a single shot, using Google's Gemini AI.

## Requirements

- Node.js (v18+)
- Python 3.10+
- Google Gemini API Key

## Project Structure

- `frontend/`: React + Vite + TailwindCSS application.
- `backend/`: FastAPI + Python application.

---

## How to Run the Application

You will need to run both the frontend and the backend servers simultaneously in separate terminal windows.

### 1. Start the Backend Server (FastAPI)

1. Open a new terminal.
2. Navigate to the backend directory:
   ```bash
   cd backend
   ```
3. Set up the Python virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install fastapi uvicorn python-multipart google-genai
   ```
4. Start the server (it will run on port 8000):
   ```bash
   uvicorn main:app --reload --port 8000
   ```

### 2. Start the Frontend Server (React)

1. Open a new, separate terminal window.
2. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
3. Install the Node.js dependencies:
   ```bash
   npm install
   ```
4. Start the Vite development server (it will run on port 5173):
   ```bash
   npm run dev
   ```

### 3. Use the App

Open your browser and navigate to the frontend URL (usually `http://localhost:5173`). 
You can now upload images, select a jewelry category, and generate results! The generated images will be neatly saved inside the `backend/outputs/` directory.

---

## Troubleshooting

- **API Key Error**: Ensure `GEMINI_API_KEY` is set correctly in the environment before starting the backend, or edit the default key in `backend/generator.py`.
- **CORS Errors**: Ensure the backend is running on `http://localhost:8000`. The frontend is hard-coded to communicate with this specific port.
