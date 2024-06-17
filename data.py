import streamlit as st
import plotly.express as px
from pathlib import Path
import pandas as pd

chemin = Path(__file__).parent
fichier_data = chemin / 'data.csv'
data = pd.read_csv(fichier_data,sep=',')

fichier_data = chemin /'combined_df.csv'
combined_df = pd.read_csv(fichier_data,sep=',')

combined_df = combined_df.reset_index()
combined_df = combined_df.sort_values('Count')


# avoir uniquement la liste
data = data[data['Cuisine'].str.contains('|'.join(['asian','chinese','cambodian','korean','japanese','thai','vietnamese']))].reset_index(drop=True)
# création d'une liste des départemants unique
city_names = data['Commune'].unique().tolist()
# création d'une option qui permet de tout selectionnés
city_names.insert(0, "FRANCE")
def show():
    # col_intro = st.columns([0.90,0.10])
    # with col_intro[0]:
    col_header = st.columns([0.90,0.10])
    with col_header[0]:
        st.header("Food Services Details")
    # convertion 'Latitude' and 'Longitude'en numériquedata['Latitude'] = pd.to_numeric(data['Latitude'], errors='coerce')
    data['Longitude'] = pd.to_numeric(data['Longitude'], errors='coerce')
    #drop les valeurs manquantes latitude or longitude
    data.dropna(subset=['Latitude', 'Longitude'], inplace=True)
    data['size'] = 2
    # Créer des liens cliquables pour les sites web
    data['URL'] = data['Site Web'].apply(lambda x: f'<a href="{x}" target="_blank">{x}</a>')
    with st.sidebar:
    # création d'une selected box
        selected_city = st.selectbox("Sélectionne un departement", city_names)
        st.title("ANALYSE")
        st.subheader("HAUSSE DES COÛTS DES MATIÈRES PREMIÈRES ET DE L’ÉNERGIE :")
        
        multi = """
        <p style="font-size: 18px; color: #5f5f5f;">
        Source(extensia.fr)<br>
        </p>
        """
        st.markdown(multi, unsafe_allow_html=True)

        multi = """
        <p style="font-size: 18px; color: #5f5f5f;">
        Exp. : Huile de friture =  400 % <br>
        Matières premières environ 11,1 %
        <br>
        </p>
        """
        st.markdown(multi, unsafe_allow_html=True)
        st.subheader("REACTIVITE :")
        multi = """
        <p style="font-size: 18px; color: #5f5f5f;">
        Plus d’un restaurateur sur deux a décidé de revoir sa stratégie d’achat comme une priorité. Face à l’augmentation de <br>
        11,1 % du coût des matières premières,<br>
        les restaurateurs ont dû ajuster légèrement leurs prix <br>
        Matières premières environ 11,1 % <br>
        <br>
        66% ont fait le choix de proposer d’avantage de produits locaux<br>
        options végétariennes pour 32 % d’entre eux<br>
        </p>
        """
        st.markdown(multi, unsafe_allow_html=True)

    if selected_city =='FRANCE':

        fig = px.scatter_mapbox(data, lat="Latitude", lon="Longitude",
                        hover_name="Nom",  # Utiliser 'hover_name' pour afficher les noms lors du survol
                        hover_data={"size":False,"Latitude":False,"Longitude":False,"URL":True,"Type": True, "Cuisine": True,"À emporter":True,"Livraison":True,"Végétarien":True,"Ouverture Dimanche":True},  # Ajouter des colonnes spécifiques aux données de survol
                        color="Type", size='size',
                        size_max=15,
                        zoom=5, height=700, width=1200)

# Définir le style de la carte
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                plot_bgcolor="rgba(0, 0, 0, 0)",
                paper_bgcolor="rgba(0, 0, 0, 0)",
            )               
        # Afficher la figure
        st.plotly_chart(fig)
    else:
        data_city = data[data['Commune'] == selected_city]

        fig = px.scatter_mapbox(data_city, lat="Latitude", lon="Longitude",
                        hover_name="Nom",  # Utiliser 'hover_name' pour afficher les noms lors du survol
                        hover_data={"size":False,"Latitude":False,"Longitude":False,"URL":True,"Type": True, "Cuisine": True,"À emporter":True,"Livraison":True,"Végétarien":True,"Ouverture Dimanche":True},  # Ajouter des colonnes spécifiques aux données de survol
                        color="Type", size='size',
                        size_max=15,
                        zoom=11, height=700, width=1200)

# Définir le style de la carte
        fig.update_layout(mapbox_style="open-street-map")
        fig.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                plot_bgcolor="rgba(0, 0, 0, 0)",
                paper_bgcolor="rgba(0, 0, 0, 0)",
            )               
        # Afficher la figure
        st.plotly_chart(fig)
    col_histogram =st.columns([0.80,0.20])
    with col_histogram[0]:
        st.header("Food Service Repartition")
        fig=px.histogram(combined_df, 
                         x =["À emporter", "Livraison", "Végétarien", "Fermer Dimanche"],
                         y="Type",
                         hover_data="Count")
        fig.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                plot_bgcolor="rgba(0, 0, 0, 0)",
                paper_bgcolor="rgba(0, 0, 0, 0)",
            xaxis=dict(  # x-axis settings
                title=dict(
                    font=dict(size=20, color="#5f5f5f")
                ),  # x-axis title color
                tickfont=dict(color="#5f5f5f"),  # x-axis tick color
            ),
            yaxis=dict(  # y-axis settings
                title=dict(
                    font=dict(color="#5f5f5f")
                ),  # y-axis title color
                tickfont=dict(color="#5f5f5f"),  # y-axis tick color
            ),
        )
        st.plotly_chart(fig)
    with col_histogram[1]:
        st.write(combined_df[["Type","Count"]])
