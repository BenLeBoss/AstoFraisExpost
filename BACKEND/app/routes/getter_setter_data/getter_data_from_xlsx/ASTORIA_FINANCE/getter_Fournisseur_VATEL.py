import pandas as pd
import unicodedata
import re
from app.routes.getter_setter_data.setter_data_from_xlsx.setter_Fournisseurs_data import setter_data_fournisseur_vatel


# Récupère tous les clients d'une entité
def getter_data_fournisseur_Vatel(Client_doc):
    
    NumClient = 2
    for index, row in Client_doc.iterrows():

        #si la colonne 'NOM' est remplie
        if 'NOM SOUSCRIPTEUR' in Client_doc.columns and pd.notna(row["PRENOM SOUSCRIPTEUR"]):

            Nom = str(row["NOM SOUSCRIPTEUR"]).upper()

            Prenom = ''
            if 'PRENOM SOUSCRIPTEUR' in Client_doc.columns and pd.notna(row["PRENOM SOUSCRIPTEUR"]):
                Prenom = str(row["PRENOM SOUSCRIPTEUR"]).lower().capitalize()

            Civilite = ''
            if 'CIVILITÉ' in Client_doc.columns and pd.notna(row["CIVILITÉ"]):
                Civilite = str(row["CIVILITÉ"]).upper()

            IntituleProduit = ''
            if 'NOM DU FONDS' in Client_doc.columns and pd.notna(row["NOM DU FONDS"]):
                IntituleProduit = str(row["NOM DU FONDS"])

            DateSouscription = ''
            if 'DATE' in Client_doc.columns and pd.notna(row["DATE"]):
                DateSouscription = str(row["DATE"])

            MontantTotalSouscritAnneeCourante = 0.00
            if 'Total des frais ex-post 2024 (en €)' in Client_doc.columns and pd.notna(row["Total des frais ex-post 2024 (en €)"]):
                MontantTotalSouscritAnneeCourante = float(row["Total des frais ex-post 2024 (en €)"])

            TypeFrais2_eu = 0.00
            if 'Frais récurrents S1 2024' in Client_doc.columns and pd.notna(row["Frais récurrents S1 2024"]):
                TypeFrais2_eu += float(row["Frais récurrents S1 2024"])
            if 'Frais récurrents S2 2024' in Client_doc.columns and pd.notna(row["Frais récurrents S2 2024"]):
                TypeFrais2_eu += float(row["Frais récurrents S2 2024"])


            print(f"Ligne {NumClient} =  Client : '{Civilite} {Nom} {Prenom}', Produit : '{IntituleProduit}' souscrit le {DateSouscription}")
            print(f"            Frais 2 (euros) : {row["Frais récurrents S1 2024"]} + {row["Frais récurrents S2 2024"]} = {str(TypeFrais2_eu)}, Montant total 2024 : {MontantTotalSouscritAnneeCourante} \n")
            
            NumClient += 1
            setter_data_fournisseur_vatel(Civilite=Civilite, Nom=Nom, Prenom=Prenom, DateOuverture=DateSouscription, IntituleProduit=IntituleProduit,
                                          TypeFrais2_eu=TypeFrais2_eu, MontantTotalSouscritAnneeCourante=MontantTotalSouscritAnneeCourante, ModeleUtilise="M6")


