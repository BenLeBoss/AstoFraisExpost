from app.BDD.database import get_Database_connection
from mysql.connector import Error
import traceback

def setter_data_tclient_produits(IDClient, IDProduit, NumeroCompte, DateOuverture, Compte_au_01_01_2024, Compte_au_31_12_2024, LigneAjoutée):
    conn = None
    cursor = None

    try : 

        conn = get_Database_connection()
        if not conn:
           print(f"Erreur de connexion à la base de données"),500
            
        cursor = conn.cursor()
        requete =  """
                        INSERT INTO Tclient_produits (IDClient, IDProduit, NumeroCompte, DateOuverture, Compte_au_01_01_2024, Compte_au_31_12_2024, EstGenere)  
                        VALUES (%s,%s,%s,STR_TO_DATE(%s,"%d/%m/%Y"),%s,%s,%s) 
                    """               
        valeurs = (IDClient, IDProduit, NumeroCompte, DateOuverture, Compte_au_01_01_2024, Compte_au_31_12_2024, False)

        cursor.execute(requete, valeurs)
        conn.commit()

        print(f"Élément {LigneAjoutée} ajouté !")

    except Error as e:
        traceback.print_exc()
        print(f"Erreur lors de l'insertion en base de l'ajout d'élément : {str(e)}"), 500
    
    finally: 
        if cursor :
            cursor.close()
        if conn:
            conn.close()