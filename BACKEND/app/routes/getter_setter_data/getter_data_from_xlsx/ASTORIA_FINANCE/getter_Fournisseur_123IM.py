import pandas as pd
from pathlib import Path
from app.routes.getter_setter_data.setter_data_from_xlsx.setter_Fournisseurs_data import setter_data_fournisseur_123IM


def getter_data_fournisseur_123IM(Fichier_EMT, colonne_valeur):
    start_col = colonne_excel_vers_index(colonne_valeur)-1
    
    nb_colonnes = Fichier_EMT.shape[1]
    index_lignes = Fichier_EMT.iloc[:, 0] 

    for col_index in range(start_col, nb_colonnes):
        colonne_choisie = Fichier_EMT.iloc[:, col_index]
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
        
        
        # Les taux 123IM sont donnés sous forme décimal, il faut les multiplier par 100 pour les obtenir sous forme de pourcentage        
        TypeFrais1_percent = TypeFrais1_percent * 100
        TypeFrais3_percent = TypeFrais3_percent * 100


        if pd.notna(IntituleProduit):
            print(f"\n→ Colonne {col_index+1} | Produit : {IntituleProduit}")
            print(f"  TypeFrais1_percent : {TypeFrais1_percent} | TypeFrais2_percent : {TypeFrais2_percent} | TypeFrais3_percent : {TypeFrais3_percent} ")
            setter_data_fournisseur_123IM( IntituleProduit=IntituleProduit ,TypeFrais1_percent=TypeFrais1_percent,TypeFrais2_percent=TypeFrais2_percent,
                                                TypeFrais3_percent=TypeFrais3_percent,ModeleUtilise="M1")



# --------------Procédures utiles à la récupération des données

def colonne_excel_vers_index(colonne_lettre):
    return ord(colonne_lettre.upper()) - ord("A")

def nettoyer_float(valeur):
    if pd.isna(valeur):
        return 0.0
    return str(valeur).replace(",",".").replace("\n", "").strip()