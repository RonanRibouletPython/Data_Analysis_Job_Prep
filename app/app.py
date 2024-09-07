import streamlit as st
import pandas as pd
import plotly.express as px  # Import Plotly Express

COLOR_PALETTE = {
    "Burgundy": "#803D3B",
    "Coffee": "#AF8260",
    "Cream": "#E4C59E",
}

# Dashboard Streamlit configuration MUST be the FIRST command
st.set_page_config(
    page_title="French Legislative Election Second Round Analysis",
    page_icon="french_flag_icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Loading and Preprocessing ---
@st.cache_data  # Cache the data to speed up app loading
def load_data():
    df = pd.read_csv("../Clean_Data/2024/clean_dataset_legislative_2024.csv", sep=";")
    df = df.rename(columns={"Votants": "Voters", 
                           "Abstentions": "Abstentionists", 
                           "Inscrits": "Registered",
                           "Exprimés": "Cast",
                           "Blancs": "Blank",
                           "Nuls": "Invalid",
                           })
    return df

df = load_data()

# --- Streamlit App ---

# Sidebar
st.sidebar.title('French Anticipated Legislative Election Second Round Analysis')
page = st.sidebar.selectbox("Go to", [
    "Homepage", 
    "National Analysis", 
    "Regional Analysis", 
    "Departmental Analysis",
    "City Analysis"
])

# Page functions
def page_home():
    st.title("Homepage")
    st.write("Welcome to the analysis of the French Anticipated Legislative Election of 2024")

def national_analysis():
    
    # Button to select analysis type
    analysis_type = st.selectbox("Select Analysis Type:", ["Vote Analysis", "Candidate Analysis"])
    
    if analysis_type == "Vote Analysis":
        st.title("French Legislative Election: National Voter Turnout and Ballot Analysis")

        total_registered = df["Registered"].sum()
        total_voters = df["Voters"].sum()
        total_abstentionists = df["Abstentionists"].sum()

        # --- Layout for Key Metrics ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Registered Voters", f"{total_registered:,}")
        with col2:
            st.metric("Total Voters", f"{total_voters:,}")
        with col3:
            st.metric("Total Abstentionists", f"{total_abstentionists:,}")

        st.markdown("---")  # Horizontal separator

        # --- Layout for Charts ---
        col4, col5 = st.columns(2)

        # --- Barplot using Plotly Express ---
        with col4:
            fig = px.bar(
                x=['Voters', 'Abstentionists'],
                y=[total_voters, total_abstentionists],
                color=['Voters', 'Abstentionists'],
                color_discrete_map={'Voters': COLOR_PALETTE["Burgundy"], 'Abstentionists': COLOR_PALETTE["Cream"]},
                title="Distribution of Voters and Abstentions"
            )
            fig.update_layout(
                xaxis_title="Voting Status",
                yaxis_title="Number of Registered People",
                yaxis_tickformat=",",
                plot_bgcolor='rgba(0,0,0,0)'  # Transparent background
            )
            st.plotly_chart(fig)

        # --- Pie Chart using Plotly Express ---
        with col5:
            fig = px.pie(
                values=[total_voters, total_abstentionists],
                names=['Voters', 'Abstentionists'],
                title="Voter Turnout Proportion",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Cream"]],
            )
            fig.update_traces(textinfo='percent+label', pull=[0.05, 0])
            st.plotly_chart(fig)
            
        total_cast = df["Cast"].sum()
        total_blank  = df["Blank"].sum()
        total_invalid  = df["Invalid"].sum()
            
            # --- Layout for Key Metrics ---
        col6, col7, col8 = st.columns(3)
        with col6:
            st.metric("Total Votes Cast", f"{total_cast:,}")
        with col7:
            st.metric("Total Votes Blank", f"{total_blank:,}")
        with col8:
            st.metric("Total Votes Invalid", f"{total_invalid:,}")
        
        st.markdown("---")  # Horizontal separator
        
        # --- Layout for Charts ---
        col9, col10 = st.columns(2)
        
        # --- Barplot using Plotly Express ---
        with col9:
            fig = px.bar(
                x=['Cast', 'Blank', 'Invalid'],
                y=[total_cast, total_blank, total_invalid],
                color=['Cast', 'Blank', 'Invalid'],
                color_discrete_map={'Cast': COLOR_PALETTE["Burgundy"], 'Blank': COLOR_PALETTE["Coffee"], "Invalid": COLOR_PALETTE["Cream"]},
                title="Distribution of Voters and Abstentions"
            )
            fig.update_layout(
                xaxis_title="Voting Status",
                yaxis_title="Number of Registered People",
                yaxis_tickformat=",",
                plot_bgcolor='rgba(0,0,0,0)'  # Transparent background
            )
            st.plotly_chart(fig)

        # --- Pie Chart using Plotly Express ---
        with col10:
            fig = px.pie(
                values=[total_cast, total_blank, total_invalid],
                names=['Cast', 'Blank', 'Invalid'],
                title="Voter Turnout Proportion",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Coffee"], COLOR_PALETTE["Cream"]],
            )
            fig.update_traces(textinfo='percent+label', pull=[0.05, 0])
            st.plotly_chart(fig)
    
    if analysis_type == "Candidate Analysis":
        st.title("French Legislative Election: Candidate Analysis")
        
        
    

def regionAnalysis():
    st.title("Analysis of a specific region")

def departmentAnalysis():
    st.title("Analysis of a specific department")
    
def cityAnalysis():
    st.title("Analysis of a specific city")

# Display selected page
if page == "Homepage":
    page_home()
elif page == "National Analysis":
    national_analysis()
elif page == "Regional Analysis":
    regionAnalysis()
elif page == "Departmental Analysis":
    departmentAnalysis()
elif page == "City Analysis":
    cityAnalysis()


