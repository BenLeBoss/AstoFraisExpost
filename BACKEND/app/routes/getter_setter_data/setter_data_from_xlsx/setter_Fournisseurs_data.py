from app.BDD.database import get_Database_connection
from mysql.connector import Error
import traceback

def setter_data_fournisseurs(requete, valeurs):
    conn = None
    cursor = None

    try : 

        conn = get_Database_connection()
        if not conn:
           print(f"Erreur de connexion à la base de données"),500
            
        cursor = conn.cursor()     

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


# PERIAL
def setter_data_fournisseur_perial(Nom, Prenom, NumeroCompte, NomProduit, TypeFrais1_p, TypeFrais1_eu, TypeFrais2_p, TypeFrais2_eu, TypeFrais3_p, TypeFrais3_eu, ModeleUtilise):
    
    requete =  """
                        INSERT INTO fraisexpost.tfournisseur_perial (Nom, Prenom, NumeroCompte, NomProduit, TypeFrais1_p, TypeFrais1_eu, TypeFrais2_p, TypeFrais2_eu, 
                        TypeFrais3_p, TypeFrais3_eu, ModeleUtilise)  
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s, %s) 
                    """ 
    valeurs = (Nom, Prenom, NumeroCompte, NomProduit, TypeFrais1_p, TypeFrais1_eu, TypeFrais2_p, TypeFrais2_eu, TypeFrais3_p, TypeFrais3_eu, ModeleUtilise)

    setter_data_fournisseurs(requete, valeurs)


# FRANCE VALLEY
def setter_data_fournisseur_francevalley(Nom, Prenom, NomProduit, TypeFrais1_p, TypeFrais1_eu, TypeFrais2_p, TypeFrais2_eu, TypeFrais3_p, TypeFrais3_eu, 
                                         TauxFraisTransaction, MontantFraisTransaction, MontantTotalSouscritAnneeCourante, MontantTotalSouscrit, ModeleUtilise):
    
    requete =  """
                        INSERT INTO fraisexpost.tfournisseur_francevalley (Nom, Prenom, NomProduit, TypeFrais1_p, TypeFrais1_eu, TypeFrais2_p, TypeFrais2_eu, 
                        TypeFrais3_p, TypeFrais3_eu, TauxFraisTransaction, MontantFraisTransaction, MontantTotalSouscritAnneeCourante, MontantTotalSouscrit, ModeleUtilise)  
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                    """ 
    valeurs = (Nom, Prenom, NomProduit, TypeFrais1_p, TypeFrais1_eu, TypeFrais2_p, TypeFrais2_eu, TypeFrais3_p, TypeFrais3_eu, TauxFraisTransaction, MontantFraisTransaction, 
               MontantTotalSouscritAnneeCourante, MontantTotalSouscrit, ModeleUtilise)

    setter_data_fournisseurs(requete, valeurs)


# ATLAND VOISIN
def setter_data_fournisseur_atlandvoisin(Civilite, Nom, Prenom, NomProduit, TypeFrais1_p, TypeFrais1_eu, TypeFrais2_p, TypeFrais2_eu, TypeFrais3_p, TypeFrais3_eu, 
                                         ModeleUtilise):
    
    requete =  """
                        INSERT INTO fraisexpost.tfournisseur_atlandvoisin (Civilite, Nom, Prenom, NomProduit, TypeFrais1_p, TypeFrais1_eu, TypeFrais2_p, TypeFrais2_eu, 
                        TypeFrais3_p, TypeFrais3_eu, ModeleUtilise)  
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                    """ 
    valeurs = (Civilite, Nom, Prenom, NomProduit, TypeFrais1_p, TypeFrais1_eu, TypeFrais2_p, TypeFrais2_eu, TypeFrais3_p, TypeFrais3_eu, ModeleUtilise)

    setter_data_fournisseurs(requete, valeurs)


# CORUM 
def setter_data_fournisseur_corum(Civilite, Nom, Prenom, NomProduit, TypeFrais1_p, TypeFrais1_eu, TypeFrais2_p, TypeFrais2_eu, TypeFrais3_p, TypeFrais3_eu, 
                                         ModeleUtilise):
    
    requete =  """
                        INSERT INTO fraisexpost.tfournisseur_Corum (Civilite, Nom, Prenom, NomProduit, TypeFrais1_p, TypeFrais1_eu, TypeFrais2_p, TypeFrais2_eu, 
                        TypeFrais3_p, TypeFrais3_eu, ModeleUtilise)  
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                    """ 
    valeurs = (Civilite, Nom, Prenom, NomProduit, TypeFrais1_p, TypeFrais1_eu, TypeFrais2_p, TypeFrais2_eu, TypeFrais3_p, TypeFrais3_eu, ModeleUtilise)

    setter_data_fournisseurs(requete, valeurs)


# URBAN PREMIUM 
def setter_data_fournisseur_urbanpremium(Civilite, Nom, Prenom, NumCompte, IntituleProduit, DateSouscription, TypeFrais1_percent, TypeFrais1_euros, 
                                                 TypeFrais2_percent, TypeFrais2_euros, TypeFrais3_percent, TypeFrais3_euros, ModeleUtilise):
    
    requete =  """
                        INSERT INTO fraisexpost.tfournisseur_UrbanPremium (Civilite, Nom, Prenom, NumeroCompte, NomProduit, DateSouscription, TypeFrais1_p, 
                            TypeFrais1_eu, TypeFrais2_p, TypeFrais2_eu, TypeFrais3_p, TypeFrais3_eu, ModeleUtilise)  
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                    """ 
    valeurs = (Civilite, Nom, Prenom, NumCompte, IntituleProduit, DateSouscription, TypeFrais1_percent, TypeFrais1_euros, TypeFrais2_percent, TypeFrais2_euros, 
               TypeFrais3_percent, TypeFrais3_euros, ModeleUtilise)

    setter_data_fournisseurs(requete, valeurs)


# Theoreim
def setter_data_fournisseur_theoreim(Civilite, Nom, Prenom, NumCompte, IntituleProduit, TypeFrais1_percent, TypeFrais1_euros, TypeFrais2_percent, TypeFrais2_euros, 
                                     TypeFrais3_percent, TypeFrais3_euros, ModeleUtilise):
    
    requete =  """
                        INSERT INTO fraisexpost.tfournisseur_Theoreim (Civilite, Nom, Prenom, NumeroCompte, NomProduit, TypeFrais1_p, 
                            TypeFrais1_eu, TypeFrais2_p, TypeFrais2_eu, TypeFrais3_p, TypeFrais3_eu, ModeleUtilise)  
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) 
                    """ 
    valeurs = (Civilite, Nom, Prenom, NumCompte, IntituleProduit, TypeFrais1_percent, TypeFrais1_euros, TypeFrais2_percent, TypeFrais2_euros, 
               TypeFrais3_percent, TypeFrais3_euros, ModeleUtilise)

    setter_data_fournisseurs(requete, valeurs)


# Smalt Capital
def setter_data_fournisseur_smaltcapital(IntituleProduit, TypeFrais1_percent, TypeFrais2_percent,TypeFrais3_percent, ModeleUtilise):
    
    requete =  """
                        INSERT INTO fraisexpost.tfournisseur_SmaltCapital (NomProduit, TypeFrais1_p, TypeFrais2_p, TypeFrais3_p, ModeleUtilise)  
                        VALUES (%s,%s,%s,%s,%s) 
                    """ 
    valeurs = (IntituleProduit, TypeFrais1_percent, TypeFrais2_percent, TypeFrais3_percent, ModeleUtilise)

    setter_data_fournisseurs(requete, valeurs)


# Keys
def setter_data_fournisseur_keys(IntituleProduit, TypeFrais1_percent, TypeFrais2_percent,TypeFrais3_percent, ModeleUtilise):
    
    requete =  """
                        INSERT INTO fraisexpost.tfournisseur_Keys (NomProduit, TypeFrais1_p, TypeFrais2_p, TypeFrais3_p, ModeleUtilise)  
                        VALUES (%s,%s,%s,%s,%s) 
                    """ 
    valeurs = (IntituleProduit, TypeFrais1_percent, TypeFrais2_percent, TypeFrais3_percent, ModeleUtilise)

    setter_data_fournisseurs(requete, valeurs)


# Eiffel
def setter_data_fournisseur_eiffel(IntituleProduit, TypeFrais1_percent, TypeFrais2_percent,TypeFrais3_percent, ModeleUtilise):
    
    requete =  """
                        INSERT INTO fraisexpost.tfournisseur_Eiffel (NomProduit, TypeFrais1_p, TypeFrais2_p, TypeFrais3_p, ModeleUtilise)  
                        VALUES (%s,%s,%s,%s,%s) 
                    """ 
    valeurs = (IntituleProduit, TypeFrais1_percent, TypeFrais2_percent, TypeFrais3_percent, ModeleUtilise)

    setter_data_fournisseurs(requete, valeurs)


# Norma Capital
def setter_data_fournisseur_norma(Prenom, Nom, TypeFrais1_eu, TypeFrais2_eu,TypeFrais3_eu, MontantTotalSouscritAnneeCourante, ModeleUtilise):
    
    requete =  """
                        INSERT INTO fraisexpost.tfournisseur_normacapital (Prenom, Nom, TypeFrais1_eu, TypeFrais2_eu, TypeFrais3_eu, MontantTotalSouscritAnneeCourante, ModeleUtilise)  
                        VALUES (%s,%s,%s,%s,%s,%s,%s) 
                    """ 
    valeurs = (Prenom, Nom, TypeFrais1_eu, TypeFrais2_eu,TypeFrais3_eu, MontantTotalSouscritAnneeCourante, ModeleUtilise)

    setter_data_fournisseurs(requete, valeurs)


# La Française
def setter_data_fournisseur_lafrancaise(IntituleProduit, TypeFrais1_percent, TypeFrais2_percent,TypeFrais3_percent, ModeleUtilise):
    
    requete =  """
                        INSERT INTO fraisexpost.tfournisseur_lafrancaise (NomProduit, TypeFrais1_p, TypeFrais2_p, TypeFrais3_p, ModeleUtilise)  
                        VALUES (%s,%s,%s,%s,%s) 
                    """ 
    valeurs = (IntituleProduit, TypeFrais1_percent, TypeFrais2_percent, TypeFrais3_percent, ModeleUtilise)

    setter_data_fournisseurs(requete, valeurs)


# 123IM
def setter_data_fournisseur_123IM(IntituleProduit, TypeFrais1_percent, TypeFrais2_percent,TypeFrais3_percent, ModeleUtilise):
    
    requete =  """
                        INSERT INTO fraisexpost.tfournisseur_123im (NomProduit, TypeFrais1_p, TypeFrais2_p, TypeFrais3_p, ModeleUtilise)  
                        VALUES (%s,%s,%s,%s,%s) 
                    """ 
    valeurs = (IntituleProduit, TypeFrais1_percent, TypeFrais2_percent, TypeFrais3_percent, ModeleUtilise)

    setter_data_fournisseurs(requete, valeurs)


# Alpheys 
def setter_data_fournisseur_alpheys(Civilite_recu=None, NumeroCompte_recu=None, Nom_recu=None, Prenom_recu=None, NomProduit_recu=None, DateSouscription_recu=None, 
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
                        INSERT INTO tfournisseur_alpheys (Civilite, Nom, Prenom, NumeroCompte, NomProduit, DateSouscription, TypeFrais1_p, TypeFrais1_eu, TypeFrais2_p, TypeFrais2_eu, 
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

            
# Vatel
def setter_data_fournisseur_vatel(Civilite, Prenom, Nom, IntituleProduit, DateOuverture, TypeFrais2_eu, MontantTotalSouscritAnneeCourante, ModeleUtilise):
    
    requete =  """
                        INSERT INTO fraisexpost.tfournisseur_vatel (Civilite, Prenom, Nom, NomProduit, DateSouscription, TypeFrais2_eu, MontantTotalSouscritAnneeCourante, ModeleUtilise)  
                        VALUES (%s,%s,%s,%s,%s,%s,%s,%s) 
                    """ 
    valeurs = (Civilite, Prenom, Nom, IntituleProduit, DateOuverture, TypeFrais2_eu, MontantTotalSouscritAnneeCourante, ModeleUtilise)

    setter_data_fournisseurs(requete, valeurs)