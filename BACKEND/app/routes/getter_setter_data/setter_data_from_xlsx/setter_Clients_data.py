from app.BDD.database import get_Database_connection
from mysql.connector import Error
import traceback

def setter_data_tclients(Nom, Prenom, Description, Region, Bureau, Conseiller, Entreprise):
    conn = None
    cursor = None

    try : 

        conn = get_Database_connection()
        if not conn:
           print(f"Erreur de connexion à la base de données"),500
            
        cursor = conn.cursor()
        requete =  """
                        INSERT INTO tclients (Nom, Prenom, Description, Region, Bureau, Conseiller, Entreprise)  
                        VALUES (%s,%s,%s,%s,%s,%s,%s) 
                    """               
        valeurs = (Nom, Prenom, Description, Region, Bureau, Conseiller, Entreprise)

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
