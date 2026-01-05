import pandas as pd
from app.routes.getter_setter_data.setter_data_from_xlsx.setter_Fournisseurs_data import setter_data_fournisseur_urbanpremium



def getter_data_fournisseur_UrbanPremium(Fournisseur_doc):
    

    print("Colonnes disponibles :", Fournisseur_doc.columns.tolist())

    for index, row in Fournisseur_doc.iterrows():

        #si la colonne 'NOM' est remplie
        if pd.notna(row["Nom client"]):
            Num_ligne = index
            Nom = str(row["Nom client"]).upper().strip()
            if pd.notna(row["Prénom"]):
                Prenom = str(row["Prénom"]).lower().capitalize().strip()
            else:
                Prenom = ''

            Civilite = row["Titre"].strip()
            NumCompte = str(row["Code client"]).zfill(6)
            IntituleProduit = str(row["Libellé"]).strip()
            DateSouscription = row["Date de souscription"]

            TypeFrais1_percent = row["FRAIS IMMOBILIERS 2 en %               PFIM %"]
            TypeFrais1_euros = row["FRAIS IMMOBILIERS 2                    FIM €"]
            TypeFrais2_percent = row["FRAIS RECURRENTS 2 en %                FR %"]
            TypeFrais2_euros = row["FRAIS RECURRENTS 2                    FR €"]
            TypeFrais3_percent = row["FRAIS LIES AUX TRANSAC           PFIT %"]
            TypeFrais3_euros = row["FRAIS LIES AUX TRANSACTIONS 2          FIT €"]

            TauxCommission = 5.5    # 5.5%
            TVA = 20    # 20%
            TauxPaiementTiers = ((TauxCommission * TVA) / 100)

            print(f"Ligne {Num_ligne+2} =  Client : '{Civilite} {Nom} {Prenom}', Produit : '{IntituleProduit}' souscrit le {DateSouscription} sous le code client {NumCompte}")
            print(f"            Frais 1 (%, euros) : '{str(TypeFrais1_percent)}, {str(TypeFrais1_euros)}' // Frais 2 (%, euros) : '{str(TypeFrais2_percent)}, {str(TypeFrais2_euros)}' // Frais 3 (%, euros) : '{str(TypeFrais3_percent)}, {str(TypeFrais3_euros)}' \n")
            setter_data_fournisseur_urbanpremium(Civilite, Nom, Prenom, NumCompte, IntituleProduit, DateSouscription, TypeFrais1_percent, TypeFrais1_euros, 
                                                 TypeFrais2_percent, TypeFrais2_euros, TypeFrais3_percent, TypeFrais3_euros, "M3")

