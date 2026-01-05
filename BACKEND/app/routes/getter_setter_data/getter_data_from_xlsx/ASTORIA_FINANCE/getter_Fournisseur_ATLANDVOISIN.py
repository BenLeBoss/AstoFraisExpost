import pandas as pd
from app.routes.getter_setter_data.setter_data_from_xlsx.setter_Fournisseurs_data import setter_data_fournisseur_atlandvoisin



def getter_data_fournisseur_AtlandVoisin(Fournisseur_doc):
    

    print("Colonnes disponibles :", Fournisseur_doc.columns.tolist())

    for index, row in Fournisseur_doc.iterrows():

        #si la colonne 'NOM' est remplie
        if pd.notna(row["Nom du client"]):
            Num_ligne = index
            Nom = str(row["Nom du client"]).upper()
            if pd.notna(row["Prénom du client"]):
                Prenom = str(row["Prénom du client"]).lower().capitalize()
            else:
                Prenom = ''

            Civilite = row["Civilité du client"]
            #NumCompte = str(row["Code Client"]).zfill(6)
            IntituleProduit = str(row["Nom du produit"])

            TypeFrais1_percent = row["% FRAIS IMMO"]
            TypeFrais1_euros = row["FRAIS IMMO"]
            TypeFrais2_percent = row["% FRAIS RECURRENTS"]
            TypeFrais2_euros = row["FRAIS RECURRENTS"]
            TypeFrais3_percent = row["% COUTS DE TRANSACTION"]
            TypeFrais3_euros = row["COUTS DE TRANSACTIONS"]

            TauxCommission = 5.5    # 5.5%
            TVA = 20    # 20%
            TauxPaiementTiers = ((TauxCommission * TVA) / 100)

            print(f"Ligne {Num_ligne+2} =  Client nom : '{Nom}', Prénom : '{Prenom}', Produit : '{IntituleProduit}'")
            print(f"            Frais 1 (%, euros) : '{str(TypeFrais1_percent)}, {str(TypeFrais1_euros)}' // Frais 2 (%, euros) : '{str(TypeFrais2_percent)}, {str(TypeFrais2_euros)}' // Frais 3 (%, euros) : '{str(TypeFrais3_percent)}, {str(TypeFrais3_euros)}' ")
            #setter_data_fournisseur_atlandvoisin(Civilite, Nom, Prenom, IntituleProduit, TypeFrais1_percent, TypeFrais1_euros, TypeFrais2_percent, TypeFrais2_euros, 
            #                                        TypeFrais3_percent, TypeFrais3_euros, "M4")








