import pandas as pd

df = pd.read_csv("dataset/donnees_ventes_etudiants.csv")

print("Nombre de lignes et colonnes :", df.shape)
print("\nNoms des colonnes :")
print(df.columns.tolist())
print("\nAperçu des données :")
print(df.head())
print("\nTypes de données :")
print(df.dtypes)

print("\nValeurs uniques - status :")
print(df['status'].unique())

print("\nValeurs uniques - Region :")
print(df['Region'].unique())

print("\nNombre de State uniques :")
print(df['State'].nunique())
print(df['State'].unique())

print("\nValeurs manquantes par colonne clé :")
print(df[['order_date','status','cust_id','total','category','Region','State','City','Gender','age','full_name']].isnull().sum())

print("\nNombre de order_id uniques vs nombre de lignes :")
print("order_id uniques:", df['order_id'].nunique(), "/ lignes:", len(df))


""" 
 Filtres (calendrier, Région/State/Country/City, statut)
 KPI
 Graphique ligne 1 (Catégorie + Région)
 Ligne 2 : Top 10 meilleurs clients (barre horizontale)
 Ligne 3 : Histogramme âge + diagramme Hommes/Femmes
 Ligne 4 : Courbe du nombre de ventes par mois
 Bonus : Carte des ventes par State (avec latitude/longitude)
"""