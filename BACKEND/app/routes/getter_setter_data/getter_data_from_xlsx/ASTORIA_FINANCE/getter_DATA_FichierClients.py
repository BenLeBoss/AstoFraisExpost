import pandas as pd
import unicodedata
import re
from app.routes.getter_setter_data.setter_data_from_xlsx.setter_DATA_FichierClients import setter_data_tfichier_clientAstoria



def getter_data_FichierClients(Client_doc):
    
    Entreprises = ['ACP', 'ASTORIA COURTAGE', 'KARA FINANCES', 'ERP COURTAGE', 'INVEST CONSULTING', 'SPI CONSEIL', 'FIPAGEST', 'EQUATIO FINANCES', 'SAPIENTA GESTION', 'IN PATRIMOINE', 'ACTION PATRIMOINE CONSEIL',
                   'APC IMMOBILIER', 'PARISII', 'BC FINANCES', 'SOLVE PATRIMOINE', 'CAPIUM', 'FAMILY PATRIMOINE', 'PB WEALTH MANAGER', 'CV FINANCES', 'SYNERGIE CONSEILS PATRIMOINE',
                   'MY FAMILY OFFICER']
    
    Contenu_NonDesire_Colonne_ConseillerPrincipal = Recuperation_contenu_colonne_conseillerprincipal(Client_doc, Entreprises)
    Contenu_NonDesire_Colonne_AutreConseiller = Recuperation_contenu_colonne_autreconseiller(Client_doc, Contenu_NonDesire_Colonne_ConseillerPrincipal, Entreprises)
    NumClient = 2
    
    print(Contenu_NonDesire_Colonne_ConseillerPrincipal)
    print(Contenu_NonDesire_Colonne_AutreConseiller)
    print("\n\n")

    for index, row in Client_doc.iterrows():

        #si la colonne 'NOM' est remplie
        if pd.notna(row["Nom"]):
            Num_ligne = index


            # ---------RÉCUPÉRATION DES DONNÉES DU CLIENT------------
            Nom = str(row["Nom"]).upper()
            if pd.notna(row["Prénom"]):
                Prenom = str(row["Prénom"]).lower().capitalize()
            else:
                Prenom = ''

            Region = ''
            Bureau = ''
            ConseillerPrincipal = ''

            if row["Conseiller principal"] in Contenu_NonDesire_Colonne_ConseillerPrincipal:
                if 'region' in str(row["Conseiller principal"]).lower():
                    Region = row["Conseiller principal"]
            
            if row["Autre conseiller"] in Contenu_NonDesire_Colonne_AutreConseiller:
                if 'bureau' in str(row["Autre conseiller"]).lower():
                    Bureau = row["Autre conseiller"]

            for entreprise in Entreprises:
                if entreprise in row["Conseiller principal"]:
                    Bureau = row["Conseiller principal"]
                    if str(row["Autre conseiller"]).lower().strip() not in ['non défini(e)', 'nan'] and not pd.isna(row["Autre conseiller"]):
                        ConseillerPrincipal = row["Autre conseiller"]

            if str(row["Assistant(e)"]).lower().strip() not in ['non défini(e)', 'nan'] and not pd.isna(row["Assistant(e)"]):
                ConseillerPrincipal = row["Assistant(e)"]

            if not pd.isna(row["Autre conseiller"]) and est_nom_prenom_conseiller(row["Autre conseiller"]):
                ConseillerPrincipal = row["Autre conseiller"]

            Description = f"{Nom} {Prenom}"


            # ---------RÉCUPÉRATION DES DONNÉES DU PRODUIT---------
            EtablissementFournisseur = nettoyer_champ(row["Etablissement"])
            TypeProduit = nettoyer_champ(row["Type du produit"])
            Produit = nettoyer_champ(row["Produit"])
            Intitule = nettoyer_champ(row["Intitulé"])
            

            # ---------RÉCUPÉRATION DES DONNÉES CLIENT/PRODUITS---------
            NumCompte = str(row["N° de compte"])
            if pd.notna(row["Date d'ouverture"]):
                DateOuverture = str(row["Date d'ouverture"])
            else:
                DateOuverture = None
            Compte_01_01_2024 = float(str(row["Compte au 01/01/2024 (€)"]))
            Compte_31_12_2024 = float(str(row["Compte au 31/12/2024 (€)"]))

            
            print(f"""
                    Ligne {NumClient} =  Client NuméroCompte : {NumCompte}, Nom : '{Nom}', Prénom : '{Prenom}', Région : '{Region}', Bureau : '{Bureau}', Conseiller : '{ConseillerPrincipal}', 
                    Etablissement : '{EtablissementFournisseur}', DateOuverture : {DateOuverture}, TypeProduit : '{TypeProduit}', Produit : '{Produit}', Intitule : '{Intitule},
                    Compte_01_01 : {Compte_01_01_2024}, Compte_31_12 : {Compte_31_12_2024} \n
                """)
            NumClient += 1
            setter_data_tfichier_clientAstoria(NumCompte, Nom, Prenom, Description, Region, Bureau, ConseillerPrincipal, EtablissementFournisseur, DateOuverture, TypeProduit, Produit, 
                                      Intitule, Compte_01_01_2024, Compte_31_12_2024, False, 'Astoria')



#permet de récupérer toutes lignes qui ont la colonne de Compte au 31/12/2024 qui est égale à 0.00 (ou inférieur à 0.01 = 1 centime)
def Recuperation_colonne_Compte31decembre(Client_doc):
    valeur = 0
    for index, row in Client_doc.iterrows():
        Num_ligne = index
        Nom = row["Nom"]
        Prenom = row["Prénom"]
        Date_Decembre = row["Compte au 31/12/2024 (€)"]

        if pd.notna(Date_Decembre) and (Date_Decembre < 0.01):
            valeur += 1
            print(f"Ligne {Num_ligne+2} =  Client nom : {Nom}, prénom : {Prenom}")

    print(f"Nombre de compte au 31/12/24 à moins de 1 centime : {valeur}")



#permet de récupérer toutes les valeurs parasites qui ne devraient pas être dans la colonne de Conseiller principal
def Recuperation_contenu_colonne_conseillerprincipal(Client_doc, Entreprise):
    Contenu_Colonne_ConseillerPrincipal = []
    
    for index, row in Client_doc.iterrows():
        col_conseillerPrincipal = str(row["Conseiller principal"])

        if ((col_conseillerPrincipal in Entreprise) or ('region' in col_conseillerPrincipal.lower()) or ('bureau' in col_conseillerPrincipal.lower())
            or (col_conseillerPrincipal.lower() == 'nan')):
            if col_conseillerPrincipal not in Contenu_Colonne_ConseillerPrincipal:
                Contenu_Colonne_ConseillerPrincipal.append(col_conseillerPrincipal)
    """
    print(f'\nTaille tableau d\'éléments non désirés conseiller principal : {len(Contenu_Colonne_ConseillerPrincipal)}')
    for elt in Contenu_Colonne_ConseillerPrincipal:
        print(f"'{elt}',")
    """

    return Contenu_Colonne_ConseillerPrincipal




#permet de récupérer toutes les valeurs parasites qui ne devraient pas être dans la colonne de Autre Conseiller
def Recuperation_contenu_colonne_autreconseiller(Client_doc, Contenu_NonDesire_Colonne_ConseillerPrincipal, Entreprises):
    Contenu_Colonne_AutreConseiller = []
    
    for index, row in Client_doc.iterrows():
        col_autreConseiller = str(row["Autre conseiller"])

        if ((col_autreConseiller in Entreprises) or (col_autreConseiller in Contenu_NonDesire_Colonne_ConseillerPrincipal) 
            or ('bureau' in col_autreConseiller.lower()) or ('region' in col_autreConseiller.lower())
            or (col_autreConseiller.lower() == 'non défini(e)') or (col_autreConseiller.lower() == 'nan')):
            if (col_autreConseiller not in Contenu_Colonne_AutreConseiller):
                Contenu_Colonne_AutreConseiller.append(col_autreConseiller)

    """
    print(f'\nTaille tableau d\'éléments non désirés autre conseiller : {len(Contenu_Colonne_AutreConseiller)}')
    for elt in Contenu_Colonne_AutreConseiller:
        print(f"'{elt}',")
    """

    return Contenu_Colonne_AutreConseiller

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