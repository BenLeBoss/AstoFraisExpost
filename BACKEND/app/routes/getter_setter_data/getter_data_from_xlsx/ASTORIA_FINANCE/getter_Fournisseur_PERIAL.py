import pandas as pd
from app.routes.getter_setter_data.setter_data_from_xlsx.setter_Fournisseurs_data import setter_data_fournisseur_perial



def getter_data_fournisseur_Perial(Fournisseur_doc):
    
    for index, row in Fournisseur_doc.iterrows():

        #si la colonne 'NOM' est remplie
        if pd.notna(row["Nom du client"]):
            Num_ligne = index
            Nom = str(row["Nom du client"]).upper()
            if pd.notna(row["Prénom du client"]):
                Prenom = str(row["Prénom du client"]).lower().capitalize()
            else:
                Prenom = ''

            NumCompte = str(row["Code Client"]).zfill(6)
            IntituleProduit = str(row["Nom du produit"])

            TypeFrais1_percent = str(row["% Type de frais n°1"])
            TypeFrais1_euros = str(row["Type de frais n°1"])
            TypeFrais2_percent = str(row["% Type de frais n°2"])
            TypeFrais2_euros = str(row["Type de frais n°2"])
            TypeFrais3_percent = str(row["% Type de frais n°3"])
            TypeFrais3_euros = str(row["Type de frais n°3"])

            print(f"Ligne {Num_ligne+2} =  Client nom : '{Nom}', Prénom : '{Prenom}', NumCompte : '{NumCompte}', Produit : '{IntituleProduit}'")
            print(f"            Frais 1 (%, euros) : '{TypeFrais1_percent}, {TypeFrais1_euros}' // Frais 2 (%, euros) : '{TypeFrais2_percent}, {TypeFrais2_euros}' // Frais 3 (%, euros) : '{TypeFrais3_percent}, {TypeFrais3_euros}'")
            #setter_data_fournisseur_perial(Nom, Prenom, NumCompte, IntituleProduit, TypeFrais1_percent, TypeFrais1_euros, TypeFrais2_percent, TypeFrais2_euros, 
            #   TypeFrais3_percent, TypeFrais3_euros, "M4")








