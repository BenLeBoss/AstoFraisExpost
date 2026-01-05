import pandas as pd
from app.routes.getter_setter_data.setter_data_from_xlsx.setter_Fournisseurs_data import setter_data_fournisseur_francevalley



def getter_data_fournisseur_FranceValley(Fournisseur_doc):
    

    print("Colonnes disponibles :", Fournisseur_doc.columns.tolist())

    for index, row in Fournisseur_doc.iterrows():

        #si la colonne 'NOM' est remplie
        if pd.notna(row["Nom"]):
            Num_ligne = index
            Nom = str(row["Nom"]).upper()
            if pd.notna(row["Prénom"]):
                Prenom = str(row["Prénom"]).lower().capitalize()
            else:
                Prenom = ''

            #NumCompte = str(row["Code Client"]).zfill(6)
            IntituleProduit = str(row["Produit"])

            TypeFrais1_percent = str((row["Frais de souscription (hors commission partenaire)"] * 100) / row["Montant total des encours"])
            TypeFrais1_euros = str(row["Frais de souscription (hors commission partenaire)"])
            TypeFrais2_percent = str((row["Frais courants"] * 100) / row["Montant total des encours"])
            TypeFrais2_euros = str(row["Frais courants"])
            TypeFrais3_percent = str((row["Frais de transactions"] * 100) / row["Montant total des encours"])
            TypeFrais3_euros = str(row["Frais de transactions"])

            MontantSouscritAnneeCourante = str(row["Montant souscrit au cours de l'exercice"])
            TauxFraisTransaction = str(float(row["Taux de frais transaction"])*100)
            TotalFraisTransactionAnneeCourante = str(row["Frais relatifs à la transaction (droits entrée + com. Partenaire)"])
            MontantTotalSouscrit = row["Montant total des encours"]

            print(f"Ligne {Num_ligne+2} =  Client nom : '{Nom}', Prénom : '{Prenom}', Produit : '{IntituleProduit}'")
            print(f"            Frais 1 (%, euros) : '{TypeFrais1_percent}, {TypeFrais1_euros}' // Frais 2 (%, euros) : '{TypeFrais2_percent}, {TypeFrais2_euros}' // Frais 3 (%, euros) : '{TypeFrais3_percent}, {TypeFrais3_euros}' // Frais souscription + transaction (%, euros) : ' {TauxFraisTransaction}, {TotalFraisTransactionAnneeCourante}, // Montant souscrit : {MontantSouscritAnneeCourante}")
            setter_data_fournisseur_francevalley(Nom, Prenom, IntituleProduit, TypeFrais1_percent, TypeFrais1_euros, TypeFrais2_percent, TypeFrais2_euros, 
                                                 TypeFrais3_percent, TypeFrais3_euros, TauxFraisTransaction, TotalFraisTransactionAnneeCourante, MontantSouscritAnneeCourante, MontantTotalSouscrit, "M5")








