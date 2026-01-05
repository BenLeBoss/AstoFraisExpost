import pandas as pd
from pathlib import Path
from app.routes.getter_setter_data.setter_data_from_xlsx.setter_Fournisseurs_data import setter_data_fournisseur_keys


def getter_data_fournisseur_Keys(Fournisseur_doc, colonne_valeur):
    print("Colonnes disponibles :", Fournisseur_doc.columns.tolist())


    start_col = colonne_excel_vers_index(colonne_valeur)-1
    lignes_cibles = [
        "00030_Financial_Instrument_Name",
        "08030_Financial_Instrument_Ongoing_Costs_Ex_Post",
        "08050_Financial_Instrument_Management_Fee_Ex_Post",
        "08080_Financial_Instrument_Incidental_Costs_Ex_Post",
        "08070_Financial_Instrument_Transaction_Costs_Ex_Post"
    ]

    nb_colonnes = Fournisseur_doc.shape[1]
    index_lignes = Fournisseur_doc.iloc[:, 0] 

    """
    print("\n--- Valeurs extraites ---")
    for ligne in lignes_cibles:
        valeur = colonne_choisie.get(ligne, None)
        print(f"{ligne} → {valeur}")
        setter_data_fournisseur_keys(IntituleProduit, TypeFrais1_percent, TypeFrais2_percent,TypeFrais3_percent, ModeleUtilise)
    """

    for col_index in range(start_col, nb_colonnes):
        colonne_choisie = Fournisseur_doc.iloc[:, col_index]
        colonne_choisie.index = index_lignes

        IntituleProduit = colonne_choisie.get("00030_Financial_Instrument_Name")
        
        t8030_Financial = 0.0
        t8050_Financial = 0.0
        t8080_Financial = 0.0
        t8070_Financial = 0.0

        if pd.notna(colonne_choisie.get("08030_Financial_Instrument_Ongoing_Costs_Ex_Post")):
            t8030_Financial = float(nettoyer_float(colonne_choisie.get("08030_Financial_Instrument_Ongoing_Costs_Ex_Post")))
        if pd.notna(colonne_choisie.get("08050_Financial_Instrument_Management_Fee_Ex_Post")):
            t8050_Financial = float(nettoyer_float(colonne_choisie.get("08050_Financial_Instrument_Management_Fee_Ex_Post")))
        if pd.notna(colonne_choisie.get("08080_Financial_Instrument_Incidental_Costs_Ex_Post")):    
            t8080_Financial = float(nettoyer_float(colonne_choisie.get("08080_Financial_Instrument_Incidental_Costs_Ex_Post")))
        if pd.notna(colonne_choisie.get("08070_Financial_Instrument_Transaction_Costs_Ex_Post")):
            t8070_Financial = float(nettoyer_float(colonne_choisie.get("08070_Financial_Instrument_Transaction_Costs_Ex_Post")))
        

        TypeFrais1_percent = t8030_Financial + t8050_Financial + t8080_Financial
        TypeFrais2_percent = 0.0
        TypeFrais3_percent = t8070_Financial

        # Les taux Keys sont donnés sous forme décimal, il faut les multiplier par 100 pour les obtenir sous forme de pourcentage
        TypeFrais1_percent = TypeFrais1_percent * 100
        TypeFrais3_percent = TypeFrais3_percent * 100


        if pd.notna(IntituleProduit):
            print(f"\n→ Colonne {col_index+1} | Produit : {IntituleProduit}")
            print(f"  TypeFrais1_percent : {TypeFrais1_percent} | TypeFrais2_percent : {TypeFrais2_percent} | TypeFrais3_percent : {TypeFrais3_percent} ")

            setter_data_fournisseur_keys(IntituleProduit,TypeFrais1_percent,TypeFrais2_percent,TypeFrais3_percent,"M1")




def colonne_excel_vers_index(colonne_lettre):
    return ord(colonne_lettre.upper()) - ord("A")

def nettoyer_float(valeur):
    if pd.isna(valeur):
        return 0.0
    return str(valeur).replace(",",".").replace("\n", "").strip()
