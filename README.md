# AI Research Notes Summarizer

A full-stack application to summarize text and PDFs, extract keywords, and generate insights.

## Project Structure

- `backend/`: FastAPI application (Python)
- `frontend/`: Next.js application (TypeScript/React)
 **Frontend GitHub Repository:** https://github.com/Maxw311nyimbili/paper_summary_frontend
## Local Development

### Backend

1. Navigate to `backend`:
   ```bash
   cd backend
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the server:
   ```bash
   uvicorn main:app --reload
   ```


### Frontend

1. Navigate to `frontend`:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```


## Deployment

### Backend (Render / Railway)

1. Push this repository to GitHub.
2. Create a new Web Service on Render or Railway.
3. Connect your GitHub repository.
4. Set the **Root Directory** to `backend`.
5. Set the **Build Command** to `pip install -r requirements.txt`.
6. Set the **Start Command** to `uvicorn main:app --host 0.0.0.0 --port $PORT`.
7. Deploy!

### Frontend (Vercel)

1. Push this repository to GitHub.
2. Import the project in Vercel.
3. Set the **Root Directory** to `frontend`.
4. Configure Environment Variables:
   - `NEXT_PUBLIC_API_URL`: The URL of your deployed backend (e.g., `https://your-backend.onrender.com`).
5. Deploy!
