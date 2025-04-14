# SNTC (SAY NO TO CORRUPTION)
![image](https://github.com/user-attachments/assets/8986a847-0649-4cd7-a735-d1cc15fce138)

## Overview
SNTC (Say NO TO CORRUPTION) is a risk assessment tool designed to help identify corruption risks associated with individuals and companies. The application allows users to search for individuals or entities and receive comprehensive risk assessments that include sanctions checks, political exposure screening, adverse media analysis, and high-risk jurisdiction evaluation.

This tool addresses the growing need for enhanced due diligence in business relationships and investment decisions by providing quick, AI-powered risk insights that would typically require extensive manual research across multiple sources.

## Project Description
- Core functionality: Performs comprehensive risk assessments on individuals and companies to identify potential corruption risks
- Target audience: Compliance officers, due diligence professionals, financial institutions, and businesses seeking to evaluate potential partners
- Key features
  - Individual screening for political exposure, sanctions listings, and adverse media
  - Company screening for sanctions, high-risk operations, and sustainability factors
  - Risk assessment summaries with risk ratings and flags
  - Detailed step-by-step analysis of findings
- Problem statement: Manual corruption risk assessment is time-consuming, inconsistent, and often limited by access to reliable data sources
- Solution approach: Leverage Portia.ai's planning and execution capabilities to automate the search and analysis process across multiple data sources and provide structured risk assessments

## How Portia.ai Technology Was Used
- Portia Planning API: Used to create dynamic, structured plans for searching and analyzing information about individuals and companies
- Portia Execution Context: Implemented to manage user sessions and track search operations
- DefaultToolRegistry: Utilized Portia's built-in tool registry, which includes search and data retrieval functionality
- Plan-Based Approach: Each search query generates a multi-step investigation plan that is executed sequentially by Portia
- AI Analysis: Portia's AI capabilities are used to analyze search results, identify risk factors, and generate comprehensive risk assessments in a structured format

### Video Demo
[Link to video demonstration](https://www.youtube.com/watch?v=PlEDk1UHx1s&ab_channel=AdeayoOladipo)

## Technical Details
- Architecture: Client-server architecture with a FastAPI backend and HTML/JavaScript frontend
- Tech stack:
  - Backend: Python, FastAPI, Portia SDK
  - Frontend: HTML, CSS, JavaScript
- Implementation highlights
  - RESTful API for both individual and company searches
  - Dynamic plan generation based on search parameters
  - Structured output formatting for risk assessment
  - Client-side rendering of complex risk assessment results
- Scalability considerations
  - Stateless API design allows for horizontal scaling
  - Asynchronous request handling  
- Security measures

## Installation Instructions
```bash
# Clone the repository
git clone https://github.com/yourusername/sntc.git

# Navigate to the project directory
cd sntc

# Set up backend
cd backend

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
# Create a .env file with your Portia.ai and Openai API keys

# Start the backend server
python main.py

# In a separate terminal, serve the frontend
cd ../frontend
# You can use any simple HTTP server, e.g.:
python -m http.server
```

## Usage Examples

Usage Examples

1. Individual Search:
- Enter an individual's name in the search box
- Click "Search Individual"
- Review the comprehensive risk assessment, including:
  - PEP (Politically Exposed Person) status
  - Sanctions listings
  - Adverse media mentions
  - High-risk country connections
  - Overall risk rating

2. Company Search:
- Enter a company name in the search box
- Click "Search Entity."
- Review the risk assessment, including:
   - Registration information
   - Sustainability/CSR reports analysis
   - Sanctions checks
   - High-risk jurisdiction exposure
   - Corruption index scores for countries of operation

## Future Enhancements
- Integration with additional data sources
- RAG implementation for better data search capability
- Batch processing for multiple entities
- PDF report generation
- User authentication and search history
- Additional risk metrics and scoring models
- Visualization of entity relationships and risk networks

## Team Members
- Jamie Ogundiran - AI engineer (https://github.com/JReal10)
- Vanessa Nwabuoku - Software engineer (https://github.com/vaninx)
- Adeayooluwa Oladipo - Software Engineer (https://github.com/atiaen)
- Ruth Iluyomade - Software Engineer (https://github.com/ruru156)
- Safia Hasan - Governance, Risk and Compliance Expert (https://www.linkedin.com/in/safia-hassan-a68438223/)

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Special thanks to Portia.ai for providing the AI technology that powers this project
- Transparency International for corruption perception data
- Various regulatory bodies whose public data helps make this tool effective
