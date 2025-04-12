from dotenv import load_dotenv
from portia import Config, Portia, PortiaToolRegistry, DefaultToolRegistry, execution_context
#from portia.examples.tools import example_tool_registry
from portia.cli import CLIExecutionHooks
from portia.open_source_tools.search_tool import SearchTool
#from registry import custom_tool_registry
from portia import (
  default_config, 
  Portia,
)

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


def company_search():
    """
    Main function to run the Portia search tool.
    """
    # business_or_individual = input("Are you doing a check on a individual or a business?: ")
    
    # if(business_or_individual) == "individual": 
    #     answer = input("Please enter an individual you would like to check:\n")
    # elif(business_or_individual) == "business":
    #     answer = input("Please enter an Business you would like to check:\n")

    # Load environment variables
    load_dotenv(override=True)
    
    name = "Shell plc"
    country = "United Kingdom"
    
    config = default_config()
    portia = Portia(config=config, tools = DefaultToolRegistry(config=config))
    country = ""
    
    with execution_context(end_user_id = "test", additional_data={"name": "test_name"}):
    
        plan = portia.plan(f'Search company *{name}* registry that it operates in'
            f'store the {country}'
            f'Search *{name}* sustainability/CSR reports'
            f'Search if *{name}* is in the json file "UK_sanction_list.json"'
            f'Search if *{name}* operates in any "high_risk_jurisdiction.json" country'
            f'From "corruption_index.json" List index score of all the country {name} operates in')
        
        input(f"{plan.model_dump_json(indent = 2)}") 
        
        plan_run = portia.run_plan(plan)
        print(f"{plan_run.model_dump_json(indent = 2)}")  

def main():
    Individual_Search("GHULAM NABI Mohammed Omar")

def Individual_Search(individual_name):
    
    load_dotenv(override=True)
    
    config = default_config()
    portia = Portia(config=config, tools = DefaultToolRegistry(config=config))

    with execution_context(end_user_id = "test_individual", additional_data={"name": "test_individual"}):

        plan = portia.plan(f"**Web Footprint Analysis:** Conduct broad web searches for *{individual_name}*. Identify biographical details, current and former prominent positions (especially in government, judiciary, military, state-owned enterprises, or international organizations), significant business affiliations, and known close associates or family members who might also be PEPs. Utilize search operators to refine results towards official sources, biographical entries, and corporate registries where applicable"
        f"**Professional Network Scan (e.g., LinkedIn via Web Search):** Search professional networking platforms accessible via the web for *{individual_name}*'s profile. Extract information about their career trajectory, current/past job titles, seniority levels, connections, and listed organizations. Pay attention to roles that align with PEP definitions."
        f"**Adverse Media Screening:** Search reputable global and local news archives and websites for *{individual_name}*. Focus specifically on identifying negative news articles or reports related to: * Allegations or convictions of financial crime (fraud, bribery, corruption, money laundering, terrorist financing). * Involvement in significant controversies, scandals, or investigations. * Sanctions, regulatory warnings, or disqualifications. * Keywords: *{individual_name}* AND (investigation OR fraud OR bribery OR corruption OR money laundering OR scandal OR controversy OR sanction OR lawsuit OR charges OR allegations OR negative news)."
        f"**Sanctions List Check:** Query the internal 'UK_sanction_list.json' file to determine if *{individual_name}* is explicitly listed."
        f"**Sanctions List Check:** Query the internal 'EU_sanction_list.json' file to determine if *{individual_name}* is explicitly listed."
        f"**Sanctions List Check:** Query the internal 'UN_sanction_list.json' file to determine if *{individual_name}* is explicitly listed."
        f"**Sanctions List Check:** Query the internal 'US_sanction_list.json' file to determine if *{individual_name}* is explicitly listed."
        f"**High-Risk Jurisdiction Exposure:** a.Based on information gathered in Phase 1, identify countries where *{individual_name}* holds citizenship, residency, has significant business operations, or holds/held prominent positions. b.Cross-reference these countries against the 'high_risk_jurisdiction.json' list. Note any matches. c.For relevant countries identified, retrieve their corruption perception scores/rankings from 'corruption_index.json'."                    
            )
        
        input(f"{plan.model_dump_json(indent = 2)}") 
        
        plan_run = portia.run_plan(plan)
        
        return(f"{plan_run.model_dump_json(indent = 2)}")

if __name__ == "__main__":
    main()