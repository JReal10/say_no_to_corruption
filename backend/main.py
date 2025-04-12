from dotenv import load_dotenv
from portia import Config, Portia, PortiaToolRegistry, DefaultToolRegistry, execution_context
#from portia.examples.tools import example_tool_registry
from portia.cli import CLIExecutionHooks
from portia.open_source_tools.search_tool import SearchTool
#from registry import custom_tool_registry
from fastapi import FastAPI, Query, HTTPException
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

# def Individual_Search(individual_name):
    
#     load_dotenv(override=True)
    
#     config = default_config()
#     portia = Portia(config=config, tools = DefaultToolRegistry(config=config))

#     with execution_context(end_user_id = "test_individual", additional_data={"name": "test_individual"}):

#         plan = portia.plan(f"**Web Footprint Analysis:** Conduct broad web searches for *{individual_name}*. Identify biographical details, current and former prominent positions (especially in government, judiciary, military, state-owned enterprises, or international organizations), significant business affiliations, and known close associates or family members who might also be PEPs. Utilize search operators to refine results towards official sources, biographical entries, and corporate registries where applicable"
#         f"**Professional Network Scan (e.g., LinkedIn via Web Search):** Search professional networking platforms accessible via the web for *{individual_name}*'s profile. Extract information about their career trajectory, current/past job titles, seniority levels, connections, and listed organizations. Pay attention to roles that align with PEP definitions."
#         f"**Adverse Media Screening:** Search reputable global and local news archives and websites for *{individual_name}*. Focus specifically on identifying negative news articles or reports related to: * Allegations or convictions of financial crime (fraud, bribery, corruption, money laundering, terrorist financing). * Involvement in significant controversies, scandals, or investigations. * Sanctions, regulatory warnings, or disqualifications. * Keywords: *{individual_name}* AND (investigation OR fraud OR bribery OR corruption OR money laundering OR scandal OR controversy OR sanction OR lawsuit OR charges OR allegations OR negative news)."
#         f"**Sanctions List Check:** Query the internal 'UK_sanction_list.json' file to determine if *{individual_name}* is explicitly listed."
#         #f"**Sanctions List Check:** Query the internal 'EU_sanction_list.json' file to determine if *{individual_name}* is explicitly listed."
#         f"**Sanctions List Check:** Query the internal 'UN_sanction_list.json' file to determine if *{individual_name}* is explicitly listed."
#         f"**Sanctions List Check:** Query the internal 'US_sanction_list.json' file to determine if *{individual_name}* is explicitly listed."
#         f"**High-Risk Jurisdiction Exposure:** a.Based on information gathered in Phase 1, identify countries where *{individual_name}* holds citizenship, residency, has significant business operations, or holds/held prominent positions. b.Cross-reference these countries against the 'high_risk_jurisdiction.json' list. Note any matches. c.For relevant countries identified, retrieve their corruption perception scores/rankings from 'corruption_index.json'."                    
#             )
        
#         input(f"{plan.model_dump_json(indent = 2)}") 
        
#         plan_run = portia.run_plan(plan)
        
#         return(f"{plan_run.model_dump_json(indent = 2)}")

# def company_search():
#     """
#     Main function to run the Portia search tool.
#     """
#     # business_or_individual = input("Are you doing a check on a individual or a business?: ")
    
#     # if(business_or_individual) == "individual": 
#     #     answer = input("Please enter an individual you would like to check:\n")
#     # elif(business_or_individual) == "business":
#     #     answer = input("Please enter an Business you would like to check:\n")

#     # Load environment variables
#     load_dotenv(override=True)
    
#     name = "Shell plc"
#     country = "United Kingdom"
    
#     config = default_config()
#     portia = Portia(config=config, tools = DefaultToolRegistry(config=config))
#     country = ""
    
#     with execution_context(end_user_id = "test", additional_data={"name": "test_name"}):
    
#         plan = portia.plan(f'Search company *{name}* registry that it operates in'
#             f'store the {country}'
#             f'Search *{name}* sustainability/CSR reports'
#             f'Search if *{name}* is in the json file "UK_sanction_list.json"'
#             f'Search if *{name}* operates in any "high_risk_jurisdiction.json" country'
#             f'From "corruption_index.json" List index score of all the country {name} operates in')
        
#         input(f"{plan.model_dump_json(indent = 2)}") 
        
#         plan_run = portia.run_plan(plan)
#         print(f"{plan_run.model_dump_json(indent = 2)}")  

# Alternative endpoint with GET method for simpler testing