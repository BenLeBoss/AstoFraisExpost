from app.BDD.database import get_Database_connection
from mysql.connector import Error


class Partenaire:

    def __init__(self, Partenaire, CritereAssociation, Requete):
        self.Partenaire = Partenaire
        self.CritereAssociation = CritereAssociation
        self.Requete = Requete

    def __del__(self):
        pass


    def Get_Partenaire_Taux(self):

        conn = None
        cursor = None 

        try : 
            conn = get_Database_connection()
            if not conn:
                print('Erreur de connexion à la base de données')
                return None

            cursor = conn.cursor(dictionary=True)

            cursor.execute(self.Requete, (self.CritereAssociation, ))
            dataFournisseur = cursor.fetchall()


            if not dataFournisseur:
                return None
            elif len(dataFournisseur) == 1:
                return dataFournisseur[0]
            else:
                return dataFournisseur
        
            
        except Error as e:
            print("Erreur lors de la récupération de données de la base : " + str(e))
            return None
    
        finally: 
            if cursor :
                cursor.close()
            if conn:
                conn.close()



class Perial:
    def __init__(self, IDFournisseur):
        self.IDFournisseur = IDFournisseur

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                        Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                        from tfournisseur_perial f
                        where f.ID = %s
                    """
        
        Perial = Partenaire("Perial", self.IDFournisseur, requete)
        return Perial.Get_Partenaire_Taux()
    


class FranceValley:
    def __init__(self, IDFournisseur):
        self.IDFournisseur = IDFournisseur

    def __del__(self):
        pass
    
    def Get_Taux_et_NomProduit(self):
        requete = """
                        Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                        from tfournisseur_francevalley f
                        where f.ID = %s
                    """
        
        FranceValley = Partenaire("FranceValley", self.IDFournisseur, requete)
        return FranceValley.Get_Partenaire_Taux()
    

class AtlandVoisin:
    def __init__(self, IDFournisseur):
        self.IDFournisseur = IDFournisseur

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from tfournisseur_atlandvoisin2 f
                    where f.ID = %s
            """
            
        AtlandVoisin = Partenaire("AtlandVoisin", self.IDFournisseur, requete)
        return AtlandVoisin.Get_Partenaire_Taux()
    

class Corum:
    def __init__(self, IDFournisseur):
        self.IDFournisseur = IDFournisseur

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from tfournisseur_corum f
                    where f.ID = %s
            """
            
        Corum = Partenaire("Corum", self.IDFournisseur, requete)
        return Corum.Get_Partenaire_Taux()


class UrbanPremium:
    def __init__(self, IDFournisseur):
        self.IDFournisseur = IDFournisseur

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from tfournisseur_urbanpremium f
                    where f.ID = %s
            """
            
        UrbanPremium = Partenaire("UrbanPremium", self.IDFournisseur, requete)
        return UrbanPremium.Get_Partenaire_Taux()


class Theoreim:
    def __init__(self, IDFournisseur):
        self.IDFournisseur = IDFournisseur

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from tfournisseur_theoreim f
                    where f.ID = %s
            """
            
        Theoreim = Partenaire("Theoreim", self.IDFournisseur, requete)
        return Theoreim.Get_Partenaire_Taux()


class SmaltCapital:
    def __init__(self, IDFournisseur):
        self.IDFournisseur = IDFournisseur

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from tfournisseur_smaltcapital f
                    where f.ID = %s
            """
            
        SmaltCapital = Partenaire("SmaltCapital", self.IDFournisseur, requete)
        return SmaltCapital.Get_Partenaire_Taux()


class Keys:
    def __init__(self, IDFournisseur):
        self.IDFournisseur = IDFournisseur

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from tfournisseur_keys f
                    where f.ID = %s
            """
            
        Keys = Partenaire("Keys", self.IDFournisseur, requete)
        return Keys.Get_Partenaire_Taux()


class Eiffel:
    def __init__(self, IDFournisseur):
        self.IDFournisseur = IDFournisseur

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from tfournisseur_eiffel f
                    where f.ID = %s
            """
            
        Eiffel = Partenaire("Eiffel", self.IDFournisseur, requete)
        return Eiffel.Get_Partenaire_Taux()


class Norma:
    def __init__(self, IDFournisseur):
        self.IDFournisseur = IDFournisseur

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from tfournisseur_normacapital f
                    where f.ID = %s
            """
            
        Norma = Partenaire("Norma", self.IDFournisseur, requete)
        return Norma.Get_Partenaire_Taux()


class Alpheys:
    def __init__(self, IDFournisseur):
        self.IDFournisseur = IDFournisseur

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from tfournisseur_alpheys f
                    where f.ID = %s
            """
            
        Alpheys = Partenaire("Alpheys", self.IDFournisseur, requete)
        return Alpheys.Get_Partenaire_Taux()


class Vatel:
    def __init__(self, IDFournisseur):
        self.IDFournisseur = IDFournisseur

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from tfournisseur_vatel f
                    where f.ID = %s
            """
            
        Vatel = Partenaire("Vatel", self.IDFournisseur, requete)
        return Vatel.Get_Partenaire_Taux()


class Sofidy:
    def __init__(self, IDFournisseur):
        self.IDFournisseur = IDFournisseur

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from tfournisseur_sofidy f
                    where f.ID = %s
            """
            
        Sofidy = Partenaire("Sofidy", self.IDFournisseur, requete)
        return Sofidy.Get_Partenaire_Taux()


class Paref:
    def __init__(self, IDFournisseur):
        self.IDFournisseur = IDFournisseur

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from tfournisseur_paref f
                    where f.ID = %s
            """
            
        Paref = Partenaire("Paref", self.IDFournisseur, requete)
        return Paref.Get_Partenaire_Taux()


class Primonial:
    def __init__(self, IDFournisseur):
        self.IDFournisseur = IDFournisseur

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from tfournisseur_primonial f
                    where f.ID = %s
            """
            
        Primonial = Partenaire("Primonial", self.IDFournisseur, requete)
        return Primonial.Get_Partenaire_Taux()


class LaFrancaise:
    def __init__(self, IDFournisseur):
        self.IDFournisseur = IDFournisseur

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from tfournisseur_lafrancaise f
                    where f.ID = %s
            """
            
        LaFrancaise = Partenaire("LaFrancaise", self.IDFournisseur, requete)
        return LaFrancaise.Get_Partenaire_Taux()

    