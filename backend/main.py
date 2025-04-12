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


def main():
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
    
    with execution_context(end_user_id = "test", additional_data={"name": "test_name"}):
    
        plan = portia.plan(f'Search company *{name}* registry in {country}' 
            f'Search *{name}* sustainability/CSR reports'
            f'Search if *{name}* is in the json file "UK_sanction_list.json"'
            f'Search if *{name}* operates in any "high_risk_jurisdiction.json" country')
        
        input(f"{plan.model_dump_json(indent = 2)}") 
        
        plan_run = portia.run_plan(plan)
        print(f"{plan_run.model_dump_json(indent = 2)}")  

if __name__ == "__main__":
    main()