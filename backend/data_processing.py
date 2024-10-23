import os
import pandas as pd

def load_data():
    """
    Load the dataset from a file, either from a relative path (when running locally)
    or from an absolute path (when running in a Docker container).
    """
    
    # Check if the script is running in a Docker container by checking if the '/app' directory exists
    if os.path.exists('/app'):
        # If running inside a Docker container, use the absolute path for Docker
        data_path = '/app/data/dataset.csv'
    else:
        # If running locally, construct the relative path to the dataset
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
        data_path = os.path.join(script_dir, '..', 'data', 'dataset.csv')  # Go up one level and into the 'data' folder
    
    # Load the CSV file as a DataFrame using pandas
    return pd.read_csv(data_path)

# Load the dataset at the start and store it in a DataFrame called `df`
df = load_data()

def get_companies():
    """
    Retrieve a list of unique company names from the dataset.
    """
    return df['Company Name'].unique().tolist()  # Extract unique company names and return as a list

def filter_by_company(company_name):
    """
    Filter the dataset by a specific company name.
    
    Args:
    - company_name (str): The name of the company to filter by.
    
    Returns:
    - A DataFrame containing only the rows for the specified company.
    """
    return df[df['Company Name'] == company_name]  # Filter rows where 'Company Name' matches the input

def get_company_metrics(df):
    """
    Calculate and return various metrics for a company, such as emissions and capital investments.
    
    Args:
    - df (DataFrame): A filtered DataFrame for a specific company.
    
    Returns:
    - A dictionary with total emissions, capital catalyzed, and fund investments.
    """

    # Sum up the emissions (Scope 1, Scope 2, and Scope 3) and convert to float for precision
    emissions = {
        "Total Emissions": float(df['Total Emissions by Fund (tons of CO2e)'].sum()),
        "Scope 1": float(df['Scope 1 Emissions (tons of CO2e)'].sum()),
        "Scope 2": float(df['Scope 2 Emissions (tons of CO2e)'].sum()),
        "Scope 3": float(df['Scope 3 Emissions (tons of CO2e)'].sum())
    }
    
    # Sum up the capital committed and convert it to float
    capital_catalyzed = float(df['Total Capital Committed ($B)'].sum())
    
    # Sum up the fund investments and convert it to an integer
    fund_investments = int(df['Fund Investments'].sum())

    # Return the calculated metrics as a dictionary
    return {
        "emissions": emissions,
        "capital_catalyzed": capital_catalyzed,
        "fund_investments": fund_investments,
    }

def get_company_location(df):
    """
    Retrieve the country location of the company from the dataset.
    
    Args:
    - df (DataFrame): A filtered DataFrame for a specific company.
    
    Returns:
    - The country where the company is located (first occurrence in the dataset).
    """
    return df['Country'].values[0]  # Assuming all rows have the same country, return the first value
