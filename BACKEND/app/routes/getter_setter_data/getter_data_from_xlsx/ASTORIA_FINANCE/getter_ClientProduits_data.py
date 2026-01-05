import pandas as pd
import unicodedata
import re
import traceback
from mysql.connector import Error

from app.routes.getter_setter_data.setter_data_from_xlsx.setter_ClientProduits_data import setter_data_tclient_produits
from app.BDD.database import get_Database_connection


def getter_data_clientproduits(Client_doc):
    
    LigneAjoutée = 1

    for index, row in Client_doc.iterrows():

        #si les colonne 'PRODUIT' et 'NOM' sont remplies
        if pd.notna(row["Produit"]) and pd.notna(row["Nom"]) :
            Num_ligne = index
            NumCompte = str(row["N° de compte"])
            Nom = str(row["Nom"]).upper()
            if pd.notna(row["Prénom"]):
                Prenom = str(row["Prénom"]).lower().capitalize()
            else:
                Prenom = ''
            if pd.notna(row["Date d'ouverture"]):
                DateOuverture = str(row["Date d'ouverture"])
            else:
                DateOuverture = None
            EtablissementFournisseur = nettoyer_champ(row["Etablissement"])
            TypeProduit = nettoyer_champ(row["Type du produit"])
            Produit = nettoyer_champ(row["Produit"])
            Intitule = nettoyer_champ(row["Intitulé"])
            Compte_01_01_2024 = float(str(row["Compte au 01/01/2024 (€)"]))
            Compte_31_12_2024 = float(str(row["Compte au 31/12/2024 (€)"]))


            Concat_Client = f"{Nom} {Prenom}"
            Concat_Produit = f"{EtablissementFournisseur} {TypeProduit} {Produit} {Intitule}"
            
            IDClient, IDProduit = get_IDs(Concat_Client, Concat_Produit)
            setter_data_tclient_produits(IDClient, IDProduit, NumCompte, DateOuverture, Compte_01_01_2024, Compte_31_12_2024, LigneAjoutée)
            LigneAjoutée += 1
            print(f"Ligne {Num_ligne+2} =  Client nom : '{Nom}', Prénom : '{Prenom}', IDClient : {IDClient}, Etablissement : {EtablissementFournisseur}, Produit : {Produit}, IDProduit : {IDProduit}")
            


#récupère les IDs coorespondant au client et à son produit
def get_IDs(Concat_Client, Concat_Produit):

    

    conn = None
    IDClient = None
    IDProduit = None
    try :     

        conn = get_Database_connection()
        if not conn:
                print(f"Erreur de connexion à la base de données")
            
        IDClient = get_ClientID(conn, Concat_Client)
        IDProduit = get_ProduitID(conn, Concat_Produit)

        return IDClient, IDProduit

    except Error as e:
        if IDClient is not None:
            print("IDClient : " + str(IDClient))
        if IDProduit is not None:
            print("IDProduit : " + str(IDProduit))
        print("Concat_Client : '" + Concat_Client + "'")
        print("Concat_Produit : '" + Concat_Produit + "'")
        traceback.print_exc()
        print("Erreur lors de la récupération de données de la base")
        raise
    finally:
        if conn:
            conn.close()


#récup l'ID Client
def get_ClientID(conn, Concat_Client):
    cursor = None

    try :     
        cursor = conn.cursor()
        requete = "SELECT c.ID FROM tclients c WHERE concat(c.Nom,' ',c.Prenom) COLLATE utf8mb4_bin = %s COLLATE utf8mb4_bin"
        cursor.execute(requete, (Concat_Client,))
            
        client = cursor.fetchone()

        if client :
            return str(client[0])
        else:
            return None
        
    except Error as e:
        traceback.print_exc()
        print(f"Erreur lors de la récupération de données de la base")
        raise
    finally: 
        if cursor :
            cursor.close()


#récup l'ID Produit
def get_ProduitID(conn, Concat_Produit):
    cursor = None

    try :     
        cursor = conn.cursor()
        requete = "SELECT p.ID FROM tproduits p WHERE concat(p.EtablissementFournisseur,' ',p.TypeProduit, ' ',p.Produit,' ',p.Intitule) = %s"
        cursor.execute(requete, (Concat_Produit,))
            
        produit = cursor.fetchone()

        if produit :
            return str(produit[0])
        else:
            return None
        
    except Error as e:
        traceback.print_exc()
        print(f"Erreur lors de la récupération de données de la base")
        raise
    finally: 
        if cursor :
            cursor.close()



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