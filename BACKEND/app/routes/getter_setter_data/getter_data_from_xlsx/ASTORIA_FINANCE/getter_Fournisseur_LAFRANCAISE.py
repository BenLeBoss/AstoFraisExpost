import pandas as pd
from app.routes.getter_setter_data.setter_data_from_xlsx.setter_Fournisseurs_data import setter_data_fournisseur_lafrancaise



def getter_data_fournisseur_LaFrancaise(Fournisseur_doc):
    

    print("Colonnes disponibles :", Fournisseur_doc.columns.tolist())

    for index, row in Fournisseur_doc.iterrows():

        #si la colonne du nom de produit est remplie
        if pd.notna(row["00030_financial_instrument_name"]):
            Num_ligne = index

            IntituleProduit = str(row["00030_financial_instrument_name"])


            t8030_Financial = 0.0
            t8050_Financial = 0.0
            t8080_Financial = 0.0
            t8070_Financial = 0.0

            if pd.notna(row["08030_financial_instrument_ongoing_costs_ex_post"]):
                t8030_Financial = float(nettoyer_float(row["08030_financial_instrument_ongoing_costs_ex_post"]))
            if pd.notna(row["08050_financial_instrument_management_fee_ex_post"]):
                t8050_Financial = float(nettoyer_float(row["08050_financial_instrument_management_fee_ex_post"]))
            if pd.notna(row["08080_financial_instrument_incidental_costs_ex_post"]):    
                t8080_Financial = float(nettoyer_float(row["08080_financial_instrument_incidental_costs_ex_post"]))
            if pd.notna(row["08070_financial_instrument_transaction_costs_ex_post"]):
                t8070_Financial = float(nettoyer_float(row["08070_financial_instrument_transaction_costs_ex_post"]))


            TypeFrais1_percent = t8030_Financial + t8050_Financial + t8080_Financial
            TypeFrais2_percent = 0.0
            TypeFrais3_percent = t8070_Financial

            if t8030_Financial:

                print(f"Ligne {Num_ligne+2} =  Nom Produit : '{IntituleProduit}'")
                print(f"            Frais 1 (%) : '{TypeFrais1_percent}' // Frais 2 (%) : '{TypeFrais2_percent}' // Frais 3 (%) : '{TypeFrais3_percent}'\n")
                #setter_data_fournisseur_lafrancaise(IntituleProduit, TypeFrais1_percent, TypeFrais2_percent, TypeFrais3_percent, "M1")



def nettoyer_float(valeur):
    if pd.isna(valeur):
        return 0.0
    return str(valeur).replace(",",".").replace("\n", "").strip()





