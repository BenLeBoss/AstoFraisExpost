import pandas as pd
from app.routes.getter_setter_data.setter_data_from_xlsx.setter_Fournisseurs_data import setter_data_fournisseur_theoreim



def getter_data_fournisseur_Theoreim(Fournisseur_doc):
    

    print("Colonnes disponibles :", Fournisseur_doc.columns.tolist())

    for index, row in Fournisseur_doc.iterrows():

        #si la colonne 'NOM' est remplie
        if pd.notna(row["Nom du client"]):
            Num_ligne = index
            Nom = str(row["Nom du client"]).upper().strip()
            if pd.notna(row["Prénom du client"]):
                Prenom = str(row["Prénom du client"]).lower().capitalize().strip()
            else:
                Prenom = ''

            Civilite = row["Civilité du client"].strip()

            # spécificité du fichier EMT Theoreim : met SC et empeche les match avec le fichier client où les éléments sont renseignés avec 'SCI'
            if Civilite == 'SC':
                Civilite = 'SCI'
                
            NumCompte = str(row["Code Client"]).zfill(6)
            IntituleProduit = str(row["Nom du produit"]).strip()

            TypeFrais1_percent = row["% Type de frais n°1"]
            TypeFrais1_euros = row["Type de frais n°1"]
            TypeFrais2_percent = row["% Type de frais n°3"]
            TypeFrais2_euros = row["Type de frais n°3"]
            TypeFrais3_percent = row["% Type de frais n°4"]
            TypeFrais3_euros = row["Type de frais n°4"]

            TauxCommission = 5.5    # 5.5%
            TVA = 20    # 20%
            TauxPaiementTiers = ((TauxCommission * TVA) / 100)

            

            print(f"Ligne {Num_ligne+2} =  Client : '{Civilite} {Nom} {Prenom}', Produit : '{IntituleProduit}' sous le code client {NumCompte}")
            print(f"            Frais 1 (%, euros) : '{str(TypeFrais1_percent)}, {str(TypeFrais1_euros)}' // Frais 2 (%, euros) : '{str(TypeFrais2_percent)}, {str(TypeFrais2_euros)}' // Frais 3 (%, euros) : '{str(TypeFrais3_percent)}, {str(TypeFrais3_euros)}' \n")
            #setter_data_fournisseur_theoreim(Civilite, Nom, Prenom, NumCompte, IntituleProduit, TypeFrais1_percent, TypeFrais1_euros, TypeFrais2_percent, TypeFrais2_euros,
            #                                 TypeFrais3_percent, TypeFrais3_euros, "M4")

