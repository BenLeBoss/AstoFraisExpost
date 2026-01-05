from app.BDD.database import get_Database_connection
from mysql.connector import Error


class Entite:

    def __init__(self, Entite, CritereAssociation, Requete):
        self.Entite = Entite
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


class Fipagest:
    def __init__(self, IDEntite, Partenaire):
        self.IDEntite = IDEntite
        self.Partenaire = Partenaire
        self.Table_Partenaire = {
            '123IM' : '',
            'ALPHEYS' : 'tfournisseur_alpheys',
            'EIFFEL INVESTMENT GROUP' : 'tfournisseur_eiffel',
            'LA FRANCAISE AM' : 'tfournisseur_lafrancaise',
            'PRIMONIAL' : 'tfournisseur_primonial',
            'XERYSINVEST' : '',
        }

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):

        TablePartenaire = self.Table_Partenaire[self.Partenaire]
        requete = f"""
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from {TablePartenaire} f
                    where f.ID = %s
            """
            
        Fipagest = Entite("Fipagest", self.IDEntite, requete)
        return Fipagest.Get_Partenaire_Taux()


class WatsonPatrimoine:
    def __init__(self, IDEntite):
        self.IDEntite = IDEntite

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from tfournisseur_insinia_watsonall f
                    where f.ID = %s
            """
            
        Watson = Entite("Watson", self.IDEntite, requete)
        return Watson.Get_Partenaire_Taux()


class Synergie:
    def __init__(self, IDEntite):
        self.IDEntite = IDEntite

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from tfournisseur_insinia_synergieconseilspatrimoineall f
                    where f.ID = %s
            """
            
        Synergie = Entite("Synergie", self.IDEntite, requete)
        return Synergie.Get_Partenaire_Taux()


class FamilyPatrimoine:
    def __init__(self, IDEntite):
        self.IDEntite = IDEntite

    def __del__(self):
        pass

    # Récupération des taux et de l'intitulé du produit avec le numéro de compte
    def Get_Taux_et_NomProduit(self):
        requete = """
                    Select f.TypeFrais1_p, f.TypeFrais1_eu, f.TypeFrais2_p, f.TypeFrais2_eu, f.TypeFrais3_p, f.TypeFrais3_eu, f.TauxFraisTransaction, 
                            f.MontantFraisTransaction, f.NomProduit, f.MontantTotalSouscritAnneeCourante, f.MontantTotalSouscrit, f.ModeleUtilise
                    from tfournisseur_insinia_familypatrimoineall f
                    where f.ID = %s
            """
            
        Family = Entite("Family", self.IDEntite, requete)
        return Family.Get_Partenaire_Taux()

    



    