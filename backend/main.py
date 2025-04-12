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
                2.Search news using specific queries: *{request.name}* AND (corruption OR sanction OR investigation) limited to major news outlets and last 5 years.
                3.Check 'UN_sanction_list.json' for exact match of *{request.name}*.
                4. Search if *{request.name}* has citizenship and primary countries of activities in any "high_risk_jurisdiction.json" country
                5. Risk Assessment Summary
                    - PEP Status: [Yes/No] - [Position/Relationship if applicable]
                    - Sanctions: [None/Listed] - [List name if applicable]
                    - Adverse Media: [Yes/No] - [Brief description if applicable]
                    - High-Risk Countries: [List countries]
                    - Overall Risk Rating: [Low/Medium/High]
                    - Risk Flags: [Brief bullet points of key issues]
                """
            )
        
            # Run the plan
            plan_run = portia.run_plan(plan)
            
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

@app.get("/search/company/{name}")
async def get_company_search(name: str):
    request = CompanySearchRequest(name=name)
    return await search_company(request)
    

@app.post("/search/company", response_model=SearchResponse)
async def search_company(request: CompanySearchRequest):
    try:
        load_dotenv(override=True)

        config = default_config()
        portia = Portia(config=config, tools = DefaultToolRegistry(config=config))

        with execution_context(end_user_id = "api_user", additional_data={"name": "individual_search" }):
            # plan = portia.plan(
            #     f"Search official registries or business datasets for *{request.name}*. "
            #     f"Identify country of registration, incorporation date, registration number, and active status. "
            #     f"Search internal JSON files for *{request.name}* in: 'UN_sanction_list.json' "
            #     #f"Search global news archives and financial reports for negative coverage related to *{request.name}*. "
            #     f"Determine countries where *{request.name}* operates, holds assets, or has entities. "
            #     #f"I dentifyCross-check these countries against 'high_risk_jurisdiction.json'. "
            
           
            # )
            plan =  portia.plan(f"""1. Search company *{request.name}* registry that it operates in
            2. Search *{request.name}* sustainability/CSR reports
            3. Search if *{request.name}* is in "UN_sanction_list.json
            4. Search if *{request.name}* operates in any "high_risk_jurisdiction.json" country
            5. List index score of all the country *{request.name}* operates in from "corruption_index.json"
            6. Risk Assessment Summary
                    - PEP Status: [Yes/No] - [Position/Relationship if applicable]
                    - Sanctions: [None/Listed] - [List name if applicable]
                    - Adverse Media: [Yes/No] - [Brief description if applicable]
                    - High-Risk Countries: [List countries]
                    - Overall Risk Rating: [Low/Medium/High]
                    - Risk Flags: [Brief bullet points of key issues]""")

            # input(f"{plan.model_dump_json(indent = 2)}") 
        
            plan_run = portia.run_plan(plan)
        
            result = json.loads(plan_run.model_dump_json())
            return JSONResponse(content = result)
        
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=500, detail=f"Error performing individual search: {str(e)}")



    

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)

