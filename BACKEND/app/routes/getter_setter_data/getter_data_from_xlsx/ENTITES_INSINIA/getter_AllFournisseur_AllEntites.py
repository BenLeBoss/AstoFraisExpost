import pandas as pd
from pathlib import Path
from app.routes.getter_setter_data.setter_data_from_xlsx.setter_AllFournisseur_Insinia import setter_data_allfournisseurs_insinia


# Récupère TOUS les partenaires et leurs produits pour une entité INSINIA et les stocke dans une seule table SQL
def getter_AllFournisseur_AllEntites(Fichier_EMT, Partenaire, Entite, colonne_valeur=""):
    
    TableSQL = Entites_Tables(Entite)

    match(Partenaire):
        case "ATLANDVOISIN":
            getter_Insinia_ATLANDVOISIN(Fichier_EMT, TableSQL)
 
        case "CORUM":
            getter_Insinia_CORUM(Fichier_EMT, TableSQL)
 
        case "EIFFEL":
            getter_Insinia_EIFFEL(Fichier_EMT, TableSQL)
 
        case "FRANCEVALLEY":
            getter_Insinia_FRANCEVALLEY(Fichier_EMT, TableSQL)
 
        case "KEYS":
            getter_Insinia_KEYS(Fichier_EMT, TableSQL, colonne_valeur)
 
        case "LAFRANCAISE":
            getter_Insinia_LAFRANCAISE(Fichier_EMT, TableSQL)
 
        case "NORMACAPITAL":
            print("AUCUN CODE IMPLÉMENTÉ")
 
        case "PERIAL":
            getter_Insinia_PERIAL(Fichier_EMT, TableSQL)
 
        case "SMALTCAPITAL":
            getter_Insinia_SMALTCAPITAL(Fichier_EMT, TableSQL)
 
        case "THEOREIM":
            getter_Insinia_THEOREIM(Fichier_EMT, TableSQL)
 
        case "URBANPREMIUM":
            getter_Insinia_URBANPREMIUM(Fichier_EMT, TableSQL)
 


def Entites_Tables(Entite):
    match(Entite):
        case "ACTION PATRIMOINE":
            return "fraisexpost.tfournisseur_Insinia_ActionPatrimoineConseilAll"
        
        case "ALLURE FINANCE":
            return "fraisexpost.tfournisseur_Insinia_AllureFinanceAll"
        
        case "BC FINANCES":
            return "fraisexpost.tfournisseur_Insinia_BCFinancesAll"
        
        case "CAPIUM":
            return "fraisexpost.tfournisseur_Insinia_CapiumAll"
        
        case "FAMILY PATRIMOINE":
            return "fraisexpost.tfournisseur_Insinia_FamilyPatrimoineAll"
        
        case "FIPAGEST":
            return "fraisexpost.tfournisseur_Insinia_FipagestAll"
        
        case "MY FAMILY OFFICER":
            return "fraisexpost.tfournisseur_Insinia_MyFamilyOfficerAll"
        
        case "PARISII":
            return "fraisexpost.tfournisseur_Insinia_ParisiiAll"
        
        case "SOLVE PATRIMOINE":
            return "fraisexpost.tfournisseur_Insinia_SolvePatrimoineAll"
        
        case "SYNERGIE CONSEILS PARTIMOINE":
            return "fraisexpost.tfournisseur_Insinia_SynergieConseilsPatrimoineAll"       

        case "WATSON":
            return "fraisexpost.tfournisseur_Insinia_WatsonAll"
        
        

def getter_Insinia_ATLANDVOISIN(Fichier_EMT, TablesSQL):
    print(1)
    
        

def getter_Insinia_CORUM(Fichier_EMT, TablesSQL):
    print(1)
        

def getter_Insinia_EIFFEL(Fichier_EMT, TablesSQL):
    print(1)
        

def getter_Insinia_FRANCEVALLEY(Fichier_EMT, TablesSQL):
    print(1)
        

def getter_Insinia_KEYS(Fichier_EMT, TablesSQL, colonne_valeur):
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

        TypeFrais1_percent = TypeFrais1_percent * 100
        TypeFrais3_percent = TypeFrais3_percent * 100



        if pd.notna(IntituleProduit):
            print(f"\n→ Colonne {col_index+1} | Produit : {IntituleProduit}")
            print(f"  TypeFrais1_percent : {TypeFrais1_percent} | TypeFrais2_percent : {TypeFrais2_percent} | TypeFrais3_percent : {TypeFrais3_percent} \n\n")

            setter_data_allfournisseurs_insinia(Table_recu=TablesSQL, NomProduit_recu=IntituleProduit, TypeFrais1_p_recu=TypeFrais1_percent, TypeFrais2_p_recu=TypeFrais2_percent,
                                                TypeFrais3_p_recu=TypeFrais3_percent, ModeleUtilise_recu="M1")




def getter_Insinia_LAFRANCAISE(Fichier_EMT, TablesSQL):
    print(1)
        

def getter_Insinia_NORMACAPITAL(Fichier_EMT, TablesSQL):
    print(1)
        

def getter_Insinia_PERIAL(Fichier_EMT, TablesSQL):
    print(1)

        

def getter_Insinia_SMALTCAPITAL(Fichier_EMT, TablesSQL):
    print(1)
        

def getter_Insinia_THEOREIM(Fichier_EMT, TablesSQL):
    print(1)
        

def getter_Insinia_URBANPREMIUM(Fichier_EMT, TablesSQL):
    print(1)
        



















# -----------------------------Procédures utiles à la récupération des données



def colonne_excel_vers_index(colonne_lettre):
    return ord(colonne_lettre.upper()) - ord("A")

def nettoyer_float(valeur):
    if pd.isna(valeur):
        return 0.0
    return str(valeur).replace(",",".").replace("\n", "").strip()
