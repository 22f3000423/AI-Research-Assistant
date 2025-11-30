# AI-Research-Assistant


AI Research Assistant API
Agentic AI system using CrewAI and FastAPI.
Deploy to Railway

Push code to GitHub
Connect Railway to your repo
Add environment variable: OPENAI_API_KEY=your_key
Deploy automatically

Deploy to Render

Push code to GitHub
Create new Web Service on Render
Connect your repo
Add environment variable: OPENAI_API_KEY=your_key
Deploy

Environment Variables
OPENAI_API_KEY=your_openai_api_key
PORT=8000
API Endpoints

GET / - API info
GET /health - Health check
POST /research - Submit research topic

Example Request
bashcurl -X POST "https://your-app.railway.app/research" \
  -H "Content-Type: application/json" \
  -d '{"topic": "quantum computing", "depth": "basic"}'
Local Development
bashpip install -r requirements.txt
export OPENAI_API_KEY=your_key
uvicorn main:app --reload
