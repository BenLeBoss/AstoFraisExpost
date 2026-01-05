import pandas as pd
import unicodedata
import re
from pathlib import Path
from app.routes.getter_setter_data.setter_data_from_xlsx.setter_Fournisseurs_data import setter_data_fournisseur_alpheys


# Récupère TOUS les produits vendus sur la plateforme Alpheys en fonction du type de fichier EMT envoyé par le partenaire (liste de personnes ou de produits)
def getter_data_fournisseur_Alpheys_AllProduits(Fichier_EMT, TypeFichier):
    
    match(TypeFichier):
        case 'Produits':
            getter_Fournisseur_Alpheys_byProduits(Fichier_EMT)

        case 'Personnes':
            getter_Fournisseur_Alpheys_byPersonnes(Fichier_EMT)

        case 'Pourcentage':
            getter_Fournisseur_Alpheys_byPourcentage(Fichier_EMT)

        case _:
            print("Erreur : Variable 'TypeFichier' non valide ou non renseigné")



def getter_Fournisseur_Alpheys_byProduits(Fichier_EMT):

    # met toutes les colonnes en minuscule
    Fichier_EMT.columns = Fichier_EMT.columns.str.lower()

    for index, row in Fichier_EMT.iterrows():

        # si la colonne du nom de produit est remplie
        if '00030_financial_instrument_name' in Fichier_EMT.columns and pd.notna(row["00030_financial_instrument_name"]):
            Num_ligne = index

            IntituleProduit = str(row["00030_financial_instrument_name"])

            t8030_Financial = 0.0
            t8050_Financial = 0.0
            t8080_Financial = 0.0
            t8070_Financial = 0.0

            if '08030_financial_instrument_ongoing_costs_ex_post' in Fichier_EMT.columns and pd.notna(row["08030_financial_instrument_ongoing_costs_ex_post"]):
                t8030_Financial = float(nettoyer_float(row["08030_financial_instrument_ongoing_costs_ex_post"]))

            if '08050_financial_instrument_management_fee_ex_post' in Fichier_EMT.columns and pd.notna(row["08050_financial_instrument_management_fee_ex_post"]):
                t8050_Financial = float(nettoyer_float(row["08050_financial_instrument_management_fee_ex_post"]))

            if '08080_financial_instrument_incidental_costs_ex_post' in Fichier_EMT.columns and pd.notna(row["08080_financial_instrument_incidental_costs_ex_post"]):    
                t8080_Financial = float(nettoyer_float(row["08080_financial_instrument_incidental_costs_ex_post"]))

            if '08070_financial_instrument_transaction_costs_ex_post' in Fichier_EMT.columns and pd.notna(row["08070_financial_instrument_transaction_costs_ex_post"]):
                t8070_Financial = float(nettoyer_float(row["08070_financial_instrument_transaction_costs_ex_post"]))

            TypeFrais1_percent = t8030_Financial + t8050_Financial + t8080_Financial
            TypeFrais2_percent = 0.0
            TypeFrais3_percent = t8070_Financial


            # Les taux du produit Pierval Santé sont donnés sous forme décimal, il faut les multiplier par 100 pour les obtenir sous forme de pourcentage
            TypeFrais1_percent = TypeFrais1_percent * 100
            TypeFrais3_percent = TypeFrais3_percent * 100


            print(f"Ligne {Num_ligne+2} =  Nom Produit : '{IntituleProduit}'")
            print(f"            Frais 1 (%) : '{TypeFrais1_percent}' // Frais 2 (%) : '{TypeFrais2_percent}' // Frais 3 (%) : '{TypeFrais3_percent}'\n")
            setter_data_fournisseur_alpheys( NomProduit_recu=IntituleProduit, TypeFrais1_p_recu=TypeFrais1_percent, TypeFrais2_p_recu=TypeFrais2_percent,
                                                TypeFrais3_p_recu=TypeFrais3_percent, ModeleUtilise_recu="M1")




def getter_Fournisseur_Alpheys_byPersonnes(Fichier_EMT):

    # met toutes les colonnes en minuscules et enlève les espaces parasites
    Fichier_EMT.columns = Fichier_EMT.columns.str.lower()

    NumClient = 2
    for index, row in Fichier_EMT.iterrows():

        # si la colonne 'nom' est remplie
        if 'nom' in Fichier_EMT.columns and pd.notna(row["nom"]):

            # ---------RÉCUPÉRATION DES DONNÉES DU CLIENT------------
            Nom = str(row["nom"]).upper()

            Prenom = ''
            if 'prénom' in Fichier_EMT.columns and pd.notna(row["prénom"]):
                Prenom = str(row["prénom"]).lower().capitalize()

            Civilite = ''
            if 'civilite' in Fichier_EMT.columns and pd.notna(row["précivilitenom"]):
                Civilite = str(row["civilite"]).lower().capitalize()

            IntituleProduit = ''
            if 'produit' in Fichier_EMT.columns and pd.notna(row["produit"]):
                IntituleProduit = str(row["produit"])

            TypeFrais1_percent = ''
            if '% type de frais n°1' in Fichier_EMT.columns and pd.notna(row["% type de frais n°1"]):
                TypeFrais1_percent = str(row["% type de frais n°1"])

            TypeFrais1_euros = ''
            if 'type de frais n°1' in Fichier_EMT.columns and pd.notna(row["type de frais n°1"]):
                TypeFrais1_euros = str(row["type de frais n°1"])

            TypeFrais2_percent = ''
            if '% type de frais n°2' in Fichier_EMT.columns and pd.notna(row["% type de frais n°2"]):
                TypeFrais2_percent = str(row["% type de frais n°2"])
            
            TypeFrais2_euros = ''
            if 'type de frais n°2' in Fichier_EMT.columns and pd.notna(row["type de frais n°2"]):
                TypeFrais2_euros = str(row["type de frais n°2"])

            TypeFrais3_percent = ''
            if '% type de frais n°3' in Fichier_EMT.columns and pd.notna(row["% type de frais n°3"]):
                TypeFrais3_percent = str(row["% type de frais n°3"])
            
            TypeFrais3_euros = ''
            if 'type de frais n°3' in Fichier_EMT.columns and pd.notna(row["type de frais n°3"]):
                TypeFrais3_euros = str(row["type de frais n°3"])


            MontantSouscritAnneeCourante = ''
            if "montant souscrit au cours de l'exercice" in Fichier_EMT.columns and pd.notna(row["montant souscrit au cours de l'exercice"]):
                MontantSouscritAnneeCourante = str(row["montant souscrit au cours de l'exercice"])

            TauxFraisTransaction = ''
            if 'taux de frais transaction' in Fichier_EMT.columns and pd.notna(row["taux de frais transaction"]):
                TauxFraisTransaction = str(float(row["taux de frais transaction"]) * 100)

            TotalFraisTransactionAnneeCourante = ''
            if "frais relatifs à la transaction (droits entrée + com. partenaire)" in Fichier_EMT.columns and pd.notna(row["frais relatifs à la transaction (droits entrée + com. partenaire)"]):
                TotalFraisTransactionAnneeCourante = str(row["frais relatifs à la transaction (droits entrée + com. partenaire)"])


            MontantTotalSouscrit = ''
            if 'montant total des encours' in Fichier_EMT.columns and pd.notna(row["montant total des encours"]):
                MontantTotalSouscrit = row["montant total des encours"]


            print(f"Ligne {NumClient+2} =  Client nom : '{Nom}', Prénom : '{Prenom}', Produit : '{IntituleProduit}'")
            print(f"            Frais 1 (%, euros) : '{TypeFrais1_percent}, {TypeFrais1_euros}' // Frais 2 (%, euros) : '{TypeFrais2_percent}, {TypeFrais2_euros}' // Frais 3 (%, euros) : '{TypeFrais3_percent}, {TypeFrais3_euros}'")
            
            NumClient += 1
            setter_data_fournisseur_alpheys(Civilite_recu=Civilite, Nom_recu=Nom, Prenom_recu=Prenom, NomProduit_recu=IntituleProduit,TypeFrais1_p_recu=TypeFrais1_percent, 
                                            TypeFrais1_eu_recu=TypeFrais1_euros, TypeFrais2_p_recu=TypeFrais2_percent, TypeFrais2_eu_recu=TypeFrais2_euros, 
                                            TypeFrais3_p_recu=TypeFrais3_percent, TypeFrais3_eu_recu=TypeFrais3_euros, TauxFraisTransaction_recu=TauxFraisTransaction, 
                                            MontantFraisTransaction_recu=TotalFraisTransactionAnneeCourante, MontantTotalSouscritAnneeCourante_recu=MontantSouscritAnneeCourante, 
                                            MontantTotalSouscrit_recu=MontantTotalSouscrit, ModeleUtilise_recu="M4" )



def getter_Fournisseur_Alpheys_byPourcentage(Fichier_EMT):

    # met toutes les colonnes en minuscule
    Fichier_EMT.columns = Fichier_EMT.columns

    for index, row in Fichier_EMT.iterrows():

        # si la colonne du nom de produit est remplie
        if 'Produit' in Fichier_EMT.columns and pd.notna(row["Produit"]):
            Num_ligne = index

            IntituleProduit = str(row["Produit"])

            if 'Frais immobiliers' in Fichier_EMT.columns and pd.notna(row["Frais immobiliers"]):
                TypeFrais1_percent = float(nettoyer_float(row["Frais immobiliers"]))*100

            if 'Frais récurrents' in Fichier_EMT.columns and pd.notna(row["Frais récurrents"]):
                TypeFrais2_percent = float(nettoyer_float(row["Frais récurrents"]))*100

            if 'Frais de transactions' in Fichier_EMT.columns and pd.notna(row["Frais de transactions"]):    
                TypeFrais3_percent = float(nettoyer_float(row["Frais de transactions"]))*100



            print(f"Ligne {Num_ligne+2} =  Nom Produit : '{IntituleProduit}'")
            print(f"            Frais 1 (%) : '{TypeFrais1_percent}' // Frais 2 (%) : '{TypeFrais2_percent}' // Frais 3 (%) : '{TypeFrais3_percent}'\n")
            setter_data_fournisseur_alpheys( NomProduit_recu=IntituleProduit, TypeFrais1_p_recu=TypeFrais1_percent, TypeFrais2_p_recu=TypeFrais2_percent,
                                                TypeFrais3_p_recu=TypeFrais3_percent, ModeleUtilise_recu="M2")





# -----------------------------Procédures utiles à la récupération des données



def colonne_excel_vers_index(colonne_lettre):
    return ord(colonne_lettre.upper()) - ord("A")

def nettoyer_float(valeur):
    if pd.isna(valeur):
        return 0.0
    return str(valeur).replace(",",".").replace("\n", "").strip()


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