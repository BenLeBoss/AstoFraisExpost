from app.BDD.database import get_Database_connection
from mysql.connector import Error
import traceback

def setter_data_tproduits(EtablissementFournisseur, TypeProduit, Produit, Intitule):
    conn = None
    cursor = None

    try : 

        conn = get_Database_connection()
        if not conn:
           print(f"Erreur de connexion à la base de données"),500
            
        cursor = conn.cursor()
        requete =  """
                        INSERT INTO tproduits (EtablissementFournisseur, TypeProduit, Produit, Intitule)  
                        VALUES (%s,%s,%s,%s) 
                    """               
        valeurs = (EtablissementFournisseur, TypeProduit, Produit, Intitule)

        cursor.execute(requete, valeurs)
        conn.commit()


    except Error as e:
        traceback.print_exc()
        print(f"Erreur lors de l'insertion en base de l'ajout d'élément : {str(e)}"), 500
    
    finally: 
        if cursor :
            cursor.close()
        if conn:
            conn.close()
