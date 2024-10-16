import os
import pandas as pd

import os
import pandas as pd

def load_data():
    """Load dataset from a relative path if running locally or absolute path if in Docker."""
    
    # Check if the script is running in a Docker container by checking an environment variable
    if os.path.exists('/app'):
        # Running inside Docker
        data_path = '/app/data/dataset.csv'
    else:
        # Running locally
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_path = os.path.join(script_dir, '..', 'data', 'dataset.csv')
    
    # Load the dataset
    return pd.read_csv(data_path)

# Load the dataset
df = load_data()

def get_companies():
    return df['Company Name'].unique().tolist()

def filter_by_company(company_name):
    return df[df['Company Name'] == company_name]

def get_company_metrics(df):


    emissions = {
        "Total Emissions": float(df['Total Emissions by Fund (tons of CO2e)'].sum()),  # Convert to float
        "Scope 1": float(df['Scope 1 Emissions (tons of CO2e)'].sum()),  # Convert to float
        "Scope 2": float(df['Scope 2 Emissions (tons of CO2e)'].sum()),  # Convert to float
        "Scope 3": float(df['Scope 3 Emissions (tons of CO2e)'].sum())  # Convert to float
    }
    capital_catalyzed = float(df['Total Capital Committed ($B)'].sum())  # Convert to float
    fund_investments = int(df['Fund Investments'].sum())  # Convert to int

    return {
        "emissions": emissions,
        "capital_catalyzed": capital_catalyzed,
        "fund_investments": fund_investments,
    }


def get_company_location(df):
    return df['Country'].values[0]  # Assuming no latitude/longitude


