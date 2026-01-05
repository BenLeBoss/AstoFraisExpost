from app.BDD.database import get_Database_connection
from mysql.connector import Error
import traceback


def setter_data_tfichier_clientAstoria(NumCompte, Nom, Prenom, Description, Region, Bureau, ConseillerPrincipal, EtablissementFournisseur, DateOuverture, TypeProduit, Produit, 
                                       Intitule, Compte_01_01_2024, Compte_31_12_2024, EstGenere, Entreprise):
    conn = None
    cursor = None

    try : 

        conn = get_Database_connection()
        if not conn:
           print(f"Erreur de connexion à la base de données")
            
        cursor = conn.cursor()
        requete =  """
                        INSERT INTO tfichier_clientAstoria (NumeroCompte, Nom, Prenom, Description, Region, Bureau, Conseiller, EtablissementFournisseur, DateOuverture, 
                                                                TypeProduit, Produit, Intitule, Compte_au_01_01_2024, Compte_au_31_12_2024, EstGenere, Entreprise)  
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,STR_TO_DATE(%s,"%d/%m/%Y"),%s,%s,%s,%s,%s,%s,%s) 
                    """               
        valeurs = (NumCompte, Nom, Prenom, Description, Region, Bureau, ConseillerPrincipal, EtablissementFournisseur, DateOuverture, TypeProduit, Produit, 
                        Intitule, Compte_01_01_2024, Compte_31_12_2024, EstGenere, Entreprise)

        cursor.execute(requete, valeurs)
        conn.commit()


    except Error as e:
        traceback.print_exc()
        print(f"Erreur lors de l'insertion en base de l'ajout d'élément : {str(e)}")
    
    finally: 
        if cursor :
            cursor.close()
        if conn:
            conn.close()


def setter_data_tfichier_clientInsinia(Table, NumCompte, Nom, Prenom, Description, Region, Bureau, ConseillerPrincipal, EtablissementFournisseur, DateOuverture, TypeProduit, Produit, 
                                       Intitule, Compte_01_01_2024, Compte_31_12_2024, EstGenere, Entreprise):
    conn = None
    cursor = None

    try : 

        conn = get_Database_connection()
        if not conn:
           print(f"Erreur de connexion à la base de données")
            
        cursor = conn.cursor()
        requete =  f"""
                        INSERT INTO {Table} (NumeroCompte, Nom, Prenom, Description, Region, Bureau, Conseiller, EtablissementFournisseur, DateOuverture, 
                                                                TypeProduit, Produit, Intitule, Compte_au_01_01_2024, Compte_au_31_12_2024, EstGenere, Entreprise)  
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,STR_TO_DATE(%s,"%d/%m/%Y"),%s,%s,%s,%s,%s,%s,%s) 
                    """               
        valeurs = ( NumCompte, Nom, Prenom, Description, Region, Bureau, ConseillerPrincipal, EtablissementFournisseur, DateOuverture, TypeProduit, Produit, 
                        Intitule, Compte_01_01_2024, Compte_31_12_2024, EstGenere, Entreprise)

        cursor.execute(requete, valeurs)
        conn.commit()


    except Error as e:
        traceback.print_exc()
        print(f"Erreur lors de l'insertion en base de l'ajout d'élément : {str(e)}")
    
    finally: 
        if cursor :
            cursor.close()
        if conn:
            conn.close()


