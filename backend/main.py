from fastapi import FastAPI
import os

from backend.data_processing import load_data, get_companies, filter_by_company, get_company_metrics, get_company_location

app = FastAPI()

# Endpoint to load the dataset
@app.get("/load_data")
async def load():
    return {"message": "Data Loaded Successfully!"}

# Endpoint to get all companies
@app.get("/companies")
async def get_all_companies():
    companies = get_companies()
    return {"companies": companies}

# Endpoint to filter by company name
@app.get("/company/{company_name}")
async def get_company_data(company_name: str):
    company_data = filter_by_company(company_name)
    metrics = get_company_metrics(company_data)
    location = get_company_location(company_data)
    return {
        "company_data": company_data.to_dict(orient='records'),
        "metrics": metrics,
        "location": location
    }


