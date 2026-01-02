# Multi-Platform Contact Form Application

A full-stack contact form application built with React (frontend) and FastAPI (backend), integrated with Supabase for data storage. This project is configured for deployment on multiple hosting platforms: Fly.io, Railway, Vercel, Render, DigitalOcean, and Netlify.

## Features

- **Contact Form**: Submit messages with name, email, and message fields
- **Message List**: View all submitted messages in real-time
- **Supabase Integration**: Persistent data storage using Supabase
- **Multi-Platform Ready**: Pre-configured for 6 different hosting platforms
- **Responsive Design**: Modern, mobile-friendly UI

## Project Structure

```
test_hosting_project/
├── frontend/              # React application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API service layer
│   │   └── App.jsx        # Main app component
│   └── package.json
├── backend/               # FastAPI application
│   ├── main.py           # FastAPI app and routes
│   ├── database.py       # Supabase integration
│   ├── models.py         # Pydantic models
│   └── requirements.txt  # Python dependencies
├── supabase/             # Database schema
│   └── schema.sql        # SQL schema for Supabase
└── [deployment configs]  # Platform-specific configs
```

## Prerequisites

- **Node.js** (v18 or higher)
- **Python** (v3.11 or higher)
- **Supabase Account** (free tier works)
- **Git**

## Local Setup

### 1. Clone and Install Dependencies

```bash
# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies
cd ../frontend
npm install
```

### 2. Set Up Supabase

1. Create a new project at [supabase.com](https://supabase.com)
2. Go to SQL Editor and run the schema from `supabase/schema.sql`:

```sql
CREATE TABLE IF NOT EXISTS messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    message TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_messages_created_at ON messages(created_at DESC);

ALTER TABLE messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Allow all operations for testing" ON messages
    FOR ALL
    USING (true)
    WITH CHECK (true);
```

3. Get your Supabase credentials:
   - Go to Project Settings → API
   - Copy the **Project URL** (SUPABASE_URL)
   - Copy the **anon public** key (SUPABASE_KEY)

### 3. Configure Environment Variables

**Backend** (`backend/.env`):
```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_anon_key
PORT=8000
```

**Frontend** (`frontend/.env`):
```env
VITE_BACKEND_URL=http://localhost:8000
```

### 4. Run the Application

**Terminal 1 - Backend:**
```bash
cd backend
uvicorn main:app --reload
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

The app will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Deployment Guides

### Vercel

1. **Install Vercel CLI:**
   ```bash
   npm i -g vercel
   ```

2. **Deploy:**
   ```bash
   vercel
   ```

3. **Set Environment Variables:**
   - Go to Vercel Dashboard → Project Settings → Environment Variables
   - Add `SUPABASE_URL` and `SUPABASE_KEY`
   - Add `VITE_BACKEND_URL` with your deployed backend URL

4. **Configure:**
   - The `vercel.json` file handles routing
   - Backend API routes go to `/api/*`
   - Frontend routes serve the React app

**Note:** Vercel works best with serverless functions. For the backend, you may need to use Vercel's Python runtime or deploy backend separately.

### Netlify

1. **Install Netlify CLI:**
   ```bash
   npm i -g netlify-cli
   ```

2. **Install Netlify Functions dependency:**
   ```bash
   cd backend
   pip install mangum
   ```

3. **Deploy:**
   ```bash
   netlify deploy --prod
   ```

4. **Set Environment Variables:**
   - Go to Netlify Dashboard → Site Settings → Environment Variables
   - Add `SUPABASE_URL`, `SUPABASE_KEY`, and `VITE_BACKEND_URL`

**Note:** Netlify Functions require the `mangum` adapter for FastAPI. Update `netlify/functions/api.py` if needed.

### Render

1. **Create Two Services:**
   - Go to [render.com](https://render.com)
   - Create a new **Web Service** for backend
   - Create a new **Web Service** for frontend

2. **Backend Service:**
   - **Build Command:** `pip install -r backend/requirements.txt`
   - **Start Command:** `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Environment Variables:**
     - `SUPABASE_URL`
     - `SUPABASE_KEY`
     - `PORT=8000`

3. **Frontend Service:**
   - **Build Command:** `cd frontend && npm install && npm run build`
   - **Start Command:** `cd frontend && npx serve -s dist -l $PORT`
   - **Environment Variables:**
     - `VITE_BACKEND_URL` (use the backend service URL)
     - `PORT=3000`

4. **Alternative:** Use `render.yaml` for infrastructure as code:
   ```bash
   render deploy
   ```

### Railway

1. **Install Railway CLI:**
   ```bash
   npm i -g @railway/cli
   ```

2. **Login:**
   ```bash
   railway login
   ```

3. **Deploy:**
   ```bash
   railway init
   railway up
   ```

4. **Set Environment Variables:**
   ```bash
   railway variables set SUPABASE_URL=your_url
   railway variables set SUPABASE_KEY=your_key
   railway variables set PORT=8000
   ```

5. **Configure:**
   - Railway auto-detects Python projects
   - The `railway.json` and `Procfile` configure the deployment
   - For frontend, create a separate service or use Railway's static site hosting

### Fly.io

1. **Install Fly CLI:**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   ```

2. **Login:**
   ```bash
   fly auth login
   ```

3. **Initialize (Backend):**
   ```bash
   cd backend
   fly launch
   ```

4. **Set Secrets:**
   ```bash
   fly secrets set SUPABASE_URL=your_url
   fly secrets set SUPABASE_KEY=your_key
   ```

5. **Deploy:**
   ```bash
   fly deploy
   ```

6. **Frontend:**
   - Deploy frontend separately or use Fly's static site hosting
   - Update `VITE_BACKEND_URL` with your Fly.io backend URL

### DigitalOcean App Platform

1. **Create App:**
   - Go to [DigitalOcean App Platform](https://cloud.digitalocean.com/apps)
   - Click "Create App"
   - Connect your GitHub repository

2. **Configure Services:**
   - **Backend Service:**
     - Type: Web Service
     - Dockerfile: `Dockerfile` (in root)
     - Environment Variables: `SUPABASE_URL`, `SUPABASE_KEY`, `PORT=8000`
   
   - **Frontend Service:**
     - Type: Static Site
     - Build Command: `cd frontend && npm install && npm run build`
     - Output Directory: `frontend/dist`
     - Environment Variables: `VITE_BACKEND_URL` (backend service URL)

3. **Alternative:** Use `app.yaml`:
   ```bash
   doctl apps create --spec .digitalocean/app.yaml
   ```

## Environment Variables Summary

### Backend
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Your Supabase anon/service key
- `PORT` - Server port (default: 8000)

### Frontend
- `VITE_BACKEND_URL` - Backend API URL (e.g., `https://your-backend.railway.app`)

## API Endpoints

- `GET /` - Health check
- `GET /api/messages` - Retrieve all messages
- `POST /api/messages` - Submit a new message
- `GET /health` - Health check endpoint
- `GET /docs` - Interactive API documentation (Swagger UI)

## Troubleshooting

### Backend Issues

1. **Supabase Connection Error:**
   - Verify `SUPABASE_URL` and `SUPABASE_KEY` are correct
   - Check Supabase project is active
   - Verify RLS policies allow operations

2. **Port Already in Use:**
   - Change `PORT` in `.env` or use a different port
   - Kill the process using the port

### Frontend Issues

1. **Cannot Connect to Backend:**
   - Verify `VITE_BACKEND_URL` is correct
   - Check CORS settings in backend
   - Ensure backend is running

2. **Build Errors:**
   - Clear `node_modules` and reinstall: `rm -rf node_modules && npm install`
   - Check Node.js version (v18+)

### Deployment Issues

1. **Environment Variables Not Loading:**
   - Verify variables are set in platform dashboard
   - Check variable names match exactly (case-sensitive)
   - Restart/redeploy after adding variables

2. **Build Failures:**
   - Check build logs in platform dashboard
   - Verify all dependencies are in `requirements.txt` and `package.json`
   - Ensure Python/Node versions are compatible

## Development

### Running Tests

```bash
# Backend (if you add tests)
cd backend
pytest

# Frontend (if you add tests)
cd frontend
npm test
```

### Code Structure

- **Backend:** Follows FastAPI best practices with separate modules for models, database, and routes
- **Frontend:** React components with service layer for API calls
- **Database:** Supabase with Row Level Security enabled

## License

MIT License - feel free to use this project for testing hosting platforms!

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review platform-specific documentation
3. Check Supabase dashboard for database issues

---

**Happy Deploying! 🚀**

