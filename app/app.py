import streamlit as st
import pandas as pd
import plotly.express as px
import os

COLOR_PALETTE = {
    "Burgundy": "#803D3B",
    "Coffee": "#AF8260",
    "Cream": "#E4C59E",
}

# Color palette for party tendencies
palette_nuances = {
                    'Gauche-Radicale': '#E4572E',
                    'Gauche': '#FE4A49', 
                    "Centre": "#B1EDE8", 
                    "Centre-Droite": "#4EA5FF",
                    "Droite": "#207BFF",
                    "Extrême-Droite": "#053C5E",
                    "Autres": "#773344",  
                }

# Use mapping to add the regions of the departement
departements_regions = {
    "01": "Auvergne-Rhône-Alpes",
    "02": "Hauts-de-France",
    "03": "Auvergne-Rhône-Alpes",
    "04": "Provence-Alpes-Côte d'Azur",
    "05": "Provence-Alpes-Côte d'Azur",
    "06": "Provence-Alpes-Côte d'Azur",
    "07": "Auvergne-Rhône-Alpes",
    "08": "Grand Est",
    "09": "Occitanie",
    "10": "Grand Est",
    "11": "Occitanie",
    "12": "Occitanie",
    "13": "Provence-Alpes-Côte d'Azur",
    "14": "Normandie",
    "15": "Auvergne-Rhône-Alpes",
    "16": "Nouvelle-Aquitaine",
    "17": "Nouvelle-Aquitaine",
    "18": "Centre-Val de Loire",
    "19": "Nouvelle-Aquitaine",
    "2A": "Corse",
    "2B": "Corse",
    "21": "Bourgogne-Franche-Comté",
    "22": "Bretagne",
    "23": "Nouvelle-Aquitaine",
    "24": "Nouvelle-Aquitaine",
    "25": "Bourgogne-Franche-Comté",
    "26": "Auvergne-Rhône-Alpes",
    "27": "Normandie",
    "28": "Centre-Val de Loire",
    "29": "Bretagne",
    "30": "Occitanie",
    "31": "Occitanie",
    "32": "Occitanie",
    "33": "Nouvelle-Aquitaine",
    "34": "Occitanie",
    "35": "Bretagne",
    "36": "Centre-Val de Loire",
    "37": "Centre-Val de Loire",
    "38": "Auvergne-Rhône-Alpes",
    "39": "Bourgogne-Franche-Comté",
    "40": "Nouvelle-Aquitaine",
    "41": "Centre-Val de Loire",
    "42": "Auvergne-Rhône-Alpes",
    "43": "Auvergne-Rhône-Alpes",
    "44": "Pays de la Loire",
    "45": "Centre-Val de Loire",
    "46": "Occitanie",
    "47": "Nouvelle-Aquitaine",
    "48": "Occitanie",
    "49": "Pays de la Loire",
    "50": "Normandie",
    "51": "Grand Est",
    "52": "Grand Est",
    "53": "Pays de la Loire",
    "54": "Grand Est",
    "55": "Grand Est",
    "56": "Bretagne",
    "57": "Grand Est",
    "58": "Bourgogne-Franche-Comté",
    "59": "Hauts-de-France",
    "60": "Hauts-de-France",
    "61": "Normandie",
    "62": "Hauts-de-France",
    "63": "Auvergne-Rhône-Alpes",
    "64": "Nouvelle-Aquitaine",
    "65": "Occitanie",
    "66": "Occitanie",
    "67": "Grand Est",
    "68": "Grand Est",
    "69": "Auvergne-Rhône-Alpes",
    "70": "Bourgogne-Franche-Comté",
    "71": "Bourgogne-Franche-Comté",
    "72": "Pays de la Loire",
    "73": "Auvergne-Rhône-Alpes",
    "74": "Auvergne-Rhône-Alpes",
    "75": "Île-de-France",
    "76": "Normandie",
    "77": "Île-de-France",
    "78": "Île-de-France",
    "79": "Nouvelle-Aquitaine",
    "80": "Hauts-de-France",
    "81": "Occitanie",
    "82": "Occitanie",
    "83": "Provence-Alpes-Côte d'Azur",
    "84": "Provence-Alpes-Côte d'Azur",
    "85": "Pays de la Loire",
    "86": "Nouvelle-Aquitaine",
    "87": "Nouvelle-Aquitaine",
    "88": "Grand Est",
    "89": "Bourgogne-Franche-Comté",
    "90": "Bourgogne-Franche-Comté",
    "91": "Île-de-France",
    "92": "Île-de-France",
    "93": "Île-de-France",
    "94": "Île-de-France",
    "95": "Île-de-France",
    "971": "Outre-Mer",
    "972": "Outre-Mer",
    "973": "Outre-Mer",
    "974": "Outre-Mer",
    "975": "Outre-Mer",
    "976": "Outre-Mer",
    "987": "Outre-Mer",
    "988": "Outre-Mer",
    "ZX": "Outre-Mer",
    "ZZ": "Étranger",  
}


# --- Streamlit Page configuration ---
st.set_page_config(
    page_title="French Legislative Election Second Round Analysis",
    page_icon="french_flag_icon.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Data Loading and Preprocessing ---
@st.cache_data  # Cache the data to speed up app loading
def load_data_from_csv(file_path: str, separator: str)-> pd.DataFrame:
    if not os.path.splitext(file_path)[1].lower() == '.csv':
        raise ValueError(f"Invalid file type: {file_path} is not a CSV file.")
    
    df = pd.read_csv(file_path, sep=separator)

    return df

df = load_data_from_csv(file_path="clean_dataset_legislative_2024.csv", separator=";")
df = df.rename(columns={"Votants": "Voters", 
                        "Abstentions": "Abstentions", 
                        "Inscrits": "Registered",
                        "Exprimés": "Cast",
                        "Blancs": "Blank",
                        "Nuls": "Invalid",
                    })

# Adding a "0" value before the one digit numbers
df["Code_département"] = df["Code_département"].astype(str).apply(lambda x: "0" + x if len(x) == 1 else x)
# Create the new Region column with mapping
df['Libellé_Région'] = df['Code_département'].map(departements_regions)


df_unique_candidates = load_data_from_csv("candidates_legislative_2024.csv", separator=";")

# DataFrame with the candidates elected
df_elected = df_unique_candidates[df_unique_candidates['Elu'] == True]

df_candidates = load_data_from_csv("candidates.csv", separator=";")

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
    st.write("Welcome to the analysis of Second Turn Confrontations of the French Anticipated Legislative Election of 2024!")
    
    

def national_analysis():
    
    # Button to select analysis type
    analysis_type = st.selectbox("Select Analysis Type:", ["Vote Analysis", "Candidate Analysis", "Result Analysis"])
    
    if analysis_type == "Vote Analysis":
        st.title("French Legislative Election: National Voter Turnout and Ballot Analysis")

        total_registered = df["Registered"].sum()
        total_voters = df["Voters"].sum()
        total_abstentions = df["Abstentions"].sum()
        
        # Display the subtitle of the Voter Turnout
        st.subheader("National Voter Turnout Analysis")

        # --- Layout for Key Metrics ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Registered Voters", f"{total_registered:,}")
        with col2:
            st.metric("Total Voters", f"{total_voters:,}")
        with col3:
            st.metric("Total Abstentions", f"{total_abstentions:,}")

        st.markdown("---")  # Horizontal separator

        # --- Layout for Charts ---
        col4, col5 = st.columns(2)

        # --- Barplot using Plotly Express ---
        with col4:
            fig = px.bar(
                x=['Voters', 'Abstentions'],
                y=[total_voters, total_abstentions],
                color=['Voters', 'Abstentions'],
                color_discrete_map={'Voters': COLOR_PALETTE["Burgundy"], 'Abstentions': COLOR_PALETTE["Cream"]},
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
                values=[total_voters, total_abstentions],
                names=['Voters', 'Abstentions'],
                title="Voter Turnout Proportion",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Cream"]],
                hole=0.3 
            )
            fig.update_traces(textinfo='percent+label',)
            st.plotly_chart(fig)
            
        total_cast = df["Cast"].sum()
        total_blank  = df["Blank"].sum()
        total_invalid  = df["Invalid"].sum()
        
        # Display the subtitle of the Ballot Analysis
        st.subheader("National Ballot Analysis")
            
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
                title="Distribution of Cast, Blank, and Invalid Votes"
            )
            fig.update_layout(
                xaxis_title="Vote Status",
                yaxis_title="Number of Votes",
                yaxis_tickformat=",",
                plot_bgcolor='rgba(0,0,0,0)'  # Transparent background
            )
            st.plotly_chart(fig)

        # --- Pie Chart using Plotly Express ---
        with col10:
            fig = px.pie(
                values=[total_cast, total_blank, total_invalid],
                names=['Cast', 'Blank', 'Invalid'],
                title="Proportion of Cast, Blank, and Invalid Votes",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Coffee"], COLOR_PALETTE["Cream"]],
                hole=0.3
            )
            fig.update_traces(textinfo='percent+label',)
            st.plotly_chart(fig)
    
    if analysis_type == "Candidate Analysis":
        st.title("French Legislative Election: National Candidate Analysis")

        tendencies_plot_order = ['Gauche-Radicale','Gauche', 'Centre', 'Centre-Droite', 'Droite', 'Extrême-Droite', 'Autres']
        total_candidates = df_unique_candidates["Nom_complet"].value_counts().sum()
        sex_counts = df_unique_candidates["Sexe"].value_counts()
        male_candidates = sex_counts.get("MASCULIN", 0)
        female_candidates = sex_counts.get("FEMININ", 0)
        tendency_count = df_unique_candidates["Tendency"].value_counts()
        tendency_by_gender = df_unique_candidates.groupby('Sexe')['Nuance',].value_counts().unstack(fill_value=0)
        
        # Display the subtitle of the Ballot Analysis
        st.subheader("Candidate Gender Analysis")
        
        # --- Layout for Key Metrics ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Candidates", f"{total_candidates:,}")
        with col2:
            st.metric("Total Male Candidates", f"{male_candidates:,}")
        with col3:
            st.metric("Total Female Candidates", f"{female_candidates:,}")

        st.markdown("---")  # Horizontal separator
        
        # --- Layout for Charts ---
        col4, col5 = st.columns(2)

        # --- Barplot using Plotly Express ---
        with col4:
            fig = px.bar(
                x=['Male', 'Female'],
                y=[male_candidates, female_candidates],
                color=['Male', 'Female'],
                color_discrete_map={'Male': COLOR_PALETTE["Burgundy"], 'Female': COLOR_PALETTE["Cream"]},
                title="Distribution of Candidates Gender"
            )
            fig.update_layout(
                xaxis_title="Gender of the Candidates",
                yaxis_title="Number of Candidates",
                yaxis_tickformat=",",
                plot_bgcolor='rgba(0,0,0,0)'  # Transparent background
            )
            st.plotly_chart(fig)

        # --- Pie Chart using Plotly Express ---
        with col5:
            fig = px.pie(
                values=[male_candidates, female_candidates],
                names=['Male', 'Female'],
                title="Proportion of Candidates Genders",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Cream"]],
                hole=0.3
            )

            fig.update_traces(textinfo='percent+label',)
            st.plotly_chart(fig)    
        
        # Display the subtitle of the Candidate Affiliations
        st.subheader("Overview of French Legislative Candidate Affiliations")
        
        total_parties = df_unique_candidates["Nuance"].nunique()
        st.metric("Total Number of Parties or Political Alliances", f"{total_parties}")
        
        st.markdown("---")  # Horizontal separator
        
        fig = px.histogram(df_unique_candidates, 
                        x="Nuance", 
                        color="Tendency", 
                        color_discrete_map=palette_nuances,
                        title="Distribution of French Legislative Candidates by Party and Tendency",
                        category_orders={"Tendency": tendencies_plot_order})

        # Customize layout
        fig.update_layout(
            xaxis_title="Political parties",
            yaxis_title="Number of Candidates",
            showlegend=True,
            plot_bgcolor='white',
            legend_title_text='Tendencies'
        )

        # Add text annotations for counts
        fig.update_traces(texttemplate='%{y}', textposition='outside')

        # Display the chart using Streamlit
        st.plotly_chart(fig)
        
        # Create the semi-donut chart
        fig = px.pie(
            tendency_count, 
            values='count', 
            names=tendency_count.index,
            color=tendency_count.index,
            color_discrete_map=palette_nuances,  
            hole=0.5, 
            title='Distribution of Political Tendencies' ,
            category_orders={"Tendency": tendencies_plot_order},
            
        ) 
        
        fig.update_layout(
            showlegend=True,  # Display the legend
            legend_title_text='Tendencies'
        )
        fig.update_traces(textinfo='percent',
                        rotation=180,
                        )  

        
        # Display the chart using Streamlit
        st.plotly_chart(fig)
        
        st.markdown("---")  # Horizontal separator
        
    if analysis_type == "Result Analysis":
        st.title("French Legislative Election: National Result Analysis")

        tendencies_plot_order = ['Gauche-Radicale','Gauche', 'Centre', 'Centre-Droite', 'Droite', 'Extrême-Droite', 'Autres']
        total_mp = df_elected["Nom_complet"].value_counts().sum()
        male_mp = df_elected["Sexe"].value_counts()["MASCULIN"]
        female_mp = df_elected["Sexe"].value_counts()["FEMININ"]
        tendency_count = df_elected["Tendency"].value_counts()
        tendency_by_gender = df_elected.groupby('Sexe')['Nuance',].value_counts().unstack(fill_value=0)
        
        # Display the subtitle of the Ballot Analysis
        st.subheader("Elected MP Gender Analysis")
        
        # --- Layout for Key Metrics ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Elected MP", f"{total_mp:,}")
        with col2:
            st.metric("Total Male Elected MP", f"{male_mp:,}")
        with col3:
            st.metric("Total Female Elected MP", f"{female_mp:,}")

        st.markdown("---")  # Horizontal separator
        
        # --- Layout for Charts ---
        col4, col5 = st.columns(2)

        # --- Barplot using Plotly Express ---
        with col4:
            fig = px.bar(
                x=['Male', 'Female'],
                y=[male_mp, female_mp],
                color=['Male', 'Female'],
                color_discrete_map={'Male': COLOR_PALETTE["Burgundy"], 'Female': COLOR_PALETTE["Cream"]},
                title="Distribution of Elected MP Gender"
            )
            fig.update_layout(
                xaxis_title="Gender of the Elected MP",
                yaxis_title="Number of Elected MP",
                yaxis_tickformat=",",
                plot_bgcolor='rgba(0,0,0,0)'  # Transparent background
            )
            st.plotly_chart(fig)

        # --- Pie Chart using Plotly Express ---
        with col5:
            fig = px.pie(
                values=[male_mp, female_mp],
                names=['Male', 'Female'],
                title="Proportion of Elected MP Genders",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Cream"]],
                hole=0.3
            )

            fig.update_traces(textinfo='percent+label',)
            st.plotly_chart(fig)    
        
        # Display the subtitle of the Candidate Affiliations
        st.subheader("Overview of French Legislative Elected MP Affiliations")
        
        total_parties = df_elected["Nuance"].nunique()
        st.metric("Total Number of Parties or Political Alliances", f"{total_parties}")
        
        st.markdown("---")  # Horizontal separator
        
        fig = px.histogram(df_elected, 
                        x="Nuance", 
                        color="Tendency", 
                        color_discrete_map=palette_nuances,
                        title="Distribution of French Legislative Elected MP by Party and Tendency",
                        category_orders={"Tendency": tendencies_plot_order})

        # Customize layout
        fig.update_layout(
            xaxis_title="Political parties",
            yaxis_title="Number of Elected MP",
            showlegend=True,
            plot_bgcolor='white',
            legend_title_text='Tendencies'
        )

        # Add text annotations for counts
        fig.update_traces(texttemplate='%{y}', textposition='outside')

        # Display the chart using Streamlit
        st.plotly_chart(fig)
        
        # Create the semi-donut chart
        fig = px.pie(
            tendency_count, 
            values='count', 
            names=tendency_count.index,
            color=tendency_count.index,
            color_discrete_map=palette_nuances,  
            hole=0.5, 
            title='Distribution of Political Tendencies' ,
            category_orders={"Tendency": tendencies_plot_order},
            
        ) 
        
        fig.update_layout(
            showlegend=True,  # Display the legend
            legend_title_text='Tendencies'
        )
        fig.update_traces(textinfo='percent', 
                        rotation=180,
                        )  

        
        # Display the chart using Streamlit
        st.plotly_chart(fig)
        
        st.markdown("---")  # Horizontal separator
        
        

def regionAnalysis():
    regions = df['Libellé_Région'].unique()
    selected_region = st.selectbox("Select Region", regions)
    
    st.title("Analysis of a specific region")
    
    # Filter the DataFrame
    filtered_df = df[df['Libellé_Région'] == selected_region]
    
    filtered_df = filtered_df.rename(columns={"Votants": "Voters", 
                        "Abstentions": "Abstentions", 
                        "Inscrits": "Registered",
                        "Exprimés": "Cast",
                        "Blancs": "Blank",
                        "Nuls": "Invalid",
                    })
    
    filtered_df_unique_candidates = df_unique_candidates[df_unique_candidates["Région"]==selected_region]
    
        # Button to select analysis type
    analysis_type = st.selectbox("Select Analysis Type:", ["Vote Analysis", "Candidate Analysis", "Result Analysis"])
    
    if analysis_type == "Vote Analysis":
        st.title(f"French Legislative Election: Regional Voter Turnout and Ballot Analysis in {selected_region}")

        total_registered = filtered_df["Registered"].sum()
        total_voters = filtered_df["Voters"].sum()
        total_abstentions = filtered_df["Abstentions"].sum()
        
        # Display the subtitle of the Voter Turnout
        st.subheader(f"Regional Voter Turnout Analysis in {selected_region}")

        # --- Layout for Key Metrics ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Registered Voters", f"{total_registered:,}")
        with col2:
            st.metric("Total Voters", f"{total_voters:,}")
        with col3:
            st.metric("Total Abstentions", f"{total_abstentions:,}")

        st.markdown("---")  # Horizontal separator

        # --- Layout for Charts ---
        col4, col5 = st.columns(2)

        # --- Barplot using Plotly Express ---
        with col4:
            fig = px.bar(
                x=['Voters', 'Abstentions'],
                y=[total_voters, total_abstentions],
                color=['Voters', 'Abstentions'],
                color_discrete_map={'Voters': COLOR_PALETTE["Burgundy"], 'Abstentions': COLOR_PALETTE["Cream"]},
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
                values=[total_voters, total_abstentions],
                names=['Voters', 'Abstentions'],
                title="Voter Turnout Proportion",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Cream"]],
                hole=0.3 
            )
            fig.update_traces(textinfo='percent+label',)
            st.plotly_chart(fig)
            
        total_cast = filtered_df["Cast"].sum()
        total_blank  = filtered_df["Blank"].sum()
        total_invalid  = filtered_df["Invalid"].sum()
        
        # Display the subtitle of the Ballot Analysis
        st.subheader(f"Regional Ballot Analysis in {selected_region}")
            
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
                title="Distribution of Cast, Blank, and Invalid Votes"
            )
            fig.update_layout(
                xaxis_title="Vote Status",
                yaxis_title="Number of Votes",
                yaxis_tickformat=",",
                plot_bgcolor='rgba(0,0,0,0)'  # Transparent background
            )
            st.plotly_chart(fig)

        # --- Pie Chart using Plotly Express ---
        with col10:
            fig = px.pie(
                values=[total_cast, total_blank, total_invalid],
                names=['Cast', 'Blank', 'Invalid'],
                title="Proportion of Cast, Blank, and Invalid Votes",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Coffee"], COLOR_PALETTE["Cream"]],
                hole=0.3
            )
            fig.update_traces(textinfo='percent+label',)
            st.plotly_chart(fig)
    
    if analysis_type == "Candidate Analysis":
        st.title(f"French Legislative Election: Regional Candidate Analysis in {selected_region}")

        tendencies_plot_order = ['Gauche-Radicale','Gauche', 'Centre', 'Centre-Droite', 'Droite', 'Extrême-Droite', 'Autres']
        total_candidates = filtered_df_unique_candidates["Nom_complet"].value_counts().sum()
        sex_counts = filtered_df_unique_candidates["Sexe"].value_counts()
        male_candidates = sex_counts.get("MASCULIN", 0)
        female_candidates = sex_counts.get("FEMININ", 0)
        tendency_count = filtered_df_unique_candidates["Tendency"].value_counts()
        tendency_by_gender = filtered_df_unique_candidates.groupby('Sexe')['Nuance',].value_counts().unstack(fill_value=0)
        
        # Display the subtitle of the Ballot Analysis
        st.subheader("Candidate Gender Analysis")
        
        # --- Layout for Key Metrics ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Candidates", f"{total_candidates:,}")
        with col2:
            st.metric("Total Male Candidates", f"{male_candidates:,}")
        with col3:
            st.metric("Total Female Candidates", f"{female_candidates:,}")

        st.markdown("---")  # Horizontal separator
        
        # --- Layout for Charts ---
        col4, col5 = st.columns(2)

        # --- Barplot using Plotly Express ---
        with col4:
            fig = px.bar(
                x=['Male', 'Female'],
                y=[male_candidates, female_candidates],
                color=['Male', 'Female'],
                color_discrete_map={'Male': COLOR_PALETTE["Burgundy"], 'Female': COLOR_PALETTE["Cream"]},
                title="Distribution of Candidates Gender"
            )
            fig.update_layout(
                xaxis_title="Gender of the Candidates",
                yaxis_title="Number of Candidates",
                yaxis_tickformat=",",
                plot_bgcolor='rgba(0,0,0,0)'  # Transparent background
            )
            st.plotly_chart(fig)

        # --- Pie Chart using Plotly Express ---
        with col5:
            fig = px.pie(
                values=[male_candidates, female_candidates],
                names=['Male', 'Female'],
                title="Proportion of Candidates Genders",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Cream"]],
                hole=0.3
            )

            fig.update_traces(textinfo='percent+label',)
            st.plotly_chart(fig)    
        
        # Display the subtitle of the Candidate Affiliations
        st.subheader("Overview of French Legislative Candidate Affiliations")
        
        total_parties = filtered_df_unique_candidates["Nuance"].nunique()
        st.metric("Total Number of Parties or Political Alliances", f"{total_parties}")
        
        st.markdown("---")  # Horizontal separator
        
        fig = px.histogram(filtered_df_unique_candidates, 
                        x="Nuance", 
                        color="Tendency", 
                        color_discrete_map=palette_nuances,
                        title="Distribution of French Legislative Candidates by Party and Tendency",
                        category_orders={"Tendency": tendencies_plot_order})

        # Customize layout
        fig.update_layout(
            xaxis_title="Political parties",
            yaxis_title="Number of Candidates",
            showlegend=True,
            plot_bgcolor='white',
            legend_title_text='Tendencies'
        )

        # Add text annotations for counts
        fig.update_traces(texttemplate='%{y}', textposition='outside')

        # Display the chart using Streamlit
        st.plotly_chart(fig)
        
        # Create the semi-donut chart
        fig = px.pie(
            tendency_count, 
            values='count', 
            names=tendency_count.index,
            color=tendency_count.index,
            color_discrete_map=palette_nuances,  
            hole=0.5, 
            title='Distribution of Political Tendencies' ,
            category_orders={"Tendency": tendencies_plot_order},
            
        ) 
        
        fig.update_layout(
            showlegend=True,  # Display the legend
            legend_title_text='Tendencies'
        )
        fig.update_traces(textinfo='percent',
                        rotation=180,
                        )  

        
        # Display the chart using Streamlit
        st.plotly_chart(fig)
        
        st.markdown("---")  # Horizontal separator
        
    if analysis_type == "Result Analysis":
        
        
        filtered_df_elected_region = df_elected[df_elected["Région"]==selected_region]
        
        st.title(f"French Legislative Election: Regional Result Analysis in {selected_region}")

        tendencies_plot_order = ['Gauche-Radicale','Gauche', 'Centre', 'Centre-Droite', 'Droite', 'Extrême-Droite', 'Autres']
        total_mp = filtered_df_elected_region["Nom_complet"].value_counts().sum()
        tendency_count = filtered_df_elected_region["Tendency"].value_counts()
        tendency_by_gender = filtered_df_elected_region.groupby('Sexe')['Nuance',].value_counts().unstack(fill_value=0)
        sex_counts = filtered_df_elected_region["Sexe"].value_counts()
        male_mp = sex_counts.get("MASCULIN", 0)
        female_mp = sex_counts.get("FEMININ", 0)
        # Display the subtitle of the Ballot Analysis
        st.subheader("Elected MP Gender Analysis")
        
        # --- Layout for Key Metrics ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Elected MP", f"{total_mp:,}")
        with col2:
            st.metric("Total Male Elected MP", f"{male_mp:,}")
        with col3:
            st.metric("Total Female Elected MP", f"{female_mp:,}")

        st.markdown("---")  # Horizontal separator
        
        # --- Layout for Charts ---
        col4, col5 = st.columns(2)

        # --- Barplot using Plotly Express ---
        with col4:
            fig = px.bar(
                x=['Male', 'Female'],
                y=[male_mp, female_mp],
                color=['Male', 'Female'],
                color_discrete_map={'Male': COLOR_PALETTE["Burgundy"], 'Female': COLOR_PALETTE["Cream"]},
                title="Distribution of Elected MP Gender"
            )
            fig.update_layout(
                xaxis_title="Gender of the Elected MP",
                yaxis_title="Number of Elected MP",
                yaxis_tickformat=",",
                plot_bgcolor='rgba(0,0,0,0)'  # Transparent background
            )
            st.plotly_chart(fig)

        # --- Pie Chart using Plotly Express ---
        with col5:
            fig = px.pie(
                values=[male_mp, female_mp],
                names=['Male', 'Female'],
                title="Proportion of Elected MP Genders",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Cream"]],
                hole=0.3
            )

            fig.update_traces(textinfo='percent+label',)
            st.plotly_chart(fig)    
        
        # Display the subtitle of the Candidate Affiliations
        st.subheader("Overview of French Legislative Elected MP Affiliations")
        
        total_parties = filtered_df_elected_region["Nuance"].nunique()
        st.metric("Total Number of Parties or Political Alliances", f"{total_parties}")
        
        st.markdown("---")  # Horizontal separator
        
        fig = px.histogram(filtered_df_elected_region, 
                        x="Nuance", 
                        color="Tendency", 
                        color_discrete_map=palette_nuances,
                        title="Distribution of French Legislative Elected MP by Party and Tendency",
                        category_orders={"Tendency": tendencies_plot_order})

        # Customize layout
        fig.update_layout(
            xaxis_title="Political parties",
            yaxis_title="Number of Elected MP",
            showlegend=True,
            plot_bgcolor='white',
            legend_title_text='Tendencies'
        )

        # Add text annotations for counts
        fig.update_traces(texttemplate='%{y}', textposition='outside')

        # Display the chart using Streamlit
        st.plotly_chart(fig)
        
        # Create the semi-donut chart
        fig = px.pie(
            tendency_count, 
            values='count', 
            names=tendency_count.index,
            color=tendency_count.index,
            color_discrete_map=palette_nuances,  
            hole=0.5, 
            title='Distribution of Political Tendencies' ,
            category_orders={"Tendency": tendencies_plot_order},
            
        ) 
        
        fig.update_layout(
            showlegend=True,  # Display the legend
            legend_title_text='Tendencies'
        )
        fig.update_traces(textinfo='percent',
                        rotation=180,
                        )  

        
        # Display the chart using Streamlit
        st.plotly_chart(fig)
        
        st.markdown("---")  # Horizontal separator

def departmentAnalysis():
    regions = df['Libellé_Région'].unique()
    selected_region = st.selectbox("Select Region", regions)
    
    filtered_region_df = df[df['Libellé_Région'] == selected_region]
    
    departements = filtered_region_df['Libellé_département'].unique()
    selected_departement = st.selectbox("Select Region", departements)
    
    # Filter the DataFrame
    filtered_department_df = df[df['Libellé_département'] == selected_departement]
    
    filtered_department_df = filtered_department_df.rename(columns={"Votants": "Voters", 
                        "Abstentions": "Abstentions", 
                        "Inscrits": "Registered",
                        "Exprimés": "Cast",
                        "Blancs": "Blank",
                        "Nuls": "Invalid",
                    })
    
    
    st.title(f"Analysis of a specific department")
    
    # Button to select analysis type
    analysis_type = st.selectbox("Select Analysis Type:", ["Vote Analysis", "Candidate Analysis", "Result Analysis"])
    
    if analysis_type == "Vote Analysis":
        st.title(f"French Legislative Election: Departmental Voter Turnout and Ballot Analysis in {selected_departement}")

        total_registered = filtered_department_df["Registered"].sum()
        total_voters = filtered_department_df["Voters"].sum()
        total_abstentions = filtered_department_df["Abstentions"].sum()
        
        # Display the subtitle of the Voter Turnout
        st.subheader(f"Departmental Voter Turnout Analysis in {selected_departement}")

        # --- Layout for Key Metrics ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Registered Voters", f"{total_registered:,}")
        with col2:
            st.metric("Total Voters", f"{total_voters:,}")
        with col3:
            st.metric("Total Abstentions", f"{total_abstentions:,}")

        st.markdown("---")  # Horizontal separator

        # --- Layout for Charts ---
        col4, col5 = st.columns(2)

        # --- Barplot using Plotly Express ---
        with col4:
            fig = px.bar(
                x=['Voters', 'Abstentions'],
                y=[total_voters, total_abstentions],
                color=['Voters', 'Abstentions'],
                color_discrete_map={'Voters': COLOR_PALETTE["Burgundy"], 'Abstentions': COLOR_PALETTE["Cream"]},
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
                values=[total_voters, total_abstentions],
                names=['Voters', 'Abstentions'],
                title="Voter Turnout Proportion",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Cream"]],
                hole=0.3 
            )
            fig.update_traces(textinfo='percent+label', )
            st.plotly_chart(fig)
            
        total_cast = filtered_department_df["Cast"].sum()
        total_blank  = filtered_department_df["Blank"].sum()
        total_invalid  = filtered_department_df["Invalid"].sum()
        
        # Display the subtitle of the Ballot Analysis
        st.subheader(f"Depatmental Ballot Analysis in {selected_departement}")
            
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
                title="Distribution of Cast, Blank, and Invalid Votes"
            )
            fig.update_layout(
                xaxis_title="Vote Status",
                yaxis_title="Number of Votes",
                yaxis_tickformat=",",
                plot_bgcolor='rgba(0,0,0,0)'  # Transparent background
            )
            st.plotly_chart(fig)

        # --- Pie Chart using Plotly Express ---
        with col10:
            fig = px.pie(
                values=[total_cast, total_blank, total_invalid],
                names=['Cast', 'Blank', 'Invalid'],
                title="Proportion of Cast, Blank, and Invalid Votes",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Coffee"], COLOR_PALETTE["Cream"]],
                hole=0.3
            )
            fig.update_traces(textinfo='percent+label', )
            st.plotly_chart(fig)
    
    if analysis_type == "Candidate Analysis":
        st.title(f"French Legislative Election: Departmental Candidate Turnout Analysis in {selected_departement}")
        # Filter the DataFrame
        new_filtered_department_df = df_candidates[df_candidates['Département'] == selected_departement]
        new_filtered_department_df = new_filtered_department_df.drop_duplicates(subset='Nom_complet', keep="first")
        total_candidates = new_filtered_department_df["Nom_complet"].nunique()
        
        tendencies_plot_order = ['Gauche-Radicale','Gauche', 'Centre', 'Centre-Droite', 'Droite', 'Extrême-Droite', 'Autres']
        tendency_count = new_filtered_department_df["Tendency"].value_counts()
        sex_counts = new_filtered_department_df["Sexe"].value_counts()
        male_candidates = sex_counts.get("MASCULIN", 0)
        female_candidates = sex_counts.get("FEMININ", 0)
        # Display the subtitle of the Ballot Analysis
        st.subheader("Candidate Gender Analysis")
        
        # --- Layout for Key Metrics ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Candidates", f"{total_candidates:,}")
        with col2:
            st.metric("Total Male Candidates", f"{male_candidates:,}")
            pass
        with col3:
            st.metric("Total Female Candidates", f"{female_candidates:,}")
            pass
        st.markdown("---")  # Horizontal separator
        
        # --- Layout for Charts ---
        col4, col5 = st.columns(2)
        # --- Barplot using Plotly Express ---
        with col4:
            fig = px.bar(
                x=['Male', 'Female'],
                y=[male_candidates, female_candidates],
                color=['Male', 'Female'],
                color_discrete_map={'Male': COLOR_PALETTE["Burgundy"], 'Female': COLOR_PALETTE["Cream"]},
                title="Distribution of Candidates Gender"
            )
            fig.update_layout(
                xaxis_title="Gender of the Candidates",
                yaxis_title="Number of Candidates",
                yaxis_tickformat=",",
                plot_bgcolor='rgba(0,0,0,0)'  # Transparent background
            )
            st.plotly_chart(fig)

        # --- Pie Chart using Plotly Express ---
        with col5:
            fig = px.pie(
                values=[male_candidates, female_candidates],
                names=['Male', 'Female'],
                title="Proportion of Candidates Genders",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Cream"]],
                hole=0.3
            )

            fig.update_traces(textinfo='percent+label',)
            st.plotly_chart(fig)    
        
        # Display the subtitle of the Candidate Affiliations
        st.subheader("Overview of French Legislative Candidate Affiliations")
        
        total_parties = new_filtered_department_df["Nuance"].nunique()
        st.metric("Total Number of Parties or Political Alliances", f"{total_parties}")
        
        st.markdown("---")  # Horizontal separator
        
        fig = px.histogram(new_filtered_department_df, 
                        x="Nuance", 
                        color="Tendency", 
                        color_discrete_map=palette_nuances,
                        title="Distribution of French Legislative Candidates by Party and Tendency",
                        category_orders={"Tendency": tendencies_plot_order})

        # Customize layout
        fig.update_layout(
            xaxis_title="Political parties",
            yaxis_title="Number of Candidates",
            showlegend=True,
            plot_bgcolor='white',
            legend_title_text='Tendencies'
        )

        # Add text annotations for counts
        fig.update_traces(texttemplate='%{y}', textposition='outside')

        # Display the chart using Streamlit
        st.plotly_chart(fig)
        
        # Create the semi-donut chart
        fig = px.pie(
            tendency_count, 
            values='count', 
            names=tendency_count.index,
            color=tendency_count.index,
            color_discrete_map=palette_nuances,  
            hole=0.5, 
            title='Distribution of Political Tendencies' ,
            category_orders={"Tendency": tendencies_plot_order},
            
        ) 
        
        fig.update_layout(
            showlegend=True,  # Display the legend
            legend_title_text='Tendencies'
        )
        fig.update_traces(textinfo='percent',
                        rotation=180,
                        )  

        
        # Display the chart using Streamlit
        st.plotly_chart(fig)
        
        st.markdown("---")  # Horizontal separator
        
    if analysis_type == "Result Analysis":
        
        df_region_elu = df_candidates[df_candidates['Elu'] == True]
        # Filter the DataFrame
        new_filtered_department_df = df_region_elu[df_region_elu["Département"] == selected_departement]
        new_filtered_department_df = new_filtered_department_df.drop_duplicates(subset='Nom_complet', keep="first")
        # Display the subtitle of the Result Analysis
        st.title(f"French Legislative Election: Departmental Result Analysis in {selected_departement}")

        tendencies_plot_order = ['Gauche-Radicale','Gauche', 'Centre', 'Centre-Droite', 'Droite', 'Extrême-Droite', 'Autres']
        total_mp = new_filtered_department_df['Nom_complet'].value_counts().sum()
        tendency_count = new_filtered_department_df["Tendency"].value_counts()
        sex_counts = new_filtered_department_df["Sexe"].value_counts()
        male_mp = sex_counts.get("MASCULIN", 0)
        female_mp = sex_counts.get("FEMININ", 0)
        #tendency_by_gender = df_region_elu.groupby('Sexe')['Nuance',].value_counts().unstack(fill_value=0)     
        
        st.subheader("Elected MP Gender Analysis")
        # --- Layout for Key Metrics ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Elected MP", f"{total_mp:,}")
        with col2:
            st.metric("Total Male Elected MP", f"{male_mp:,}")
        with col3:
            st.metric("Total Female Elected MP", f"{female_mp:,}")

        st.markdown("---")  # Horizontal separator
        
        # --- Layout for Charts ---
        col4, col5 = st.columns(2)

        # --- Barplot using Plotly Express ---
        with col4:
            fig = px.bar(
                x=['Male', 'Female'],
                y=[male_mp, female_mp],
                color=['Male', 'Female'],
                color_discrete_map={'Male': COLOR_PALETTE["Burgundy"], 'Female': COLOR_PALETTE["Cream"]},
                title="Distribution of Elected MP Gender"
            )
            fig.update_layout(
                xaxis_title="Gender of the Elected MP",
                yaxis_title="Number of Elected MP",
                yaxis_tickformat=",",
                plot_bgcolor='rgba(0,0,0,0)'  # Transparent background
            )
            st.plotly_chart(fig)

        # --- Pie Chart using Plotly Express ---
        with col5:
            fig = px.pie(
                values=[male_mp, female_mp],
                names=['Male', 'Female'],
                title="Proportion of Elected MP Genders",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Cream"]],
                hole=0.3
            )

            fig.update_traces(textinfo='percent+label',)
            st.plotly_chart(fig)
            
            # Display the subtitle of the Candidate Affiliations
        st.subheader("Overview of French Legislative Elected MP Affiliations")
        
        total_parties = new_filtered_department_df["Nuance"].nunique()
        st.metric("Total Number of Parties or Political Alliances", f"{total_parties}")
        
        st.markdown("---")  # Horizontal separator
        
        fig = px.histogram(new_filtered_department_df, 
                        x="Nuance", 
                        color="Tendency", 
                        color_discrete_map=palette_nuances,
                        title="Distribution of French Legislative Elected MP by Party and Tendency",
                        category_orders={"Tendency": tendencies_plot_order})

        # Customize layout
        fig.update_layout(
            xaxis_title="Political parties",
            yaxis_title="Number of Elected MP",
            showlegend=True,
            plot_bgcolor='white',
            legend_title_text='Tendencies'
        )

        # Add text annotations for counts
        fig.update_traces(texttemplate='%{y}', textposition='outside')

        # Display the chart using Streamlit
        st.plotly_chart(fig)
        
        # Create the semi-donut chart
        fig = px.pie(
            tendency_count, 
            values='count', 
            names=tendency_count.index,
            color=tendency_count.index,
            color_discrete_map=palette_nuances,  
            hole=0.5, 
            title='Distribution of Political Tendencies' ,
            category_orders={"Tendency": tendencies_plot_order},
            
        ) 
        
        fig.update_layout(
            showlegend=True,  # Display the legend
            legend_title_text='Tendencies'
        )
        fig.update_traces(textinfo='percent',
                        rotation=180,
                        )  

        
        # Display the chart using Streamlit
        st.plotly_chart(fig)
        
        st.markdown("---")  # Horizontal separator
    
    
def cityAnalysis():
    
    regions = df['Libellé_Région'].unique()
    selected_region = st.selectbox("Select Region", regions)
    
    filtered_region_df = df[df['Libellé_Région'] == selected_region]
    
    departements = filtered_region_df['Libellé_département'].unique()
    selected_departement = st.selectbox("Select Department", departements)
    
    filtered_department_df = df[df['Libellé_département'] == selected_departement]
    
    cities = filtered_department_df["Libellé_commune"].unique()
    selected_city = st.selectbox("Select City",cities)
    
    filtered_city_df = df[df['Libellé_commune'] == selected_city]
        
    st.title("Analysis of a specific city")
    
    # Button to select analysis type
    analysis_type = st.selectbox("Select Analysis Type:", ["Vote Analysis", "Candidate Analysis", "Result Analysis"])
    
    if analysis_type == "Vote Analysis":
        st.title(f"French Legislative Election: Communal Voter Turnout and Ballot Analysis in {selected_city}")

        total_registered = filtered_city_df["Registered"].sum()
        total_voters = filtered_city_df["Voters"].sum()
        total_abstentions = filtered_city_df["Abstentions"].sum()
        
        # Display the subtitle of the Voter Turnout
        st.subheader(f"Communal Voter Turnout Analysis in {selected_city}")

        # --- Layout for Key Metrics ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Registered Voters", f"{total_registered:,}")
        with col2:
            st.metric("Total Voters", f"{total_voters:,}")
        with col3:
            st.metric("Total Abstentions", f"{total_abstentions:,}")

        st.markdown("---")  # Horizontal separator

        # --- Layout for Charts ---
        col4, col5 = st.columns(2)

        # --- Barplot using Plotly Express ---
        with col4:
            fig = px.bar(
                x=['Voters', 'Abstentions'],
                y=[total_voters, total_abstentions],
                color=['Voters', 'Abstentions'],
                color_discrete_map={'Voters': COLOR_PALETTE["Burgundy"], 'Abstentions': COLOR_PALETTE["Cream"]},
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
                values=[total_voters, total_abstentions],
                names=['Voters', 'Abstentions'],
                title="Voter Turnout Proportion",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Cream"]],
                hole=0.3 
            )
            fig.update_traces(textinfo='percent+label',)
            st.plotly_chart(fig)
            
        total_cast = filtered_city_df["Cast"].sum()
        total_blank  = filtered_city_df["Blank"].sum()
        total_invalid  = filtered_city_df["Invalid"].sum()
        
        # Display the subtitle of the Ballot Analysis
        st.subheader(f"Depatmental Ballot Analysis in {selected_departement}")
            
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
                title="Distribution of Cast, Blank, and Invalid Votes"
            )
            fig.update_layout(
                xaxis_title="Vote Status",
                yaxis_title="Number of Votes",
                yaxis_tickformat=",",
                plot_bgcolor='rgba(0,0,0,0)'  # Transparent background
            )
            st.plotly_chart(fig)

        # --- Pie Chart using Plotly Express ---
        with col10:
            fig = px.pie(
                values=[total_cast, total_blank, total_invalid],
                names=['Cast', 'Blank', 'Invalid'],
                title="Proportion of Cast, Blank, and Invalid Votes",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Coffee"], COLOR_PALETTE["Cream"]],
                hole=0.3
            )
            fig.update_traces(textinfo='percent+label',)
            st.plotly_chart(fig)
            
    
    if analysis_type == "Candidate Analysis":
        st.title(f"French Legislative Election: Communal Candidate Turnout Analysis in {selected_city}")
        # Filter the DataFrame
        new_filtered_department_df = df_candidates[df_candidates['Département']==selected_departement]
        new_filtered_city_df = new_filtered_department_df[new_filtered_department_df['Commune'] == selected_city]
        new_filtered_city_df = new_filtered_city_df.drop_duplicates(subset='Nom_complet', keep="first")
        total_candidates = new_filtered_city_df["Nom_complet"].nunique()
        
        tendencies_plot_order = ['Gauche-Radicale','Gauche', 'Centre', 'Centre-Droite', 'Droite', 'Extrême-Droite', 'Autres']
        sex_counts = new_filtered_city_df["Sexe"].value_counts()
        male_candidates = sex_counts.get("MASCULIN", 0)
        female_candidates = sex_counts.get("FEMININ", 0)
        tendency_count = new_filtered_city_df["Tendency"].value_counts()
        # Display the subtitle of the Ballot Analysis
        st.subheader("Candidate Gender Analysis")
        
        # --- Layout for Key Metrics ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Candidates", f"{total_candidates:,}")
        with col2:
            st.metric("Total Male Candidates", f"{male_candidates:,}")
            pass
        with col3:
            st.metric("Total Female Candidates", f"{female_candidates:,}")
            pass
        st.markdown("---")  # Horizontal separator
        
        # --- Layout for Charts ---
        col4, col5 = st.columns(2)
        # --- Barplot using Plotly Express ---
        with col4:
            fig = px.bar(
                x=['Male', 'Female'],
                y=[male_candidates, female_candidates],
                color=['Male', 'Female'],
                color_discrete_map={'Male': COLOR_PALETTE["Burgundy"], 'Female': COLOR_PALETTE["Cream"]},
                title="Distribution of Candidates Gender"
            )
            fig.update_layout(
                xaxis_title="Gender of the Candidates",
                yaxis_title="Number of Candidates",
                yaxis_tickformat=",",
                plot_bgcolor='rgba(0,0,0,0)'  # Transparent background
            )
            st.plotly_chart(fig)

        # --- Pie Chart using Plotly Express ---
        with col5:
            fig = px.pie(
                values=[male_candidates, female_candidates],
                names=['Male', 'Female'],
                title="Proportion of Candidates Genders",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Cream"]],
                hole=0.3
            )

            fig.update_traces(textinfo='percent+label',)
            st.plotly_chart(fig)    
        
        # Display the subtitle of the Candidate Affiliations
        st.subheader("Overview of French Legislative Candidate Affiliations")
        
        total_parties = new_filtered_city_df["Nuance"].nunique()
        st.metric("Total Number of Parties or Political Alliances", f"{total_parties}")
        
        st.markdown("---")  # Horizontal separator
        
        fig = px.histogram(new_filtered_city_df, 
                        x="Nuance", 
                        color="Tendency", 
                        color_discrete_map=palette_nuances,
                        title="Distribution of French Legislative Candidates by Party and Tendency",
                        category_orders={"Tendency": tendencies_plot_order})

        # Customize layout
        fig.update_layout(
            xaxis_title="Political parties",
            yaxis_title="Number of Candidates",
            showlegend=True,
            plot_bgcolor='white',
            legend_title_text='Tendencies'
        )

        # Add text annotations for counts
        fig.update_traces(texttemplate='%{y}', textposition='outside')

        # Display the chart using Streamlit
        st.plotly_chart(fig)
        
        # Create the semi-donut chart
        fig = px.pie(
            tendency_count, 
            values='count', 
            names=tendency_count.index,
            color=tendency_count.index,
            color_discrete_map=palette_nuances,  
            hole=0.5, 
            title='Distribution of Political Tendencies' ,
            category_orders={"Tendency": tendencies_plot_order},
            
        ) 
        
        fig.update_layout(
            showlegend=True,  # Display the legend
            legend_title_text='Tendencies'
        )
        fig.update_traces(textinfo='percent',
                        rotation=180,
                        )  

        
        # Display the chart using Streamlit
        st.plotly_chart(fig)
        
        st.markdown("---")  # Horizontal separator
        
    if analysis_type == "Result Analysis":
        
        df_region_elu = df_candidates[df_candidates['Elu'] == True]
        # Filter the DataFrame
        new_filtered_department_df = df_region_elu[df_region_elu['Département']==selected_departement]
        new_filtered_department_df = new_filtered_department_df[new_filtered_department_df["Commune"] == selected_city]
        new_filtered_department_df = new_filtered_department_df.drop_duplicates(subset='Nom_complet', keep="first")
        # Display the subtitle of the Result Analysis
        st.title(f"French Legislative Election: Communal Result Analysis in {selected_city}")

        tendencies_plot_order = ['Gauche-Radicale','Gauche', 'Centre', 'Centre-Droite', 'Droite', 'Extrême-Droite', 'Autres']
        total_mp = new_filtered_department_df['Nom_complet'].value_counts().sum()
        tendency_count = new_filtered_department_df["Tendency"].value_counts()
        sex_counts = new_filtered_department_df["Sexe"].value_counts()
        male_mp = sex_counts.get("MASCULIN", 0)
        female_mp = sex_counts.get("FEMININ", 0)
        #tendency_by_gender = df_region_elu.groupby('Sexe')['Nuance',].value_counts().unstack(fill_value=0)     
        
        st.subheader("Elected MP Gender Analysis")
        # --- Layout for Key Metrics ---
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Elected MP", f"{total_mp:,}")
        with col2:
            st.metric("Total Male Elected MP", f"{male_mp:,}")
        with col3:
            st.metric("Total Female Elected MP", f"{female_mp:,}")

        st.markdown("---")  # Horizontal separator
        
        # --- Layout for Charts ---
        col4, col5 = st.columns(2)

        # --- Barplot using Plotly Express ---
        with col4:
            fig = px.bar(
                x=['Male', 'Female'],
                y=[male_mp, female_mp],
                color=['Male', 'Female'],
                color_discrete_map={'Male': COLOR_PALETTE["Burgundy"], 'Female': COLOR_PALETTE["Cream"]},
                title="Distribution of Elected MP Gender"
            )
            fig.update_layout(
                xaxis_title="Gender of the Elected MP",
                yaxis_title="Number of Elected MP",
                yaxis_tickformat=",",
                plot_bgcolor='rgba(0,0,0,0)'  # Transparent background
            )
            st.plotly_chart(fig)

        # --- Pie Chart using Plotly Express ---
        with col5:
            fig = px.pie(
                values=[male_mp, female_mp],
                names=['Male', 'Female'],
                title="Proportion of Elected MP Genders",
                color_discrete_sequence=[COLOR_PALETTE["Burgundy"], COLOR_PALETTE["Cream"]],
                hole=0.3
            )

            fig.update_traces(textinfo='percent+label',)
            st.plotly_chart(fig)
            
            # Display the subtitle of the Candidate Affiliations
        st.subheader("Overview of French Legislative Elected MP Affiliations")
        
        total_parties = new_filtered_department_df["Nuance"].nunique()
        st.metric("Total Number of Parties or Political Alliances", f"{total_parties}")
        
        st.markdown("---")  # Horizontal separator
        
        fig = px.histogram(new_filtered_department_df, 
                        x="Nuance", 
                        color="Tendency", 
                        color_discrete_map=palette_nuances,
                        title="Distribution of French Legislative Elected MP by Party and Tendency",
                        category_orders={"Tendency": tendencies_plot_order})

        # Customize layout
        fig.update_layout(
            xaxis_title="Political parties",
            yaxis_title="Number of Elected MP",
            showlegend=True,
            plot_bgcolor='white',
            legend_title_text='Tendencies'
        )

        # Add text annotations for counts
        fig.update_traces(texttemplate='%{y}', textposition='outside')

        # Display the chart using Streamlit
        st.plotly_chart(fig)
        
        # Create the semi-donut chart
        fig = px.pie(
            tendency_count, 
            values='count', 
            names=tendency_count.index,
            color=tendency_count.index,
            color_discrete_map=palette_nuances,  
            hole=0.5, 
            title='Distribution of Political Tendencies' ,
            category_orders={"Tendency": tendencies_plot_order},
            
        ) 
        
        fig.update_layout(
            showlegend=True,  # Display the legend
            legend_title_text='Tendencies'
        )
        fig.update_traces(textinfo='percent',
                        rotation=180,
                        )  

        
        # Display the chart using Streamlit
        st.plotly_chart(fig)
        
        st.markdown("---")  # Horizontal separator

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


