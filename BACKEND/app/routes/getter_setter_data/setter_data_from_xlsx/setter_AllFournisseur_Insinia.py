from app.BDD.database import get_Database_connection
from mysql.connector import Error
import traceback

def setter_data_allfournisseurs_insinia(Table_recu=None, Civilite_recu=None, NumeroCompte_recu=None, Nom_recu=None, Prenom_recu=None, NomProduit_recu=None, DateSouscription_recu=None, 
                                        TypeFrais1_p_recu=0.0, TypeFrais1_eu_recu=0.0, TypeFrais2_p_recu=0.0, TypeFrais2_eu_recu=0.0, TypeFrais3_p_recu=0.0, TypeFrais3_eu_recu=0.0, 
                                        TauxFraisTransaction_recu=0.0, MontantFraisTransaction_recu=0.0, MontantTotalSouscritAnneeCourante_recu=0.0, MontantTotalSouscrit_recu=0.0, 
                                        ModeleUtilise_recu=None ):


    conn = None
    cursor = None

    try : 

        conn = get_Database_connection()
        if not conn:
           print(f"Erreur de connexion à la base de données"),500
            
        cursor = conn.cursor()     

        requete =  f"""
                        INSERT INTO {Table_recu} (Civilite, Nom, Prenom, NumeroCompte, NomProduit, DateSouscription, TypeFrais1_p, TypeFrais1_eu, TypeFrais2_p, TypeFrais2_eu, 
                        TypeFrais3_p, TypeFrais3_eu, TauxFraisTransaction, MontantFraisTransaction, MontantTotalSouscritAnneeCourante, MontantTotalSouscrit, ModeleUtilise)  
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)   
                    """ 
        valeurs = (Civilite_recu, Nom_recu, Prenom_recu, NumeroCompte_recu, NomProduit_recu, DateSouscription_recu, TypeFrais1_p_recu, TypeFrais1_eu_recu, TypeFrais2_p_recu, 
                   TypeFrais2_eu_recu, TypeFrais3_p_recu, TypeFrais3_eu_recu, TauxFraisTransaction_recu, MontantFraisTransaction_recu, MontantTotalSouscritAnneeCourante_recu, 
                   MontantTotalSouscrit_recu, ModeleUtilise_recu )

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


