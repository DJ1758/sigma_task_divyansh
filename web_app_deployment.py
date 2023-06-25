from ast import main
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import geopandas as gpd


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
    'Geographical Analysis',
    'Conclusion'

])

# Analysis Tasks
if analysis_task=='Data Cleaning & Preprocessing':
    st.subheader("Data Cleaning and Preprocessing")
    st.dataframe(df)
   
    st.markdown("""
                - I have added a column 'continent' and changed the name of the country 'United States' to 'United States of America' for further use.
                - I have also assumed Cayman Islands and Bermuda to be in North America.
                - I have also changed the data type of "Rank_nr" column from object to int64.
                - There was one row with value in "Rank_nr" as "TRUE" which was replaced with the correct value.
                """)
elif analysis_task == 'Descriptive Statistics':

    st.subheader('Descriptive Statistics')
    st.markdown("In this section, the general information about the numeric columns of the given dataset is displayed.")
    st.write(df.describe())


elif analysis_task == 'Categorical Analysis - Industry':
    st.subheader('Categorical Analysis - Industry')

    industry_counts = df['Industry'].value_counts()
    st.markdown("This section shows the number of companies belonging to various industries.")

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(industry_counts.index, industry_counts.values)
    ax.set_xlabel('Industry')
    ax.set_ylabel('Count')
    ax.set_title('Companies by Industry')
    ax.tick_params(axis='x', rotation=90)
    
    st.pyplot(fig)
    
    industry_counts = df['Industry'].value_counts()
    industry_names=industry_counts.index
    cmap = plt.cm.get_cmap('tab20b')
    colors = cmap(np.linspace(0, 1, 26))
    
    fig_pie, ax_pie = plt.subplots()
    ax_pie.pie(industry_counts, labels=industry_names,wedgeprops={'edgecolor':'black'} ,colors=colors, radius=2)
    ax_pie.set_aspect('equal')
    st.pyplot(fig_pie)
    

    st.markdown("Distribution of Profits over industries")
    plt.figure(figsize=(12, 8))
    df.boxplot(column='Profits', by='Industry', vert=True)
    plt.xlabel('Industry')
    plt.ylabel('Profits')
    plt.title('Distribution of Profits over Industries')
    plt.tight_layout()
    plt.xticks(rotation=90)
    st.pyplot(plt.gcf())
    st.markdown("""
    - The industries with highest profits were Banking and Oil&Gas Operations.
    - The Semiconductors Industry had the largest interquantile range suggesting the most consistent profits in a single sector.
    - IT Software & Services has the greatest profit-loss range.
    - Industry operating with greatest losses is IT Software & Services. 
    """)
    
  
elif analysis_task == 'Categorical Analysis - Continent':
    st.subheader('Categorical Analysis - Continent')
    continent_counts = df['continent'].value_counts()
    fig1, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(continent_counts.index, continent_counts.values)
    ax1.set_xlabel('Continent')
    ax1.set_ylabel('Count')
    ax1.set_title('Companies by Continent')
    ax1.tick_params(axis='x', rotation=90)
    st.pyplot(fig1)



elif analysis_task == 'Correlation Analysis':
    st.subheader('Correlation Analysis')
    st.markdown("In this section, I have displayed the Correlation Analysis of numeric columns of the dataset ")

    correlation_matrix = numeric_columns.corr()
    st.write(correlation_matrix)
    fig2, ax2 = plt.subplots()
    sns.heatmap(correlation_matrix, ax=ax2)
    st.write(fig2)


elif analysis_task=='Geographical Analysis':
    st.markdown("The map shows the top 10 countries with highest number of companies in Forbes Global 2000 2022 list ")
    st.markdown("Top ten countries are highlighted with Blue.")
    top_countries=df['Country'].value_counts().head(10)    
    world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    merged = world.merge(top_countries, left_on='name', right_index=True, how='left')
    st.title('Top Countries with Highest Number of Companies')
    fig3, ax3 = plt.subplots(figsize=(15, 10))
    world.boundary.plot(ax=ax3, linewidth=0.8, color='black')
    merged.plot(column='name', cmap='YlOrRd', linewidth=0.8, ax=ax3, edgecolor='0.8', legend=False)
    highlight_color = 'blue'
    highlighted_countries = merged[merged['name'].isin(top_countries.index)]
    highlighted_countries.plot(color=highlight_color, ax=ax3)

    legend_text = []
    for Country, count in top_countries.items():
        legend_text.append(f'{Country}: {count}')


    st.text('\n'.join(legend_text))  

    st.pyplot(fig3)
    st.markdown("List of top five industries according to their profits in the different continents.")
    st.markdown("Africa")
    africa_df = df[df['continent'] == 'Africa']


    grouped_africa = africa_df.groupby('Industry')['Profits'].sum()


    top_industries_continent_africa = grouped_africa.sort_values(ascending=False).head(5)


    st.write(top_industries_continent_africa)
    st.markdown("Asia")
    asia_df = df[df['continent'] == 'Asia']


    grouped_asia = asia_df.groupby('Industry')['Profits'].sum()


    top_industries_continent_asia = grouped_asia.sort_values(ascending=False).head(5)


    st.write(top_industries_continent_asia)
    st.markdown("Europe")
    europe_df = df[df['continent'] == 'Europe']


    grouped_europe = europe_df.groupby('Industry')['Profits'].sum()


    top_industries_continent_europe = grouped_europe.sort_values(ascending=False).head(5)


    st.write(top_industries_continent_europe)

    st.markdown("Oceania")
    oceania_df = df[df['continent'] == 'Oceania']


    grouped_oceania = oceania_df.groupby('Industry')['Profits'].sum()


    top_industries_continent_oceania = grouped_oceania.sort_values(ascending=False).head(5)


    st.write(top_industries_continent_oceania)

    st.markdown("North America")
    
    na_df = df[df['continent'] == 'North America']


    grouped_na = na_df.groupby('Industry')['Profits'].sum()


    top_industries_continent_na = grouped_na.sort_values(ascending=False).head(5)


    st.write(top_industries_continent_na)

    st.markdown("South America")
    sa_df = df[df['continent'] == 'South America']


    grouped_sa = sa_df.groupby('Industry')['Profits'].sum()


    top_industries_continent_sa = grouped_sa.sort_values(ascending=False).head(5)


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

elif analysis_task=='Conclusion':
    st.subheader("Conclusion")
    st.markdown("To conlude, I restate the research questions and answer them explicity based on my findings:")
    st.markdown("""
                - 122 companies out of 2000 companies were operating in loss. 
                    - Kuaishou Technology (China), Telecom Italia (Italy), and Carnival Corporation (USA) were the companies with highest losses.
                - What are the top companies ranked by sales, profits, assets and market value respectively? Which countries do they operate in?
                    - Listing only the top 3 for brevity:
                    - Sales: Walmart (USA), Amazon (USA), Saudi Arabian Oil Company (Saudi Aramco) (Saudi Arabia)
                    - Profits: Saudi Arabian Oil Company (Saudi Aramco) (Saudi Arabia), Apple (USA), Berkshire Hathaway (USA)
                    - Assets: ICBC, China Construction Bank, and Agricultural Bank of China; all operating in China
                    - Market Value: Apple (USA), Saudi Arabian Oil Company (Saudi Aramco) (Saudi Arabia), Microsoft (USA)
                - What are the top profit-making industries across continents?
                    - Africa: Media, Materials, Banking
                    - South America: Materials, Oil & GasOperations, Banking
                    - Asia: Banking, Oil & Gas Operations, Consumer Durables 
                    - Europe: Banking, Oil & Gas Operations, Consumer Durables 
                    - Oceania: Materials, Banking, Food Market
                    - North America: Diversified Financials, IT Software & Services, Banking
                - How are profits distributed across industries?
                    - The industries with highest profits were Banking and Oil&Gas Operations.
                    - The Semiconductors Industry had the largest interquantile range suggesting the most consistent profits in a single sector.
                    - IT Software & Services has the greatest profit-loss range.
                    - Industry operating with greatest losses is IT Software & Services.    
                - How are industries distributed in the Forbes ranking for this year?
                    - The most represented industries were Banking (290), Diversified Financials (146), and Construction (127).
                    - The least represented industries were Media (25), Hotels,Restaurants & Leisure (19), and Aerospace & Defence (18)
                """)

if __name__ == '__main__':
    main()    


    







