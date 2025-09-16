import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import seaborn as sns
import base64

# Set page config
st.set_page_config(page_title = "Mobile Trend Analysis", layout = "wide")
sns.set_style("ticks")

# Function to convert local image to base64
def get_base64_of_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    return encoded

# Apply background image using base64
img_path = "bg.jpeg"  
bg_image_base64 = get_base64_of_image(img_path)

st.markdown(
    f"""
    <style>
    /* Main App background */
    .stApp {{
        background-image: url("data:image/jpg;base64,{bg_image_base64}");
        background-size: cover;
        background-attachment: fixed;
        background-repeat: no-repeat;
        background-position: center;
    }}

    /* Main content container */
    .main > div {{
        background-color: rgba(255, 255, 255, 0.85);
        padding: 2rem;
        border-radius: 10px;
    }}

    /* Sidebar background */
    [data-testid="stSidebar"] {{
        background: rgba(0, 0, 0, 0.6); /* semi-transparent black */
        background-blend-mode: overlay;
    }}

    /* Sidebar text */
    [data-testid="stSidebar"] * {{
        color: white;  /* change to #222 or another color if needed */
        font-weight: 500;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# Load your CSV file
df = pd.read_csv("cleaned_mobile_data.csv", encoding='ISO-8859-1')
df['Model Name'] = df['Model Name'].str.lower().str.strip()
    
st.sidebar.title(":bar_chart: Mobile Insights")

# Initialize session state
st.session_state.setdefault("page", "Home")
st.session_state.setdefault("feature", "Price")
st.session_state.setdefault("country", "India")
st.session_state.setdefault("company", df['Company Name'].dropna().unique()[0])

# Sidebar navigation

pages = {
    ":house: Home": "Home",
    ":bar_chart: Price by Company": "Price by Company",
    ":chart_with_upwards_trend: Select Features to Analyze Mobile": "Select Features to Analyze Mobile",
    ":earth_asia: Country Comparison": "Country Comparison",
    ":star: Brand Popularity": "Brand Popularity",
    ":clipboard: Dataset": "Dataset"
}

for label, value in pages.items():
    if st.sidebar.button(label):
        st.session_state.page = value

# Current page
page = st.session_state.page

# Home Page
if page == "Home":
    # Title section
    st.markdown("""
        <div style='text-align: center; padding: 30px; border-radius: 10px;'>
            <h1 style='font-size: 3.2;'>📱Mobile Trend Analysis</h1>
            <h3 style='color: Black;'>Explore mobile phone trends by price, brand, and country</h3>
        </div>
    """, unsafe_allow_html=True)

    # Features section
    st.markdown("""
    <h2 style='font-size: 2rem;'>🔍What You Can Explore</h2>

    <h4 style='font-size: 1.3rem;'>Price Distribution by Company</h4>
    <p style='font-size: 1.1rem;'>Compare how different smartphone brands price their devices. See which brands dominate the <b>budget</b>, <b>mid-range</b>, or <b>premium</b> segment.</p>

    <h4 style='font-size: 1.3rem;'>Launch Price Trends Over Years</h4>
    <p style='font-size: 1.1rem;'>Visualize how average launch prices have changed from 2018 to 2023. Identify rising or falling trends and the tech impact over the years.</p>

    <h4 style='font-size: 1.3rem;'>Country-wise Analysis</h4>
    <p style='font-size: 1.1rem;'>Analyze how smartphone prices vary across countries like India, USA, UK, and more. Understand regional pricing strategies and brand preferences.</p>

    <h4 style='font-size: 1.3rem;'>Raw Dataset Access</h4>
    <p style='font-size: 1.1rem;'>View the full dataset with brand, model, launch year, and price. Filter and sort as you wish — perfect for deep exploration or custom analysis.</p>
    """, unsafe_allow_html=True)

    # Tools used section
    st.markdown("""
    <h2 style='font-size: 2.2rem;'>Tools Used in Project</h2>

    <ul style='font-size: 1.2rem; line-height: 2;'>
      <li>🐍 <b>Python</b> - Scripting and data manipulation</li>
      <li>📊 <b>Pandas</b> - Data cleaning and preprocessing</li>
      <li>🔢 <b>NumPy</b> - Numerical computations</li>
      <li>📈 <b>Matplotlib</b> & <b>Seaborn</b> - Creating visualizations</li>
      <li>🌐 <b>Streamlit</b> - Interactive web app framework</li>
      <li>🧭 <b>Streamlit Option Menu</b> - Sidebar navigation and UI</li>
    </ul>
    """, unsafe_allow_html=True)

    # Footer note
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; padding-top: 10px;'>
            <p style='color: Black;'><b>Your trend dashboard awaits! Choose a section from the sidebar 📱</b></p>
        </div>
    """, unsafe_allow_html=True)

# Price by Company
elif page == "Price by Company":
    st.title(":bar_chart: Price by Company")


    selected_company = st.selectbox("Choose a company:", df['Company Name'].unique())
    company_df = df[df['Company Name'] == selected_company]

    # Sort and limit to top 10 models
    top_models = company_df.sort_values(by='Launched Price (India)', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(12, 6))

    # Draw vertical barplot with Seaborn
    bars = sns.barplot(
        x='Model Name',
        y='Launched Price (India)',
        data=top_models,
        palette='crest'
    )

    # Add value labels on top of each bar
    for bar in bars.patches:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1000,  
            f"₹{int(height):,}",
            ha='center',
            va='bottom',
            fontsize=9,
            fontweight='semibold'
        )

    ax.set_title(f"Top 10 Most Expensive Models - {selected_company}", fontsize=16, fontweight='bold')
    ax.set_xlabel("")
    ax.set_ylabel("Price (INR)", fontsize=12)
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    sns.despine()  # Remove bordr

    plt.tight_layout()
    st.pyplot(fig)


# Select Features to Analyze Mobile
elif page == "Select Features to Analyze Mobile":
    feature = st.selectbox("Select Feature", ("Price", "RAM", "Battery", "Camera"))

    if feature == "Price":
        # Country selection
        country_options = {
            "India": "Launched Price (India)",
            "USA": "Price in INR (USA)",
            "China": "Price in INR (China)",
            "Pakistan": "Price in INR (Pakistan)",
            "Dubai": "Price in INR (Dubai)"
        }

        c1, c2 = st.columns([5, 5])
        with c1:
            selected_country = st.selectbox("Select Country", list(country_options.keys()))
            price_column = country_options[selected_country]
        with c2:
            company_names = sorted([name for name in df['Company Name'].dropna().unique()])
            selected_company = st.selectbox("Select Company", company_names)

        # Filter by selected company
        if selected_company:
            filtered_df = df[df['Company Name'] == selected_company]
        else:
            filtered_df = df.copy()

        # Trend plotting
        if 'Launched Year' in filtered_df.columns and price_column in filtered_df.columns:
            trend_df = filtered_df.groupby('Launched Year')[price_column].mean().reset_index()
            fig = px.line(trend_df, x='Launched Year', y=price_column, markers=True,
                          hover_data={price_column: True, 'Launched Year': True})
            st.plotly_chart(fig)
        else:
            st.error(f"'Launched Year' or '{price_column}' column not found in dataset.")

    elif feature == "RAM":
        fig, ax = plt.subplots(figsize = (6,3))
        ax.set_facecolor("black")  #inside plot area
        fig.patch.set_facecolor("black")  #outside plot area
        sns.lineplot(x="Launched Year", y="RAM", data=df, marker="o", markersize=4,ax=ax, ci = None)
        ax.set_title("RAM Trend Over Years",fontsize = 10,color = "white")
        ax.set_xlabel("Year",fontsize = 8,color = "white")
        ax.set_ylabel("RAM (GB)",fontsize = 8, color = "white")
        ax.tick_params(axis='x', labelsize=8,colors = "white")
        ax.tick_params(axis='y', labelsize=8,colors = "white")
        st.pyplot(fig)   
        
    elif feature == "Battery":
        fig = px.scatter(df,x='Launched Year',y='Battery Capacity',hover_data={'Battery Capacity': True, 'Launched Year': True},
        color_discrete_sequence=['cyan'],)
        fig.update_layout(plot_bgcolor="black",paper_bgcolor="black",font=dict(color="white"),xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor="gray", gridwidth=0.5))
        st.plotly_chart(fig)

    elif feature == "Camera":
        trend_df = df.groupby('Launched Year')["Front Camera"].mean().reset_index()
        fig = px.line(trend_df,x='Launched Year',y="Front Camera",markers=True,
        hover_data={"Front Camera": True, 'Launched Year': True})
        st.plotly_chart(fig)


# Country Comparison

elif page == "Country Comparison":
    st.title(":earth_africa: Country-wise Mobile Price Comparison")

    country_options = {
        "India": "Launched Price (India)",
        "USA": "Price in INR (USA)",
        "China": "Price in INR (China)",
        "Pakistan": "Price in INR (Pakistan)",
        "Dubai": "Price in INR (Dubai)"
    }

    selected_country = st.multiselect("Select Country", list(country_options.keys()))

    if selected_country:
        # Create a new DataFrame in long format
        comparison_data = pd.DataFrame()

        for country in selected_country:
            price_column = country_options[country]
            temp_df = df[[price_column]].copy()
            temp_df = temp_df.rename(columns={price_column: "Price (INR)"})
            temp_df["Country"] = country
            comparison_data = pd.concat([comparison_data, temp_df], ignore_index=True)

        # Calculate average price per country
        avg_price = comparison_data.groupby('Country')['Price (INR)'].mean().reset_index()

        # Bubble Chart
        fig, ax = plt.subplots(figsize=(8,4))
        
        scatter = ax.scatter(
            x=avg_price['Country'],
            y=avg_price['Price (INR)'],
            s=avg_price['Price (INR)'] / 12,  # bubble size
            alpha=0.6,
            c=avg_price['Price (INR)'],
            cmap="coolwarm",
            edgecolors="w"
        )

        ax.set_title("Average Price by Country (Bubble Chart)")
        ax.set_xlabel("Country")
        ax.set_ylabel("Average Price (INR)")

        # Add text labels inside bubbles
        for i, row in avg_price.iterrows():
            ax.text(row['Country'], row['Price (INR)'], 
                    f"{int(row['Price (INR)'])}", 
                    ha="center", va="center", color="black", fontsize=8)

        #Fix: adjust limits so bubbles are not cut
        ax.margins(x=0.3, y=0.2)  
        plt.tight_layout()

        st.pyplot(fig)

    else:
        st.info("Please select at least one country to compare.")

elif page == "Brand Popularity":
    brand_count = df['Company Name'].value_counts().reset_index()
    brand_count.columns = ['Brand', 'Number of Models']
    fig = px.pie(brand_count,names='Brand', values='Number of Models', title='Brand Popularity by Number of Models',
    hole=0.3,color_discrete_sequence=px.colors.qualitative.Pastel,hover_data=['Number of Models'])
    fig.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig, use_container_width=True)
 
    st.markdown("### Brand Model Count Details")
    st.dataframe(brand_count.sort_values(by='Number of Models', ascending=False).reset_index(drop=True))
# Dataset
elif page == "Dataset":
    st.title(":clipboard: Full Dataset")
    st.dataframe(df)
