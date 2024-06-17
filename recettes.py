import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# Chargement des données
chemin = Path(__file__).parent
fichier_data = chemin / "Recettes.csv"
fichier_plats = chemin / "Plats.csv"

df = pd.read_csv(fichier_data, sep=";")
df_plats = pd.read_csv(fichier_plats, sep=";")

# Calcul le cout de chaque ingrédient en multipliant "Qté Base Initiale"par "Cout Unitaire Ingrédient"
df["Cout Ingrédient"] = df["Qté Base Initiale"] * df["Cout Unitaire Ingrédient"]

def show():
    st.title("Analyse des recettes")

    # Créez un selectbox pour choisir une recette, avec une clé unique
    with st.sidebar:
        recette_selectionnee = st.selectbox("recette", df["Recette"].unique(), key="recette_select")
        st.title("DONNEES RECETTES")
        st.subheader("QUANTITES")

        unites_produites = df[df["Recette"] == recette_selectionnee].iloc[0]["Unités Produites"]
        st.write("Unités Produites :", f"{unites_produites:.0f}")

        # afficher le nombre par portions 
        nb_par_portions = df_plats[df_plats["Plats"] == recette_selectionnee]["Pieces"].iloc[0]
        st.write("Nombre / portions :", f"{nb_par_portions:.0f}")

        #Afficher le nombre de portions
        nb_portions = round(unites_produites/nb_par_portions, 2)
        st.write("Nombre de portions :", f"{nb_portions:.0f}") 

        st.subheader("COUTS, MARGE, COEFFICIENT")

        # Affichez le cout total de la recette
        cout_total = df[df["Recette"] == recette_selectionnee]["Cout Ingrédient"].sum()
        st.write("Cout Total de la recette :", f"{cout_total:.2f} €")

        # Affichez le cout par portion
        cout_portion = round(cout_total/nb_portions, 2)
        st.write("Cout par portion :", f"{cout_portion:.2f} €")

        # Affichez le prix de vente cible d'une portion
        Prix_cible = df_plats[df_plats["Plats"] == recette_selectionnee]["Prix_cible"].iloc[0]
        st.write("Prix cible :", f"{Prix_cible:.2f} €")

        Coefficent = Prix_cible/cout_portion
        st.write("Coefficent :", f"{Coefficent:.1f}")

        Marge = Prix_cible - cout_portion
        st.write("Marge / Portion de "f"{nb_par_portions}"," unit. :", f"{Marge:.2f} €")

        Marge_totale = Marge*nb_portions
        st.write("Marge Totale pour "f"{nb_portions:.0f}"," unit. :", f"{Marge_totale:.2f} €")

        Taux_marge = (Marge/Prix_cible)*100
        st.write("Taux de marge :", f"{Taux_marge:.2f} %")

    col_pie = st.columns([0.5,0.5])
    with col_pie[0]:
    # Ajout d'un camembert des coûts des ingrédients
        fig = px.pie(df[df["Recette"] == recette_selectionnee], values='Cout Ingrédient', names='Ingrédient', title='Répartition des coûts des ingrédients')
        fig.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                plot_bgcolor="rgba(0, 0, 0, 0)",
                paper_bgcolor="rgba(0, 0, 0, 0)",
                height=400, width=700
            ) 
        st.plotly_chart(fig)

    # On filtre le dataframe pour avoir les données de la recette sélectionnée
    df_temp = df[df["Recette"] == recette_selectionnee] 
    
    #df_temp = df[df["Recette"] == recette_selectionnee]
    col1, col2 = st.columns([.8,.2]) # Créez deux colonnes pour afficher les données et le cout total
    with col1:
        df_temp["Cout Ingrédient"] = df_temp["Cout Unitaire Ingrédient"]*df_temp["Qté Base Initiale"].round(2)
        edited_df = st.data_editor(df_temp[["Etape", "Ingrédient", "Unité de l'ingrédient", "Qté Base Initiale", "Cout Unitaire Ingrédient","Cout Ingrédient"]])
    with col2:
        total = edited_df["Cout Unitaire Ingrédient"]*edited_df["Qté Base Initiale"].round(2) # Calcul du cout 
        st.dataframe(total)

    with st.sidebar :
        st.subheader("NX COUTS, MARGE, COEFFICIENT")
    # Affichez le cout total de la recette edited_df de la recette_selectionnee
        Nx_cout_total = total.sum().round(2)
        st.write("Nouveau cout Total : ", f"{Nx_cout_total:.2f} €")
    # Affichez le cout par portion
        Nx_cout_portion = round(Nx_cout_total/nb_portions, 2)
        st.write("Nouveau cout par portion :", f"{Nx_cout_portion:.2f} €")

        Nouvelle_Marge = Prix_cible - Nx_cout_portion
        st.write("Nouvelle marge/ Portion de "f"{nb_par_portions}"," unit. :", f"{Nouvelle_Marge:.2f} €")

        Nouvelle_Marge_totale = Nouvelle_Marge*nb_portions
        st.write("Nouvelle Marge Totale pour "f"{nb_portions:.0f}"," unit. :", f"{Nouvelle_Marge_totale:.2f} €")

        Nouveau_Taux_marge = (Nouvelle_Marge/Prix_cible)*100
        st.write("Nouveau Taux de marge :", f"{Nouveau_Taux_marge:.2f} %")
        
        st.subheader("COMPARAISON")

        # Comparaison des coûts
        diff_cout = Nx_cout_total - cout_total
        st.write("Différence de coût :", f"{diff_cout:.2f} €")

        # Comparaison des marges
        diff_marge = Nouvelle_Marge - Marge
        st.write("Différence de marge :", f"{diff_marge:.2f} €")

        # Comparaison des coefficients
        diff_coeff = (Prix_cible/Nx_cout_portion) - Coefficent
        st.write("Différence de coefficient :", f"{diff_coeff:.2f}")



    with col_pie[1]:
    # Ajout d'un camembert des coûts des ingrédients
        fig = px.pie(edited_df, values=edited_df["Cout Unitaire Ingrédient"]*edited_df["Qté Base Initiale"].round(2), names='Ingrédient', title='Répartition des coûts des ingrédients')
        fig.update_layout(
                margin={"r": 0, "t": 0, "l": 0, "b": 0},
                plot_bgcolor="rgba(0, 0, 0, 0)",
                paper_bgcolor="rgba(0, 0, 0, 0)",
                height=400, width=700
            ) 
        st.plotly_chart(fig)

