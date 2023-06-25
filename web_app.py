from ast import main
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# Load the dataset
#@st.cache_data
def load_data():
    df = pd.read_csv("Forbes_global_2000_with_continent.csv")
    return df
def load_data1():
    df_og=pd.read_csv("Forbes Global 2000 (Year 2022).xlsx - Sheet1.csv")
    return df_og
df_og=load_data()
df = load_data()
numeric_columns=df[['Sales','Profits','Assets','Market_Value']]
df['Country']=df['Country'].replace("United States","United States of America")
# Title and description
st.title('Forbes Global 2000 Companies - Exploratory Data Analysis')
st.markdown('This web app performs exploratory data analysis on the Forbes Global 2000 companies dataset.')
st.markdown("Original Dataset")
st.write(df_og)
# Sidebar - Select Analysis Task
analysis_task = st.sidebar.selectbox('Select Analysis Task', [
    'Data Cleaning & Preprocessing',
    'Descriptive Statistics',
    'Categorical Analysis - Industry',
    'Categorical Analysis - Continent',
    'Correlation Analysis',
    'Top 10s',
    'Geographical Analysis'

])

# Analysis Tasks
if analysis_task=='Data Cleaning & Preprocessing':
    st.subheader("Data Cleaning and Preprocessing")
    st.dataframe(df)
    st.markdown("Here, we have added a column 'continent' and changed the name of the country 'United States' to 'United States of America for further use.")
    st.markdown("We have also assumed Cayman Islands and Bermuda to be the countries in North America.")

elif analysis_task == 'Descriptive Statistics':

    st.subheader('Descriptive Statistics')
    st.markdown("Here, we will give general information about the numeric columns of the given dataset.")
    st.write(df.describe())


elif analysis_task == 'Categorical Analysis - Industry':
    st.subheader('Categorical Analysis - Industry')

    industry_counts = df['Industry'].value_counts()
    st.markdown("This section shows the number of companies belonging to various industries.")
# Create the bar chart
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(industry_counts.index, industry_counts.values)
    ax.set_xlabel('Industry')
    ax.set_ylabel('Count')
    ax.set_title('Companies by Industry')
    ax.tick_params(axis='x', rotation=90)

# Display the bar chart using Streamlit
    st.pyplot(fig)

elif analysis_task == 'Categorical Analysis - Continent':
    st.subheader('Categorical Analysis - Country')
    continent_counts = df['continent'].value_counts()

# Create the bar chart
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(continent_counts.index, continent_counts.values)
    ax1.set_xlabel('Continent')
    ax1.set_ylabel('Count')
    ax1.set_title('Companies by Continent')
    ax1.tick_params(axis='x', rotation=90)

# Display the bar chart using Streamlit
    st.pyplot(fig1)



elif analysis_task == 'Correlation Analysis':
    st.subheader('Correlation Analysis')
    st.markdown("In this section, we have given the Correlation Analysis of numeric columns of the dataset ")

    correlation_matrix = numeric_columns.corr()
    st.write(correlation_matrix)
    fig2, ax2 = plt.subplots()
    sns.heatmap(correlation_matrix, ax=ax2)
    st.write(fig2)
elif analysis_task=='Geographical Analysis':
    st.markdown("The map shows the top 10 countries with highest number of companies in Forbes Global 2000 2022 list ")
    st.markdown("Top ten countries are highlighted with Blue.")
# Load the data
    top_countries=df['Country'].value_counts().head(10)
    # Load the world shapefile
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

# Merge the world shapefile with the top countries data
    merged = world.merge(top_countries, left_on='name', right_index=True, how='left')

# Create a Streamlit app
    st.title('Top Countries with Highest Number of Companies')

# Plot the world map using Streamlit
    fig3, ax3 = plt.subplots(figsize=(15, 10))
    world.boundary.plot(ax=ax3, linewidth=0.8, color='black')
    merged.plot(column='name', cmap='YlOrRd', linewidth=0.8, ax=ax3, edgecolor='0.8', legend=False)

# Set color for the top 10 countries
    highlight_color = 'blue'
    highlighted_countries = merged[merged['name'].isin(top_countries.index)]
    highlighted_countries.plot(color=highlight_color, ax=ax3)

# Create a legend-like text
    legend_text = []
    for Country, count in top_countries.items():
        legend_text.append(f'{Country}: {count}')

# Display the legend text
    st.text('\n'.join(legend_text))

# Display the map in Streamlit
    
# Display the legend text
    #st.text('\n'.join(legend_text))

# Display the map in Streamlit
    st.pyplot(fig3)
    st.markdown("Here is the list of top five industries according to their market value in the different continents.")
    st.markdown("Africa")
    africa_df = df[df['continent'] == 'Africa']

# Group by industry and calculate sum of market values
    grouped_africa = africa_df.groupby('Industry')['Market_Value'].sum()

# Sort the industries based on market value in descending order
    top_industries_continent_africa = grouped_africa.sort_values(ascending=False).head(5)

# Display the top 5 industries in Africa with highest market value
    st.write(top_industries_continent_africa)
    st.markdown("Asia")
    asia_df = df[df['continent'] == 'Asia']

# Group by industry and calculate sum of market values
    grouped_asia = asia_df.groupby('Industry')['Market_Value'].sum()

# Sort the industries based on market value in descending order
    top_industries_continent_asia = grouped_asia.sort_values(ascending=False).head(5)

# Display the top 5 industries in Africa with highest market value
    st.write(top_industries_continent_asia)
    st.markdown("Europe")
    europe_df = df[df['continent'] == 'Europe']

# Group by industry and calculate sum of market values
    grouped_europe = europe_df.groupby('Industry')['Market_Value'].sum()

# Sort the industries based on market value in descending order
    top_industries_continent_europe = grouped_europe.sort_values(ascending=False).head(5)

# Display the top 5 industries in Africa with highest market value
    st.write(top_industries_continent_europe)

    st.markdown("Oceania")
    oceania_df = df[df['continent'] == 'Oceania']

# Group by industry and calculate sum of market values
    grouped_oceania = oceania_df.groupby('Industry')['Market_Value'].sum()

# Sort the industries based on market value in descending order
    top_industries_continent_oceania = grouped_oceania.sort_values(ascending=False).head(5)

# Display the top 5 industries in Africa with highest market value
    st.write(top_industries_continent_oceania)

    st.markdown("North America")
    
    na_df = df[df['continent'] == 'North America']

# Group by industry and calculate sum of market values
    grouped_na = na_df.groupby('Industry')['Market_Value'].sum()

# Sort the industries based on market value in descending order
    top_industries_continent_na = grouped_na.sort_values(ascending=False).head(5)

# Display the top 5 industries in Africa with highest market value
    st.write(top_industries_continent_na)

    st.markdown("South America")
    sa_df = df[df['continent'] == 'South America']

# Group by industry and calculate sum of market values
    grouped_sa = sa_df.groupby('Industry')['Market_Value'].sum()

# Sort the industries based on market value in descending order
    top_industries_continent_sa = grouped_sa.sort_values(ascending=False).head(5)

# Display the top 5 industries in Africa with highest market value
    st.write(top_industries_continent_sa)

elif analysis_task=='Top 10s':
    st.subheader("Companies")
    st.markdown("Top 10 Companies by Profits")
    top_companies_by_profits = df.nlargest(10, 'Profits')
    plt.figure(figsize=(10, 6))
    plt.bar(top_companies_by_profits['Company'], top_companies_by_profits['Profits'])
    plt.xlabel('Company')
    plt.ylabel('Profits')
    plt.title('Top 10 Companies by Profits')    
    plt.xticks(rotation=90)
    st.pyplot(plt.gcf())

    
    st.markdown("Top 10 Companies by Assets Owned")
    top_companies_by_assets = df.nlargest(10, 'Assets')
    plt.figure(figsize=(10, 6))
    plt.bar(top_companies_by_assets['Company'], top_companies_by_assets['Assets'])
    plt.xlabel('Company')
    plt.ylabel('Assets')
    plt.title('Top 10 Companies by Assets Owned')
    plt.xticks(rotation=90)
    st.pyplot(plt.gcf())
    st.markdown("Top 10 Companies by Sales Done")
    top_companies_by_sales = df.nlargest(10, 'Sales')
    plt.figure(figsize=(10, 6))
    plt.bar(top_companies_by_sales['Company'], top_companies_by_sales['Sales'])
    plt.xlabel('Company')
    plt.ylabel('Sales')
    plt.title('Top 10 Companies by Sales')
    plt.xticks(rotation=90)
    st.pyplot(plt.gcf())
    st.markdown('Top 10 Companies by Market Value')

    top_companies_by_mv = df.nlargest(10, 'Market_Value')
    plt.figure(figsize=(10, 6))
    plt.bar(top_companies_by_mv['Company'], top_companies_by_mv['Market_Value'])
    plt.xlabel('Company')
    plt.ylabel('Market_Value')
    plt.title('Top 10 Companies by Market Value')
    plt.xticks(rotation=90)
    st.pyplot(plt.gcf())
    st.subheader("Industries")
    st.markdown("On the basis of Profits")
    profit_industry=df.groupby("Industry")["Profits"].sum()
    top_industries_profit=profit_industry.nlargest(10)

    st.write(top_industries_profit)
    st.markdown("On the basis of Market_Value")
    mv_industry=df.groupby("Industry")["Market_Value"].sum()
    top_industries_mv=mv_industry.nlargest(10)
    st.write(top_industries_mv)
    st.markdown("On the basis of Assets Owned")
    asset_industry=df.groupby("Industry")["Assets"].sum()
    top_industries_asset=asset_industry.nlargest(10)
    st.write(top_industries_asset)
    st.markdown("On the basis of Sales")
    sale_industry=df.groupby("Industry")["Sales"].sum()
    top_industries_sale=sale_industry.nlargest(10)
    st.write(top_industries_sale)

if __name__ == '__main__':
    main()    


    

#top_countries=df['Country'].value_counts().head(10)
#print(top_countries)






