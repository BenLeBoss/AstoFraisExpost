import pandas as pd
import unicodedata
import re
from app.routes.getter_setter_data.setter_data_from_xlsx.setter_DATA_FichierClients import setter_data_tfichier_clientInsinia


# Récupère tous les clients d'une entité
def getter_data_FichierClientsInsinia(Client_doc, Entite):
    
    Table = Entites_Tables(Entite)

    NumClient = 2
    for index, row in Client_doc.iterrows():

        #si la colonne 'NOM' est remplie
        if 'Nom' in Client_doc.columns and pd.notna(row["Nom"]):

            # ---------RÉCUPÉRATION DES DONNÉES DU CLIENT------------
            Nom = str(row["Nom"]).upper()

            Prenom = ''
            if 'Prénom' in Client_doc.columns and pd.notna(row["Prénom"]):
                Prenom = str(row["Prénom"]).lower().capitalize()

            ConseillerPrincipal = ''
            if 'Conseiller principal' in Client_doc.columns and pd.notna(row["Conseiller principal"]):
                ConseillerPrincipal = row["Conseiller principal"]

            Region = ''
            Bureau = ''

            Description = f"{Nom} {Prenom}"


            # ---------RÉCUPÉRATION DES DONNÉES DU PRODUIT---------
            EtablissementFournisseur = ''
            if 'Etablissement' in Client_doc.columns and pd.notna(row["Etablissement"]):
                EtablissementFournisseur = nettoyer_champ(row["Etablissement"])

            TypeProduit = ''
            if 'Type du produit' in Client_doc.columns and pd.notna(row["Etablissement"]):
                TypeProduit = nettoyer_champ(row["Type du produit"])

            Produit = ''
            if 'Produit' in Client_doc.columns and pd.notna(row["Produit"]):
                Produit = nettoyer_champ(row["Produit"])

            Intitule = ''
            if 'Intitulé' in Client_doc.columns and pd.notna(row["Intitulé"]):
                Intitule = nettoyer_champ(row["Intitulé"])

            # ---------RÉCUPÉRATION DES DONNÉES CLIENT/PRODUITS---------
            NumCompte = ''
            if 'N° de compte' in Client_doc.columns and pd.notna(row["N° de compte"]):
                NumCompte = str(row["N° de compte"])

            DateOuverture = ''
            if 'Date d\'ouverture' in Client_doc.columns and pd.notna(row["Date d'ouverture"]):
                DateOuverture = str(row["Date d'ouverture"])

            Compte_01_01_2024 = 0
            if 'Compte au 01/01/2024 (€)' in Client_doc.columns and pd.notna(row["Compte au 01/01/2024 (€)"]):
                Compte_01_01_2024 = float(str(row["Compte au 01/01/2024 (€)"]))

            Compte_31_12_2024 = 0
            if 'Compte au 31/12/2024 (€)' in Client_doc.columns and pd.notna(row["Compte au 31/12/2024 (€)"]):
                Compte_31_12_2024 = float(str(row["Compte au 31/12/2024 (€)"]))

            print(f"""
                    Ligne {NumClient} =  Client : {NumCompte}, {Nom} {Prenom}, Conseiller : '{ConseillerPrincipal}', 
                    Etablissement : '{EtablissementFournisseur}', DateOuverture : {DateOuverture}, TypeProduit : '{TypeProduit}', Produit : '{Produit}', Intitule : '{Intitule},
                    Compte_01_01 : {Compte_01_01_2024}, Compte_31_12 : {Compte_31_12_2024} \n
                """)
            NumClient += 1
            #setter_data_tfichier_clientInsinia(Table, NumCompte, Nom, Prenom, Description, Region, Bureau, ConseillerPrincipal, EtablissementFournisseur, DateOuverture, 
            #                                   TypeProduit, Produit, Intitule, Compte_01_01_2024, Compte_31_12_2024, False, Entite)



# en fonction du paramètre 'entite' donné dans le main.py, on renvoie la table sql correspondante
def Entites_Tables(Entite):
    match(Entite):
        case "ACTION PATRIMOINE":
            return "fraisexpost.tfichier_clientInsinia_ActionPatrimoine"
        
        case "ALLURE FINANCE":
            return "fraisexpost.tfichier_clientInsinia_AllureFinance"
        
        case "BC FINANCES":
            return "fraisexpost.tfichier_clientInsinia_BCFinances"
        
        case "CAPIUM":
            return "fraisexpost.tfichier_clientInsinia_Capium"
        
        case "FAMILY PATRIMOINE":
            return "fraisexpost.tfichier_clientInsinia_FamilyPatrimoine"
        
        case "FIPAGEST":
            return "fraisexpost.tfichier_clientInsinia_Fipagest"
        
        case "MY FAMILY OFFICER":
            return "fraisexpost.tfichier_clientInsinia_MyFamilyOfficer"
        
        case "PARISII":
            return "fraisexpost.tfichier_clientInsinia_Parisii"
        
        case "SOLVE PATRIMOINE":
            return "fraisexpost.tfichier_clientInsinia_SolvePatrimoine"
        
        case "SYNERGIE CONSEILS PARTIMOINE":
            return "fraisexpost.tfichier_clientInsinia_SynergieConseilsPatrimoine"       

        case "WATSON":
            return "fraisexpost.tfichier_clientInsinia_Watson"
        





# reforme les champs de produits pour ne pas avoir de doublons dans la base de données
def nettoyer_champ(champ):
    if pd.isna(champ):
        return ''
    champ = str(champ).upper()

    # Remplace les ligatures Unicode manuellement
    ligatures = {
        'Œ': 'OE',
        'œ': 'OE',
        'Æ': 'AE',
        'æ': 'AE',
    }
    for ligature, replacement in ligatures.items():
        champ = champ.replace(ligature, replacement)

    # décompose les accents
    champ = unicodedata.normalize('NFKD', champ)  

    # enlève les accents
    champ = ''.join(c for c in champ if not unicodedata.combining(c))  

    # enlève les espaces en début/fin
    champ = champ.strip()  

    # remplace les espaces multiples par un seul
    champ = re.sub(r'\s+', ' ', champ)  


    return champ

# Test avec regex
def est_nom_prenom_conseiller(chaine):
    motif = r"""^
        (?:[A-Z]+(?:[-'\s][A-Z]+)*)    # Une ou plusieurs parties du NOM en majuscules, séparées par - ' ou espace
        \s                             # Séparateur entre noms et prénoms
        (?:[A-Z][a-z]+(?:[-'][A-Za-z]+)*  # Un prénom capitalisé avec éventuellement - ou '
            (?:\s[A-Z][a-z]+(?:[-'][A-Za-z]+)*)*  # D'autres prénoms optionnels
        )$
    """
    return bool(re.match(motif, chaine, re.VERBOSE))