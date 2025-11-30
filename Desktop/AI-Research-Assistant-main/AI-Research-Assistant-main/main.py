from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
import os
from typing import Optional

load_dotenv()

app = FastAPI(
    title="AI Research Assistant API",
    description="Agentic AI system for conducting research using CrewAI",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class ResearchRequest(BaseModel):
    topic: str
    depth: Optional[str] = "comprehensive"

# Response model
class ResearchResponse(BaseModel):
    status: str
    topic: str
    result: str

# Initialize LLM
def get_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set")
    return ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)

@app.get("/")
async def root():
    return {
        "message": "AI Research Assistant API",
        "version": "1.0.0",
        "endpoints": {
            "health": "/health",
            "research": "/research (POST)"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/research", response_model=ResearchResponse)
async def conduct_research(request: ResearchRequest):
    try:
        print(f"\n Starting research on: {request.topic}")
        llm = get_llm()
        print(" LLM initialized successfully")
        
        # Define researcher agent
        researcher = Agent(
            role="Senior Research Analyst",
            goal=f"Conduct thorough research on {request.topic}",
            backstory="Expert analyst with years of experience in research and data analysis",
            verbose=True,
            llm=llm,
            allow_delegation=False
        )
        
        # Define writer agent
        writer = Agent(
            role="Technical Writer",
            goal="Create comprehensive and clear research reports",
            backstory="Skilled writer who excels at synthesizing complex information",
            verbose=True,
            llm=llm,
            allow_delegation=False
        )
        
        print(" Agents created")
        
        # Define tasks
        research_task = Task(
            description=f"Research {request.topic} in {request.depth} detail. Gather key facts, trends, and insights.",
            agent=researcher,
            expected_output="Detailed research findings with key insights"
        )
        
        write_task = Task(
            description=f"Write a comprehensive report on {request.topic} based on the research findings.",
            agent=writer,
            expected_output="Well-structured research report"
        )
        
        print(" Tasks created")
        
        # Create crew
        crew = Crew(
            agents=[researcher, writer],
            tasks=[research_task, write_task],
            process=Process.sequential,
            verbose=True
        )
        
        print(" Crew created - starting kickoff")
        
        # Execute research
        result = crew.kickoff()
        
        print("Research completed successfully")
        
        return ResearchResponse(
            status="success",
            topic=request.topic,
            result=str(result)
        )
        
    except Exception as e:
        error_msg = str(e)
        print(f" Error during research: {error_msg}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=error_msg)

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    print(f"\n AI Research Assistant API is running!")
    print(f" Access at: http://localhost:{port}")
    print(f" API Docs: http://localhost:{port}/docs\n")
    uvicorn.run(app, host="127.0.0.1", port=port)