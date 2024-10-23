import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests

# Streamlit App Layout
st.set_page_config(layout="wide")
st.title("Investment Dashboard")

# Sidebar search and selection
response = requests.get("http://127.0.0.1:8000/companies")
companies = response.json().get("companies", [])

# Adding "Overview" option manually at the top
companies.insert(0, "Overview")

# Sidebar for selecting either "Overview" or a company
company = st.sidebar.radio("Select a Company:", companies)

# Aggregated data dictionary for "Overview"
aggregated_data = {
    "Total Capital Committed ($B)": 0,
    "Fund Investments": 0,
    "Underlying Portfolio Companies": set(),
    "Total Emissions (tons CO2e)": 0,
    "Scope 1 Emissions (tons CO2e)": 0,
    "Scope 2 Emissions (tons CO2e)": 0,
    "Scope 3 Emissions (tons CO2e)": 0,
    "Theme Capital Catalyzed ($M)": {},
    "Global South Deals Funded": 0,
    "Countries": {}
}

# Fetch and calculate data for "Overview" or specific company
if company == "Overview":
    # Aggregate data for all companies
    for comp in companies[1:]:  # Skip the "Overview" entry
        company_data = requests.get(f"http://127.0.0.1:8000/company/{comp}").json()
        if isinstance(company_data.get("company_data"), list):
            for fund in company_data["company_data"]:
                aggregated_data["Total Capital Committed ($B)"] += fund.get("Total Capital Committed ($B)", 0)
                aggregated_data["Fund Investments"] += fund.get("Fund Investments", 0)
                aggregated_data["Total Emissions (tons CO2e)"] += fund.get("Total Emissions by Fund (tons of CO2e)", 0)
                aggregated_data["Scope 1 Emissions (tons CO2e)"] += fund.get("Scope 1 Emissions (tons of CO2e)", 0)
                aggregated_data["Scope 2 Emissions (tons CO2e)"] += fund.get("Scope 2 Emissions (tons of CO2e)", 0)
                aggregated_data["Scope 3 Emissions (tons CO2e)"] += fund.get("Scope 3 Emissions (tons of CO2e)", 0)
                theme = fund.get("Theme", "N/A")
                if theme not in aggregated_data["Theme Capital Catalyzed ($M)"]:
                    aggregated_data["Theme Capital Catalyzed ($M)"][theme] = 0
                aggregated_data["Theme Capital Catalyzed ($M)"][theme] += fund.get("Theme Capital Catalyzed ($M)", 0)
                aggregated_data["Underlying Portfolio Companies"].add(fund.get("Company Name", "N/A"))

                # Add country data for the map
                country = fund.get("Country", "N/A")
                if country not in aggregated_data["Countries"]:
                    aggregated_data["Countries"][country] = {
                        "Deals Funded": 0
                    }
                aggregated_data["Countries"][country]["Deals Funded"] += fund.get("Global South Deals Funded", 0)
else:
    # Fetch data for the selected company
    company_data = requests.get(f"http://127.0.0.1:8000/company/{company}").json()
    if isinstance(company_data.get("company_data"), list):
        aggregated_data = {
            "Total Capital Committed ($B)": sum([fund.get("Total Capital Committed ($B)", 0) for fund in company_data["company_data"]]),
            "Fund Investments": sum([fund.get("Fund Investments", 0) for fund in company_data["company_data"]]),
            "Underlying Portfolio Companies": "N/A",
            "Total Emissions (tons CO2e)": sum([fund.get("Total Emissions by Fund (tons of CO2e)", 0) for fund in company_data["company_data"]]),
            "Scope 1 Emissions (tons CO2e)": sum([fund.get("Scope 1 Emissions (tons of CO2e)", 0) for fund in company_data["company_data"]]),
            "Scope 2 Emissions (tons CO2e)": sum([fund.get("Scope 2 Emissions (tons of CO2e)", 0) for fund in company_data["company_data"]]),
            "Scope 3 Emissions (tons CO2e)": sum([fund.get("Scope 3 Emissions (tons of CO2e)", 0) for fund in company_data["company_data"]]),
            "Theme Capital Catalyzed ($M)": {},
            "Countries": {}
        }

        # Add country data for the map
        for fund in company_data["company_data"]:
            theme = fund.get("Theme", "N/A")
            if theme not in aggregated_data["Theme Capital Catalyzed ($M)"]:
                aggregated_data["Theme Capital Catalyzed ($M)"][theme] = 0
            aggregated_data["Theme Capital Catalyzed ($M)"][theme] += fund.get("Theme Capital Catalyzed ($M)", 0)

            country = fund.get("Country", "N/A")
            if country not in aggregated_data["Countries"]:
                aggregated_data["Countries"][country] = {
                    "Deals Funded": 0
                }
            aggregated_data["Countries"][country]["Deals Funded"] += fund.get("Global South Deals Funded", 0)

# Tabs for the sections
tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["Overview", "Fund Breakdown", "Emissions Overview", "Thematic Overview", "Global South Investments"])

# Overview Tab
with tab1:
    st.header(f"{company} - Overview")
    
    if company == "Overview":
        # Use four columns for the "Overview" case
        col1, col2, col3, col4 = st.columns(4)

        # Displaying Key Metrics with rounding off
        col1.metric("Total Capital Committed (B)", round(aggregated_data["Total Capital Committed ($B)"], 2))
        col2.metric("Total Fund Investments", aggregated_data["Fund Investments"])
        col3.metric("Underlying Portfolio Companies", len(aggregated_data["Underlying Portfolio Companies"]))
        col4.metric("Total Emissions (tons CO2e)", round(aggregated_data["Total Emissions (tons CO2e)"], 2))
        
        # Summary for Overview
        st.markdown(f"""
        ### Summary for **{company}**:
        
        - **Total Capital Committed**: **{round(aggregated_data['Total Capital Committed ($B)'], 2)} billion dollars**
        - **Total Fund Investments**: **{aggregated_data['Fund Investments']}**
        - **Underlying Portfolio Companies**: **{len(aggregated_data["Underlying Portfolio Companies"])}**
        - **Total Emissions across all scopes**: **{round(aggregated_data['Total Emissions (tons CO2e)'], 2)} tons of CO2e**
        """)

    else:
        # Use three columns for individual company cases
        col1, col2, col3 = st.columns(3)

        # Displaying Key Metrics with rounding off
        col1.metric("Total Capital Committed (B)", round(aggregated_data["Total Capital Committed ($B)"], 2))
        col2.metric("Total Fund Investments", aggregated_data["Fund Investments"])
        col3.metric("Total Emissions (tons CO2e)", round(aggregated_data["Total Emissions (tons CO2e)"], 2))
        
        # Summary for individual company for Total Capital Committed, Total Fund Investments and Total Emissions across all scopes
        st.markdown(f"""
        ### Summary for **{company}**:
        
        - **Total Capital Committed**: **{round(aggregated_data['Total Capital Committed ($B)'], 2)} billion dollars**
        - **Total Fund Investments**: **{aggregated_data['Fund Investments']}**
        - **Total Emissions across all scopes**: **{round(aggregated_data['Total Emissions (tons CO2e)'], 2)} tons of CO2e**
        """)

# Fund Breakdown Tab
with tab2:
    st.header("Fund Breakdown")
    col1, col2 = st.columns(2)

    if company == "Overview":
        # Aggregating fund data across all companies
        committed_capitals_aggregated = {}
        deals_completed_aggregated = {}

        for comp in companies[1:]:  # Skip the "Overview" entry
            company_data = requests.get(f"http://127.0.0.1:8000/company/{comp}").json()
            for fund in company_data["company_data"]:
                fund_name = fund["Fund"]

                # Aggregating committed capital
                if fund_name not in committed_capitals_aggregated:
                    committed_capitals_aggregated[fund_name] = 0
                committed_capitals_aggregated[fund_name] += fund.get("Total Capital Committed ($B)", 0)

                # Aggregating deals completed
                if fund_name not in deals_completed_aggregated:
                    deals_completed_aggregated[fund_name] = 0
                deals_completed_aggregated[fund_name] += fund.get("Fund Investments", 0)

        # Convert aggregated data to lists for visualization
        fund_names = list(committed_capitals_aggregated.keys())
        committed_capitals = list(committed_capitals_aggregated.values())
        deals_completed = list(deals_completed_aggregated.values())

    else:
        # Fetching and processing data for the selected company
        committed_capitals_aggregated = {}
        deals_completed_aggregated = {}

        # Fetch data for the selected company
        company_data = requests.get(f"http://127.0.0.1:8000/company/{company}").json()

        for fund in company_data["company_data"]:
            fund_name = fund["Fund"]

            # Aggregating committed capital
            if fund_name not in committed_capitals_aggregated:
                committed_capitals_aggregated[fund_name] = 0
            committed_capitals_aggregated[fund_name] += fund.get("Total Capital Committed ($B)", 0)

            # Aggregating deals completed
            if fund_name not in deals_completed_aggregated:
                deals_completed_aggregated[fund_name] = 0
            deals_completed_aggregated[fund_name] += fund.get("Fund Investments", 0)

        # Convert aggregated data to lists for visualization
        fund_names = list(committed_capitals_aggregated.keys())
        committed_capitals = list(committed_capitals_aggregated.values())
        deals_completed = list(deals_completed_aggregated.values())

    # Display Pie Charts for Committed Capital by Fund
    col1.subheader("Committed Capital by Fund")
    fig1 = px.pie(names=fund_names, values=committed_capitals, title="Committed Capital by Fund")
    col1.plotly_chart(fig1)

    # Display Pie Charts for Deals Completed by Fund
    col2.subheader("Deals Completed by Fund")
    fig2 = px.pie(names=fund_names, values=deals_completed, title="Deals Completed by Fund")
    col2.plotly_chart(fig2)

    # Dynamically find the fund with the largest and smallest aggregated capital committed and deals completed
    max_capital_index = committed_capitals.index(max(committed_capitals))
    min_capital_index = committed_capitals.index(min(committed_capitals))

    max_deals_index = deals_completed.index(max(deals_completed))
    min_deals_index = deals_completed.index(min(deals_completed))

    # Get the largest and smallest fund's name and values for the summary
    largest_fund_capital = fund_names[max_capital_index]
    smallest_fund_capital = fund_names[min_capital_index]
    largest_fund_capital_value = committed_capitals[max_capital_index]
    smallest_fund_capital_value = committed_capitals[min_capital_index]

    largest_fund_deals = fund_names[max_deals_index]
    smallest_fund_deals = fund_names[min_deals_index]
    largest_fund_deals_value = deals_completed[max_deals_index]
    smallest_fund_deals_value = deals_completed[min_deals_index]

    # Summary for highest and smallest Capital Committed by Fund and Deals Completed by Fund for a Company
    st.markdown(f"""
    ### Summary for **{company}**:
    
    - **Largest Fund by Capital Committed**: **{largest_fund_capital}** with **{round(largest_fund_capital_value, 2)} billion dollars**
    - **Smallest Fund by Capital Committed**: **{smallest_fund_capital}** with **{round(smallest_fund_capital_value, 2)} billion dollars**
    - **Largest Fund by Deals Completed**: **{largest_fund_deals}** with **{largest_fund_deals_value} deals**
    - **Smallest Fund by Deals Completed**: **{smallest_fund_deals}** with **{smallest_fund_deals_value} deals**
    """)

# Emissions Overview Tab
with tab3:
    st.header(f"Emissions Overview by Theme - {company}")

    # Create a dictionary to store emissions data by theme
    if company == "Overview":
        emissions_by_theme = {}

        for comp in companies[1:]:
            company_data = requests.get(f"http://127.0.0.1:8000/company/{comp}").json()
            if isinstance(company_data.get("company_data"), list):
                for fund in company_data["company_data"]:
                    theme = fund.get("Theme", "N/A")
                    if theme not in emissions_by_theme:
                        emissions_by_theme[theme] = {
                            "Scope 1": 0,
                            "Scope 2": 0,
                            "Scope 3": 0
                        }
                    emissions_by_theme[theme]["Scope 1"] += fund.get("Scope 1 Emissions (tons of CO2e)", 0)
                    emissions_by_theme[theme]["Scope 2"] += fund.get("Scope 2 Emissions (tons of CO2e)", 0)
                    emissions_by_theme[theme]["Scope 3"] += fund.get("Scope 3 Emissions (tons of CO2e)", 0)

    else:
        emissions_by_theme = {}
        for fund in company_data["company_data"]:
            theme = fund.get("Theme", "N/A")
            if theme not in emissions_by_theme:
                emissions_by_theme[theme] = {
                    "Scope 1": 0,
                    "Scope 2": 0,
                    "Scope 3": 0
                }
            emissions_by_theme[theme]["Scope 1"] += fund.get("Scope 1 Emissions (tons of CO2e)", 0)
            emissions_by_theme[theme]["Scope 2"] += fund.get("Scope 2 Emissions (tons of CO2e)", 0)
            emissions_by_theme[theme]["Scope 3"] += fund.get("Scope 3 Emissions (tons of CO2e)", 0)

    # Preparing data for plot
    df_emissions_by_theme = pd.DataFrame([{"Theme": theme, "Scope 1": data["Scope 1"], "Scope 2": data["Scope 2"], "Scope 3": data["Scope 3"]}
                                          for theme, data in emissions_by_theme.items()])

    # Melt the data for visualization
    df_emissions_melted = df_emissions_by_theme.melt(id_vars="Theme", var_name="Scope", value_name="Emissions")

    # Create a bar chart showing emissions breakdown by theme and scope
    fig_emissions_theme = px.bar(df_emissions_melted, x="Theme", y="Emissions", color="Scope", barmode="group",
                                 title=f"Emissions Breakdown by Theme and Scope for {company}")
    st.plotly_chart(fig_emissions_theme)

    highest_scope_1_value = df_emissions_by_theme["Scope 1"].max()
    smallest_scope_1_value = df_emissions_by_theme["Scope 1"].min()

    highest_scope_2_value = df_emissions_by_theme["Scope 2"].max()
    smallest_scope_2_value = df_emissions_by_theme["Scope 2"].min()

    highest_scope_3_value = df_emissions_by_theme["Scope 3"].max()
    smallest_scope_3_value = df_emissions_by_theme["Scope 3"].min()

    highest_scope_1_themes = df_emissions_by_theme[df_emissions_by_theme["Scope 1"] == highest_scope_1_value]["Theme"].tolist()
    smallest_scope_1_themes = df_emissions_by_theme[df_emissions_by_theme["Scope 1"] == smallest_scope_1_value]["Theme"].tolist()

    highest_scope_2_themes = df_emissions_by_theme[df_emissions_by_theme["Scope 2"] == highest_scope_2_value]["Theme"].tolist()
    smallest_scope_2_themes = df_emissions_by_theme[df_emissions_by_theme["Scope 2"] == smallest_scope_2_value]["Theme"].tolist()

    highest_scope_3_themes = df_emissions_by_theme[df_emissions_by_theme["Scope 3"] == highest_scope_3_value]["Theme"].tolist()
    smallest_scope_3_themes = df_emissions_by_theme[df_emissions_by_theme["Scope 3"] == smallest_scope_3_value]["Theme"].tolist()

    total_scope_1_emissions = df_emissions_by_theme["Scope 1"].sum()
    total_scope_2_emissions = df_emissions_by_theme["Scope 2"].sum()
    total_scope_3_emissions = df_emissions_by_theme["Scope 3"].sum()

    # Display asmmary for largest and smallest emission(tons of CO2e) for each scope
    st.markdown(f"""
    ### Summary for **{company}**:

    - **Theme(s) with the Highest Scope 1 Emissions**: **{', '.join(highest_scope_1_themes)}** with **{highest_scope_1_value} tons**
    - **Theme(s) with the Smallest Scope 1 Emissions**: **{', '.join(smallest_scope_1_themes)}** with **{smallest_scope_1_value} tons**
    - **Theme(s) with the Highest Scope 2 Emissions**: **{', '.join(highest_scope_2_themes)}** with **{highest_scope_2_value} tons**
    - **Theme(s) with the Smallest Scope 2 Emissions**: **{', '.join(smallest_scope_2_themes)}** with **{smallest_scope_2_value} tons**
    - **Theme(s) with the Highest Scope 3 Emissions**: **{', '.join(highest_scope_3_themes)}** with **{highest_scope_3_value} tons**
    - **Theme(s) with the Smallest Scope 3 Emissions**: **{', '.join(smallest_scope_3_themes)}** with **{smallest_scope_3_value} tons**

    **Total Emissions across all scopes**:
    - **Scope 1 Emissions:** **{total_scope_1_emissions} tons**
    - **Scope 2 Emissions:** **{total_scope_2_emissions} tons**
    - **Scope 3 Emissions:** **{total_scope_3_emissions} tons**
    """)

# Thematic Overview Tab
with tab4:
    st.header("Thematic Overview")

    # Prepare the theme data for capital catalyzed
    theme_data = {
        "Theme": list(aggregated_data["Theme Capital Catalyzed ($M)"].keys()),
        "Capital Catalyzed ($M)": list(aggregated_data["Theme Capital Catalyzed ($M)"].values())
    }

    # Create a bar chart showing capital catalyzed by theme
    st.subheader("Capital Catalyzed by Theme")
    df_themes = pd.DataFrame(theme_data)
    fig_themes = px.bar(df_themes, x="Theme", y="Capital Catalyzed ($M)", title="Capital Catalyzed by Theme")
    st.plotly_chart(fig_themes)

    max_capital = df_themes["Capital Catalyzed ($M)"].max()
    min_capital = df_themes["Capital Catalyzed ($M)"].min()

    highest_themes = df_themes[df_themes["Capital Catalyzed ($M)"] == max_capital]["Theme"].tolist()
    smallest_themes = df_themes[df_themes["Capital Catalyzed ($M)"] == min_capital]["Theme"].tolist()

    total_capital = df_themes["Capital Catalyzed ($M)"].sum()

    # Display a summary for Highest and smallest Capital Catalyzed for each Theme in million dollars
    st.markdown(f"""
    ### Summary for **{company}**:
    
    - **Theme(s) with the Highest Capital Catalyzed**: **{', '.join(highest_themes)}** with **{max_capital} million dollars**
    - **Theme(s) with the Smallest Capital Catalyzed**: **{', '.join(smallest_themes)}** with **{min_capital} million dollars**
    - **Total Capital Catalyzed across all themes**: **{total_capital} million dollars**
    """)

# Global South Investments
with tab5:
    st.header("Global South Investments")

    # Prepare data for the map based on deals funded
    countries_df = pd.DataFrame([{
        "Country": country,
        "Global South Deals Funded": data["Deals Funded"]
    } for country, data in aggregated_data["Countries"].items()])

    if not countries_df.empty:
        # Fetch ISO codes for countries using Plotly's built-in dataset
        df_countries = px.data.gapminder()[['country', 'iso_alpha']].drop_duplicates()

        # Merge the country data with the ISO codes
        countries_df = countries_df.merge(df_countries, left_on='Country', right_on='country', how='left')

        # Remove any rows where 'iso_alpha' is NaN
        countries_df = countries_df.dropna(subset=['iso_alpha'])

        fig = go.Figure()

        # Add markers for countries with hover text showing deals funded
        fig.add_trace(go.Scattergeo(
            locations=countries_df['iso_alpha'],
            locationmode='ISO-3',
            text=countries_df.apply(lambda row: f"{row['Country']}<br>Deals Funded: {row['Global South Deals Funded']}", axis=1),
            mode='markers+text',
            marker=dict(
                symbol='circle',
                size=countries_df['Global South Deals Funded'] * 3,  # Adjust size for better visibility
                sizemode='area',
                sizeref=2.*max(countries_df['Global South Deals Funded'])/(20.**2),  # Fine-tune marker size
                sizemin=6,  # Minimum size of the markers
                color=countries_df['Global South Deals Funded'],  # Color based on deals funded
                colorscale='Viridis',  # Heatmap-like color scale
                colorbar=dict(title="Deals Funded"),  # Show a colorbar on the side
                line=dict(width=1, color='black')  # Line color around the markers
            ),
            hoverinfo='text',  # Show country names and "Deals Funded" on hover
            textposition='top center',  # Position the country names above the markers
            showlegend=False
        ))

        # Update map layout with dark background and ocean/lake colors
        fig.update_layout(
            title='Global South Deals Funded by Country',
            geo=dict(
                showland=True,
                landcolor='black',
                bgcolor='black',  # Dark background for oceans/lakes
                showcountries=True,
                countrycolor='white',
                showframe=False,
                coastlinecolor='white',
                countrywidth=0.5,
                projection_type='equirectangular',
                lonaxis_range=[-180, 180],
                lataxis_range=[-60, 90],
                resolution=50,
                lakecolor='black',  # Dark color for lakes/oceans
                oceancolor='black',  # Dark color for oceans
            ),
            paper_bgcolor='black',
            plot_bgcolor='black',
            font=dict(color='white'),
            height=900,  # Increased height for a larger map
            width=1400,  # Increased width for a wider map
            margin=dict(l=10, r=10, t=30, b=10)  # Adjust margins
        )

        # Display the map in Streamlit
        st.plotly_chart(fig, use_container_width=True)

        # Calculate the max and min deals and handle multiple countries with the same values
        max_deals = countries_df["Global South Deals Funded"].max()
        min_deals = countries_df["Global South Deals Funded"].min()

        highest_deals_countries = countries_df[countries_df["Global South Deals Funded"] == max_deals]["Country"].tolist()
        smallest_deals_countries = countries_df[countries_df["Global South Deals Funded"] == min_deals]["Country"].tolist()

        total_deals = countries_df["Global South Deals Funded"].sum()

        # Summary for highest and smallest Global South Deals Funded
        st.markdown(f"""
        ### Summary for **{company}**:
        
        - **Country(ies) with the Highest Global South Deals Funded**: **{', '.join(highest_deals_countries)}** with **{max_deals} deals**
        - **Country(ies) with the Smallest Global South Deals Funded**: **{', '.join(smallest_deals_countries)}** with **{min_deals} deals**
        - **Total Global South Deals Funded**: **{total_deals} deals**
        """)
    else:
        st.write("No Global South Investments data available for the selected company.")
