from fastapi import FastAPI
import os

# Import functions from the data processing module
from backend.data_processing import (
    load_data, get_companies, filter_by_company,
    get_company_metrics, get_company_location
)

# Create an instance of the FastAPI application
app = FastAPI()

# Endpoint to load the dataset
# When the user sends a GET request to '/load_data', this function runs
@app.get("/load_data")
async def load():
    return {"message": "Data Loaded Successfully!"}

# Endpoint to get the list of all companies
# A GET request to '/companies' triggers this function, returning all company names
@app.get("/companies")
async def get_all_companies():
    companies = get_companies()  # Fetch all company data
    return {"companies": companies}

# Endpoint to get details of a specific company by its name
# A GET request to '/company/{company_name}' returns specific company data, metrics, and location
@app.get("/company/{company_name}")
async def get_company_data(company_name: str):
    # Filter company data by company name
    company_data = filter_by_company(company_name)
    
    # Get metrics and location for the specified company
    metrics = get_company_metrics(company_data)
    location = get_company_location(company_data)
    
    # Return the company data, its metrics, and location in JSON format
    return {
        "company_data": company_data.to_dict(orient='records'),
        "metrics": metrics,
        "location": location
    }
