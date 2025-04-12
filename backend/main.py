from dotenv import load_dotenv
from portia import Config, Portia, PortiaToolRegistry, DefaultToolRegistry, execution_context
#from portia.examples.tools import example_tool_registry
from portia.cli import CLIExecutionHooks
from portia.open_source_tools.search_tool import SearchTool
#from registry import custom_tool_registry
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from typing import Optional,Dict, Any

from portia import (
  default_config, 
  Portia,
)

import json

from fastapi import FastAPI

app = FastAPI(
    title = "Portia Search API",
    description="API for performing company and individual search using Portia",
    version = "1.0.0"
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Define request and response models
class CompanySearchRequest(BaseModel):
    name: str
    country: Optional[str] = ""

class IndividualSearchRequest(BaseModel):
    name: str
    
class SearchResponse(BaseModel):
    result: Dict[str, Any]

@app.get("/")
async def root():
    """Root endpoint that returns a welcome message."""
    return {"message": "Welcome to Portia Search API"}

@app.post("/search/company", response_model=SearchResponse)
async def search_company(request: CompanySearchRequest):
    
    return 0

@app.post("/search/individual", response_model=SearchResponse)
async def search_individual(request: IndividualSearchRequest):
    """
    Perform a comprehensive search on an individual.
    
    - Web footprint analysis
    - Professional network scan
    - Adverse media screening
    - Checks against multiple sanctions lists (UK, EU, UN, US)
    - High-risk jurisdiction exposure assessment
    """
    try:
        # Load environment variables
        load_dotenv(override=True)
        
        # Configure Portia
        config = default_config()
        portia = Portia(config=config, tools=DefaultToolRegistry(config=config))
        
        with execution_context(end_user_id="api_user", additional_data={"name": "individual_search"}):
            # Create plan
            plan = portia.plan(
                f"""
                1.Search web for *{request.name}* focusing on current/recent government, judicial, military, state-enterprise, or international organization roles.
                f"Search news using specific queries: *{request.name}* AND (corruption OR sanction OR investigation) limited to major news outlets and last 5 years."
                3.Check 'UN_sanction_list.json' for exact match of *{request.name}*.
                4. Search if *{request.name}* has citizenship and primary countries of activities in any "high_risk_jurisdiction.json" country'
                5.Briefly report PEP indicators, adverse media hits (BBC), anction status, key countries, and flag if high-risk/PEP.
                """
            )
        
            # Run the plan
            plan_run = portia.run_plan(plan)
            print(f"{plan.model_dump_json(indent = 2)}")
            
            # Return the results
            result = json.loads(plan_run.model_dump_json())
            return JSONResponse(content = result)
            
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f"Error performing individual search: {str(e)}")

@app.get("/search/individual/{name}")
async def get_individual_search(name: str):
    """Simple GET endpoint for individual searches (for testing purposes)"""
    request = IndividualSearchRequest(name=name)
    return await search_individual(request)

@app.get("/search/company/")
async def get_company_search(
    name: str = Query(..., description="Company name to search for"),
    country: Optional[str] = Query("", description="Country of operation")
):
    """Simple GET endpoint for company searches (for testing purposes)"""
    request = CompanySearchRequest(name=name, country=country)
    return await search_company(request)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)