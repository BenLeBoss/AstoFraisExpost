import pandas as pd
from app.routes.getter_setter_data.setter_data_from_xlsx.setter_Fournisseurs_data import setter_data_fournisseur_smaltcapital



def getter_data_fournisseur_SmaltCapital(Fournisseur_doc):
    

    print("Colonnes disponibles :", Fournisseur_doc.columns.tolist())

    for index, row in Fournisseur_doc.iterrows():

        #si la colonne du nom de produit est remplie
        if '00030_Financial_Instrument_Name' in Fournisseur_doc.columns and pd.notna(row["00030_Financial_Instrument_Name"]):
            Num_ligne = index

            IntituleProduit = str(row["00030_Financial_Instrument_Name"])

            t8030_Financial = 0.0
            t8050_Financial = 0.0
            t8080_Financial = 0.0
            t8070_Financial = 0.0

            if pd.notna(row["08030_Financial_Instrument_Ongoing_Costs_Ex_Post"]):
                t8030_Financial = float(nettoyer_float(row["08030_Financial_Instrument_Ongoing_Costs_Ex_Post"]))
            if pd.notna(row["08050_Financial_Instrument_Management_Fee_Ex_Post"]):
                t8050_Financial = float(nettoyer_float(row["08050_Financial_Instrument_Management_Fee_Ex_Post"]))
            if pd.notna(row["08080_Financial_Instrument_Incidental_Costs_Ex_Post"]):    
                t8080_Financial = float(nettoyer_float(row["08080_Financial_Instrument_Incidental_Costs_Ex_Post"]))
            if pd.notna(row["08070_Financial_Instrument_Transaction_Costs_Ex_Post"]):
                t8070_Financial = float(nettoyer_float(row["08070_Financial_Instrument_Transaction_Costs_Ex_Post"]))

            TypeFrais1_percent = t8030_Financial + t8050_Financial + t8080_Financial
            TypeFrais2_percent = 0.0
            TypeFrais3_percent = t8070_Financial


            # Les taux Smalt Capital sont donnés sous forme décimal, il faut les multiplier par 100 pour les obtenir sous forme de pourcentage
            TypeFrais1_percent = TypeFrais1_percent * 100
            TypeFrais3_percent = TypeFrais3_percent * 100


            if row["08030_Financial_Instrument_Ongoing_Costs_Ex_Post"]  != 'Funds':

                print(f"Ligne {Num_ligne+2} =  Nom Produit : '{IntituleProduit}'")
                print(f"            Frais 1 (%) : '{TypeFrais1_percent}' // Frais 2 (%) : '{TypeFrais2_percent}' // Frais 3 (%) : '{TypeFrais3_percent}'")
                setter_data_fournisseur_smaltcapital(IntituleProduit, TypeFrais1_percent, TypeFrais2_percent, TypeFrais3_percent, "M1")









def nettoyer_float(valeur):
    if pd.isna(valeur):
        return 0.0
    return str(valeur).replace(",",".").replace("\n", "").strip()


