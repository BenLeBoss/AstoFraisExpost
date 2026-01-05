import pandas as pd
import unicodedata
import re

from app.routes.getter_setter_data.setter_data_from_xlsx.setter_Produits_data import setter_data_tproduits



def getter_data_produits(Client_doc):
    
    Tab_Produits = []
    ligne = 1

    for index, row in Client_doc.iterrows():

        #si la colonne 'PRODUIT' est remplie
        if pd.notna(row["Produit"]):
            Num_ligne = index
            EtablissementFournisseur = nettoyer_champ(row["Etablissement"])
            TypeProduit = nettoyer_champ(row["Type du produit"])
            Produit = nettoyer_champ(row["Produit"])
            Intitule = nettoyer_champ(row["Intitulé"])

            Description = f"{EtablissementFournisseur} {TypeProduit} {Produit} {Intitule}"

            if Description not in Tab_Produits:
                #print(f"Ligne {Num_ligne+2} =  Etablissement : '{EtablissementFournisseur}', TypeProduit : '{TypeProduit}', Produit : '{Produit}', Intitule : '{Intitule}'")
                print(f"Ligne {ligne} =  Etablissement : '{EtablissementFournisseur}', TypeProduit : '{TypeProduit}', Produit : '{Produit}', Intitule : '{Intitule}'")
                Tab_Produits.append(Description)
                ligne += 1
                #setter_data_tproduits(EtablissementFournisseur, TypeProduit, Produit, Intitule)


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