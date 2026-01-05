import pymupdf 
import io
from pathlib import Path
from datetime import datetime

from app.routes.partenaire.Classe_Partenaire import Perial, FranceValley, AtlandVoisin, Corum, UrbanPremium, Theoreim, SmaltCapital, Keys, Eiffel, Norma, Alpheys, Vatel, Sofidy, Paref, Primonial, LaFrancaise
from app.routes.partenaire.Classe_EntiteInsinia import Fipagest, WatsonPatrimoine, Synergie, FamilyPatrimoine
from app.routes.partenaire.Classe_FraisEntree import FraisEntree


class Fiche_Reporting:

    doc = ''
    BASE_DIR = ''
    PDF_PATH = ''

    VilleBureau = {
        "fipagest": "Reims",
        "spi conseil": "Boulogne-Billancourt",
        "equatio finances": "Lille",
        "cv finance": "Voiron",
        "astoria courtage est": "Mulhouse",
        "acp": "Paris",
        "equipe 4": "Paris",
        "equipe 3": "Paris",
        "equipe 2": "Paris",
        "equipe 1": "Paris"
    }

    VilleEntite = {
        "ACTIONPATRIMOINE" : "Issy-les-Moulineaux",
        "ALLUREFINANCE" : "Paris",
        "BCFINANCES" : "Bourg-en-Bresse",
        "CAPIUM": "Lyon",
        "FAMILYPATRIMOINE": "Meylan",
        "FIPAGEST": "Reims",
        "MYFAMILYOFFICER": "Lyon",
        "PARISII": "Paris",
        "SOLVEPATRIMOINE": "Grésy-sur-Aix",
        "SYNERGIECONSEILSPATRIMOINE": "Villeneuve-Loubet",
        "WATSONPATRIMOINE": "La Rochelle"
    }

    
    # Constructeur
    def __init__(self, Groupe, Entite, Partenaire, Nom, Prenom, NumeroCompte, Entreprise, Agence, Conseiller, ProduitIntitule, ProduitEtablissementFournisseur, ClientProduitDateOuverture, ClientProduitNumCompte, Produit, 
                 Compte_31_12, FaitA, DateSignature, Signature, IDFournisseur):  
        
        self.Groupe = Groupe
        self.Entite = Entite
        self.Partenaire = Partenaire
        self.Nom = Nom 
        self.Prenom = Prenom 
        self.NumeroCompte = NumeroCompte 
        self.Entreprise = Entreprise 
        self.Conseiller = Conseiller 
        self.Agence = self.ReformaterDonnées(Agence , "Bureau")
        self.ProduitIntitule = ProduitIntitule 
        self.ProduitEtablissementFournisseur = ProduitEtablissementFournisseur 
        self.ClientProduitDateOuverture = ClientProduitDateOuverture 
        self.ClientProduitNumCompte = ClientProduitNumCompte 
        self.Produit_FichierClient = Produit 
        self.Produit_FichierFournisseur = '' 
        self.Compte_31_12 = Compte_31_12 
        self.FaitA = self.ReformaterDonnées(FaitA, "FaitA")
        self.DateSignature = DateSignature 
        self.Signature = Signature 
        self.IDFournisseur = IDFournisseur

        self.Chemin_Logo = ''
        self.Taille_Logo = 0
        self.PhraseContrat = ''
        self.PhraseDateOuverture = ''
        self.PhraseCompte31_12 = ''
        self.ModeleDeDonneesUtilisee = ''

        # Dictionnaire de données contenant les coordonnées des placeholders trouvés dans le fichier pdf patron
        self.Coords_Fiche = {
            "Logo" : '',
            "Nom" : '',
            "Prenom" : '',
            "Entreprise" : '',
            "Agence" : '',
            "Conseiller" : '',
            "DateOuverture" : '',
            "Contrat" : '',
            "Produit" : '',
            "Compte_31_12" : '',
            "FaitA" : '',
            "DateSignature" : '',
            "Signature" : '',
            "MentionsLegales" : '',
            "Frais_pourcent": {
                "Poucentage_1" : '',
                "Poucentage_2" : '',
                "Poucentage_3" : '',
                "Poucentage_4" : '',
                "Poucentage_5" : '',
                "Poucentage_6" : '',
                "Poucentage_7" : '',
                "Poucentage_8" : '',
                "Poucentage_9" : '',
                "Poucentage_10" : '',
                "Poucentage_11" : '',
                "Poucentage_12" : '',
                "Poucentage_13" : ''
            },
            "Frais_euros": {
                "Montant_1" : '',
                "Montant_2" : '',
                "Montant_3" : '',
                "Montant_4" : '',
                "Montant_5" : '',
                "Montant_6" : '',
                "Montant_7" : '',
                "Montant_8" : '',
                "Montant_9" : '',
                "Montant_10" : '',
                "Montant_11" : '',
                "Montant_12" : '',
                "Montant_13" : ''
            }
        }
        

    # Destructeur
    def __del__(self):
        print(f"Classe fermée !")
        if hasattr(self, "doc"):
            self.doc.close()
    

    # Process de création de fiche de reporting client
    def Processus(self):
        
        self.Initialiser_doc()
        self.Analyser_pdf()
        #self.Afficher_Coordonnées()
        self.MiseEnFormeTexte()
        self.Inserer_Contenu_Client()
        return self.Sauver_dans_Buffer()






    # Récupération patron 
    def Initialiser_doc(self):
        self.BASE_DIR = Path(__file__).resolve().parents[2]  # 2 niveaux au-dessus de ce fichier
        self.PDF_PATH = self.BASE_DIR / 'medias' / 'pdf' / 'Patron_fiche_de_reporting_modifie_placeholders.pdf'
        self.doc = pymupdf.open(self.PDF_PATH)


#-----------------------------------------------------------MISE EN FORME DE DONNEES-----------------------------------------------------------

    def Transformation_Montant(self):
        tempCompte_31_12 = self.Compte_31_12
        if " " in tempCompte_31_12:
            tempCompte_31_12 = float(tempCompte_31_12.replace(" ", ""))
            tempCompte_31_12 = round(tempCompte_31_12, 2)
        else:
            tempCompte_31_12 = round(float(self.Compte_31_12), 2)

        return tempCompte_31_12
    

    def MiseEnFormeTexte(self):
        if any(x is None for x in [self.ProduitIntitule, self.ProduitEtablissementFournisseur, self.ClientProduitDateOuverture, self.ClientProduitNumCompte, self.Compte_31_12]):
            self.PhraseContrat = ""
            self.PhraseDateOuverture = ""
            self.PhraseCompte31_12 = ""
            
            if self.ProduitIntitule is not None:
                self.PhraseContrat += self.ProduitIntitule
            if self.ProduitEtablissementFournisseur is not None:
                self.PhraseContrat += f" de {self.ProduitEtablissementFournisseur}"
            if self.ClientProduitDateOuverture is not None:
                self.PhraseDateOuverture += f" le {self.ClientProduitDateOuverture}"
            if self.ClientProduitNumCompte is not None:
                self.PhraseDateOuverture += f" sous le n° de compte {self.ClientProduitNumCompte}"
            if self.Compte_31_12 is not None:
                self.PhraseCompte31_12 = f"31/12/2024, la valeur globale de votre investissement est de : {self.Compte_31_12} Euros"

        else:
            self.PhraseContrat = f"{self.ProduitIntitule} de {self.ProduitEtablissementFournisseur}"
            self.PhraseDateOuverture = f" le {self.ClientProduitDateOuverture} sous le n° de compte {self.ClientProduitNumCompte}"
            self.PhraseCompte31_12 = f"31/12/2024, la valeur globale de votre investissement est de : {self.Compte_31_12} Euros"


    # Si le montant total du compte au 01/01 et au 31/12 sont égaux à 0 dans le fichier client Astoria, 
    # on utilise le montant total s'il y en a un qui existe dans le fichier EMT correspondant
    def MiseEnFormeMontant(self, MontantTotalSouscritFournisseur):
        if (MontantTotalSouscritFournisseur != 0):
            """
            tempCompte_31_12 = self.Compte_31_12
            if " " in tempCompte_31_12:
                tempCompte_31_12 = float(tempCompte_31_12.replace(" ", ""))
                tempCompte_31_12 = round(tempCompte_31_12, 2)
            else:
                tempCompte_31_12 = round(float(self.Compte_31_12), 2)

            if (tempCompte_31_12 == 0):
            """  
            tempValeurCompte = f"{MontantTotalSouscritFournisseur:,.2f}".replace(",", " ")
            self.PhraseCompte31_12 = f"31/12/2024, la valeur globale de votre investissement est de : {tempValeurCompte} Euros"


    # Calcul le montant au 31/12 disponible sur le compte du client (après y avoir appliqué les taux)
    def CalculCompte31_12_AvecTaux(self, MontantTotalSouscritAnneeCourante, TauxFraisTransaction, TauxFraisEntree):
        tempYear = str(datetime.now().year - 1)

        if self.ClientProduitDateOuverture :
            if tempYear in self.ClientProduitDateOuverture:
                tempValeurCompte = 0

                tempCompte_31_12 = self.Compte_31_12
                if " " in tempCompte_31_12:
                    tempCompte_31_12 = float(tempCompte_31_12.replace(" ", ""))
                    tempCompte_31_12 = round(tempCompte_31_12, 2)
                else:
                    tempCompte_31_12 = round(float(self.Compte_31_12), 2)

                if MontantTotalSouscritAnneeCourante != 0.00:

                    tempMontantTotalSouscritAnneeCourante = 0
                    tempMontantTotalSouscritAnneeCourante = MontantTotalSouscritAnneeCourante
                    tempMontantTotalSouscritAnneeCourante = f"{tempMontantTotalSouscritAnneeCourante:,.2f}".replace(",", " ")
                    tempValeurFrais = MontantTotalSouscritAnneeCourante * ((TauxFraisTransaction + TauxFraisEntree) / 100)
                    tempValeurCompte = f"{(MontantTotalSouscritAnneeCourante - tempValeurFrais):,.2f}".replace(",", " ")
                    self.PhraseDateOuverture += f" pour un montant de {tempMontantTotalSouscritAnneeCourante} Euros"
                    self.PhraseCompte31_12 = f"31/12/2024, la valeur globale de votre investissement est de : {tempValeurCompte} Euros"

                else:
                    
                    tempValeurFrais = tempCompte_31_12 * ((TauxFraisTransaction + TauxFraisEntree) / 100)
                    tempValeurCompte = f"{(tempCompte_31_12 - tempValeurFrais):,.2f}".replace(",", " ")
                    self.PhraseDateOuverture += f" pour un montant de {self.Compte_31_12} Euros"
                    self.PhraseCompte31_12 = f"31/12/2024, la valeur globale de votre investissement est de : {tempValeurCompte} Euros"



    # Calcul les frais en euros à partir des frais en % et du montant total
    # Fichier EMT de type M1
    def Calcul_FraisEuros_Avec_FraisPourcent(self, tab_taux):
        if tab_taux:
            tempCompte_31_12 = self.Transformation_Montant()

            if tab_taux["TypeFrais1_p"] > 0 and tab_taux["TypeFrais1_eu"] == 0:
                tab_taux["TypeFrais1_eu"] = (tempCompte_31_12 * tab_taux["TypeFrais1_p"]) / 100
            if tab_taux["TypeFrais2_p"] > 0 and tab_taux["TypeFrais2_eu"] == 0:
                tab_taux["TypeFrais2_eu"] = (tempCompte_31_12 * tab_taux["TypeFrais2_p"]) / 100
            if tab_taux["TypeFrais3_p"] > 0 and tab_taux["TypeFrais3_eu"] == 0:
                tab_taux["TypeFrais3_eu"] = (tempCompte_31_12 * tab_taux["TypeFrais3_p"]) / 100

            return tab_taux


    # Calcul les frais en % à partir des frais en euros et du montant total
    # Fichier EMT de type M6
    def Calcul_FraisPourcent_Avec_FraisEuros(self, tab_taux):
        if tab_taux:
            tempCompte_31_12 = self.Transformation_Montant()

            if tab_taux["TypeFrais1_eu"] > 0 and tab_taux["TypeFrais1_p"] == 0:
                tab_taux["TypeFrais1_p"] = (tab_taux["TypeFrais1_eu"] * 100) / tempCompte_31_12
            if tab_taux["TypeFrais2_eu"] > 0 and tab_taux["TypeFrais2_p"] == 0:
                tab_taux["TypeFrais2_p"] = (tab_taux["TypeFrais2_eu"] * 100) / tempCompte_31_12
            if tab_taux["TypeFrais3_eu"] > 0 and tab_taux["TypeFrais3_p"] == 0:
                tab_taux["TypeFrais3_p"] = (tab_taux["TypeFrais3_eu"] * 100) / tempCompte_31_12

            return tab_taux



#-----------------------------------------------------------COORDONNEES-----------------------------------------------------------

    # Parcourt le fichier et découpe le fichier
    def Analyser_pdf(self):
        for pageComplete in self.doc:
            texteComplet = pageComplete.get_text()
            """
            print(texteComplet)

        print("\n\n")
        """
            
        #parcourt chaque page du pdf
        for page in self.doc:

            #récupère le contenu de la page sous forme de dictionnaire
            page_text_dict = page.get_text("dict")

            #parcourt tout les blocs de texte de la page
            for bloc in page_text_dict["blocks"]:

                #si le bloc contient du texte
                if "lines" in bloc:

                    #coordonnées du bounding bloc
                    bloc_coordonnees = bloc["bbox"]
                    """
                    print(f"Bloc de texte trouvé aux coordonnées : {bloc_coordonnees}")
                    """

                    #parcourt toutes les lignes du bloc
                    for ligne in bloc["lines"]:

                        #parcourt chaque morceaux de texte de la ligne
                        for index, morceau_texte in enumerate(ligne["spans"]):
                            texte = morceau_texte["text"] 
                            coordonnees_texte = morceau_texte["bbox"]
                            

                            self.get_Coords(texte, coordonnees_texte)

                            """
                            print(f"span text: «{texte}» | bbox: {coordonnees_texte}")

                            # Vérifie si c'est le dernier élément de la ligne
                            EstDernier = (index == len(ligne["spans"]) - 1)

                            if EstDernier: 
                                print(f"-> Texte : « {texte} » à {coordonnees_texte}\n")
                            else:
                                print(f"-> Texte : « {texte} » à {coordonnees_texte}")
                            """

        self.Detecter_Mentions_Legales()


        
    # Récupère les coordonnées des placeholders présent dans le PDF
    def get_Coords(self, texte, coordonnees_texte):
        texte = texte.strip()


        if '{{LOGO}}' in texte :
            self.Coords_Fiche["Logo"] = coordonnees_texte
        if '{{NOM}}' in texte :
            self.Coords_Fiche["Nom"] = coordonnees_texte
        if '{{PRENOM}}' in texte :
            self.Coords_Fiche["Prenom"] = coordonnees_texte
        if '{{ENTREPRISE}}' in texte :
            self.Coords_Fiche["Entreprise"] = coordonnees_texte
        if '{{AGENCE}}' in texte :
            self.Coords_Fiche["Agence"] = coordonnees_texte
        if '{{CONSEILLER}}' in texte :
            self.Coords_Fiche["Conseiller"] = coordonnees_texte
        if '{{CONTRAT}}' in texte :
            self.Coords_Fiche["Contrat"] = coordonnees_texte
        if '{{DATEOUVERTURE}}' in texte :
            self.Coords_Fiche["DateOuverture"] = coordonnees_texte
        if '{{PRODUIT}}' in texte :
            self.Coords_Fiche["Produit"] = coordonnees_texte
        if '{{COMPTE_31_12}}' in texte :
            self.Coords_Fiche["Compte_31_12"] = coordonnees_texte
        if '{{FAITA}}' in texte :
            self.Coords_Fiche["FaitA"] = coordonnees_texte
        if '{{DATEA}}' in texte :
            self.Coords_Fiche["DateSignature"] = coordonnees_texte
        if '{{SIGNATURE}}' in texte :
            self.Coords_Fiche["Signature"] = coordonnees_texte
        if '{{p01}}' in texte :
            self.Coords_Fiche["Frais_pourcent"]["Poucentage_1"] = coordonnees_texte
        if '{{p02}}' in texte :
            self.Coords_Fiche["Frais_pourcent"]["Poucentage_2"] = coordonnees_texte
        if '{{p03}}' in texte :
            self.Coords_Fiche["Frais_pourcent"]["Poucentage_3"] = coordonnees_texte
        if '{{p04}}' in texte :
            self.Coords_Fiche["Frais_pourcent"]["Poucentage_4"] = coordonnees_texte
        if '{{p05}}' in texte :
            self.Coords_Fiche["Frais_pourcent"]["Poucentage_5"] = coordonnees_texte
        if '{{p06}}' in texte :
            self.Coords_Fiche["Frais_pourcent"]["Poucentage_6"] = coordonnees_texte
        if '{{p07}}' in texte :
            self.Coords_Fiche["Frais_pourcent"]["Poucentage_7"] = coordonnees_texte
        if '{{p08}}' in texte :
            self.Coords_Fiche["Frais_pourcent"]["Poucentage_8"] = coordonnees_texte
        if '{{p09}}' in texte :
            self.Coords_Fiche["Frais_pourcent"]["Poucentage_9"] = coordonnees_texte
        if '{{p10}}' in texte :
            self.Coords_Fiche["Frais_pourcent"]["Poucentage_10"] = coordonnees_texte
        if '{{p11}}' in texte :
            self.Coords_Fiche["Frais_pourcent"]["Poucentage_11"] = coordonnees_texte
        if '{{p12}}' in texte :
            self.Coords_Fiche["Frais_pourcent"]["Poucentage_12"] = coordonnees_texte
        if '{{p13}}' in texte :
            self.Coords_Fiche["Frais_pourcent"]["Poucentage_13"] = coordonnees_texte
        if '{{c01}}' in texte :
            self.Coords_Fiche["Frais_euros"]["Montant_1"] = coordonnees_texte
        if '{{c02}}' in texte :
            self.Coords_Fiche["Frais_euros"]["Montant_2"] = coordonnees_texte
        if '{{c03}}' in texte :
            self.Coords_Fiche["Frais_euros"]["Montant_3"] = coordonnees_texte
        if '{{c04}}' in texte :
            self.Coords_Fiche["Frais_euros"]["Montant_4"] = coordonnees_texte
        if '{{c05}}' in texte :
            self.Coords_Fiche["Frais_euros"]["Montant_5"] = coordonnees_texte
        if '{{c06}}' in texte :
            self.Coords_Fiche["Frais_euros"]["Montant_6"] = coordonnees_texte
        if '{{c07}}' in texte :
            self.Coords_Fiche["Frais_euros"]["Montant_7"] = coordonnees_texte
        if '{{c08}}' in texte :
            self.Coords_Fiche["Frais_euros"]["Montant_8"] = coordonnees_texte
        if '{{c09}}' in texte :
            self.Coords_Fiche["Frais_euros"]["Montant_9"] = coordonnees_texte
        if '{{c10}}' in texte :
            self.Coords_Fiche["Frais_euros"]["Montant_10"] = coordonnees_texte
        if '{{c11}}' in texte :
            self.Coords_Fiche["Frais_euros"]["Montant_11"] = coordonnees_texte
        if '{{c12}}' in texte :
            self.Coords_Fiche["Frais_euros"]["Montant_12"] = coordonnees_texte
        if '{{c13}}' in texte :
            self.Coords_Fiche["Frais_euros"]["Montant_13"] = coordonnees_texte


    def Detecter_Mentions_Legales(self):

        if self.Groupe == 'INSINIA':
            debut = "ASTORIA FINANCE 5-7 rue de Monttessuy 75340 Paris"
            fin = "compagnie MMA sise 160 Rue Henri Champion – 72030 Le Mans Cedex 9."

            first_bbox = None
            last_bbox = None
            capture = False

            # On scanne la dernière page du pdf pour trouver les coords des mentions légales
            page = self.doc[-1]
            page_dict = page.get_text("dict")

            for bloc in page_dict["blocks"]:

                if "lines" not in bloc:
                    continue

                for ligne in bloc["lines"]:
                    for span in ligne["spans"]:

                        texte = span["text"].strip()
                        bbox  = span["bbox"]

                        # Début du bloc
                        if texte.startswith(debut):
                            capture = True
                            first_bbox = bbox
                            last_bbox = bbox
                            continue

                        # Capturer tant que le bloc n’est pas fini
                        if capture:
                            last_bbox = bbox

                            # Ligne finale détectée
                            if fin in texte:
                                capture = False

                                # Fusion du rectangle final
                                x0 = first_bbox[0] 
                                y0 = first_bbox[1] - 10
                                x1 = last_bbox[2] + 20
                                y1 = last_bbox[3] + 10

                                self.Coords_Fiche["MentionsLegales"] = (x0, y0, x1, y1)


    # Affichage du dictionnaire de données 
    def Afficher_Coordonnées(self):
        print("self.Coords_Fiche = {")
        for cle, valeur in self.Coords_Fiche.items():
            print(f'    "{cle}" : {repr(valeur)},')
        print("}")


#-----------------------------------------------------------INSERTION-----------------------------------------------------------


    # Insertion des infos clients dans la fiche de reporting
    def Inserer_Contenu_Client(self):

        # Insère les taux correspondants
        self.get_Taux_from_Class_2()


        # Insère les infos principales
        self.Inserer_Contenu_Coords(1, self.Coords_Fiche["Nom"], self.Nom, False, "")
        self.Inserer_Contenu_Coords(1, self.Coords_Fiche["Prenom"], self.Prenom, False, "")
        self.Inserer_Contenu_Coords(1, self.Coords_Fiche["Entreprise"], self.Entreprise, False, "")
        self.Inserer_Contenu_Coords(1, self.Coords_Fiche["Agence"], self.Agence, True, "")
        self.Inserer_Contenu_Coords(1, self.Coords_Fiche["Conseiller"], self.Conseiller, False, "")
        self.Inserer_Contenu_Coords(1, self.Coords_Fiche["Contrat"], self.PhraseContrat, True, "")
        self.Inserer_Contenu_Coords(1, self.Coords_Fiche["DateOuverture"], self.PhraseDateOuverture, True, "")
        self.Inserer_Contenu_Coords(1, self.Coords_Fiche["Compte_31_12"], self.PhraseCompte31_12, False, "")
        self.Inserer_Contenu_Coords(2, self.Coords_Fiche["FaitA"], self.FaitA, False, "")
        self.Inserer_Contenu_Coords(2, self.Coords_Fiche["DateSignature"], self.DateSignature, False, "")
        
        # si c'est une entité INSINIA, on change les mentions légales, sinon on laisse tel quel
        if self.Groupe == 'INSINIA':
            self.Inserer_Contenu_Coords(2, self.Coords_Fiche["MentionsLegales"], self.Normaliser_texte_pdf(self.Definition_Mentions_Legales()), False, "MentionsLegales")


        # Remplit le pdf avec le nom du preoduit renseigné dans le fichier fournisseur, sinon utilise le nom de produit renseigné dans le fichier client
        if (self.Produit_FichierFournisseur != '') and (self.Produit_FichierFournisseur is not None) :
            self.Inserer_Contenu_Coords(1, self.Coords_Fiche["Produit"], self.Produit_FichierFournisseur, True, "Produit")
        else:
            self.Inserer_Contenu_Coords(1, self.Coords_Fiche["Produit"], self.Produit_FichierClient, True, "Produit")

        # Insère les logos
        self.Definition_logo()
        self.Inserer_Contenu_Coords(1, self.Coords_Fiche["Logo"], "", False, "Logo")
        self.Inserer_Contenu_Coords(2, self.Coords_Fiche["Signature"], "", False, "Logo")




    def get_Taux_from_Class_2(self):

        # données principales communes à tous les fournisseurs
        self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_1"], f"{0.00:.3f} %", True)
        self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_2"], " ")
        self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_3"], " ")
        self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_4"], " ")
        self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_5"], " ")
        self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_6"], " ")
        self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_1"], self.format_align(0.00), True)
        self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_2"], " ")
        self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_3"], " ")
        self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_4"], " ")
        self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_5"], " ")
        self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_6"], " ")
        self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_12"], " ")
        self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_12"], " ")


        # récupère les taux en fonction du fournisseur ET de l'entité
        if self.Groupe == 'ASTORIA':
            match(self.Partenaire):
                case "PERIAL ASSET MANAGEMENT":
                    Perial_Instance = Perial(self.IDFournisseur)
                    tab_taux =  Perial_Instance.Get_Taux_et_NomProduit()

                case "FRANCE VALLEY INVESTISSEMENTS":
                    FranceValley_Instance = FranceValley(self.IDFournisseur)
                    tab_taux =  FranceValley_Instance.Get_Taux_et_NomProduit()

                case "ATLAND VOISIN":
                    AtlandVoisin_Instance = AtlandVoisin(self.IDFournisseur)
                    tab_taux =  AtlandVoisin_Instance.Get_Taux_et_NomProduit()

                case "CORUM L'EPARGNE":
                    Corum_Instance = Corum(self.IDFournisseur)
                    tab_taux =  Corum_Instance.Get_Taux_et_NomProduit()

                case "URBAN PREMIUM":
                    UrbanPremium_Instance = UrbanPremium(self.IDFournisseur)
                    tab_taux =  UrbanPremium_Instance.Get_Taux_et_NomProduit()

                case "THEOREIM":
                    Theoreim_Instance = Theoreim(self.IDFournisseur)
                    tab_taux =  Theoreim_Instance.Get_Taux_et_NomProduit()

                case "SMALT CAPITAL":
                    SmaltCapital_Instance = SmaltCapital(self.IDFournisseur)
                    tab_taux =  SmaltCapital_Instance.Get_Taux_et_NomProduit()

                case "KEYSAM":
                    Keys_Instance = Keys(self.IDFournisseur)
                    tab_taux =  Keys_Instance.Get_Taux_et_NomProduit()

                case "EIFFEL INVESTMENT GROUP":
                    Eiffel_Instance = Eiffel(self.IDFournisseur)
                    tab_taux =  Eiffel_Instance.Get_Taux_et_NomProduit()

                case "NORMA CAPITAL":
                    Norma_Instance = Norma(self.IDFournisseur)
                    tab_taux =  Norma_Instance.Get_Taux_et_NomProduit()

                case "ALPHEYS":
                    Alpheys_Instance = Alpheys(self.IDFournisseur)
                    tab_taux =  Alpheys_Instance.Get_Taux_et_NomProduit()

                case "VATELCAPITAL":
                    Vatel_Instance = Vatel(self.IDFournisseur)
                    tab_taux =  Vatel_Instance.Get_Taux_et_NomProduit()

                case "SOFIDY":
                    Sofidy_Instance = Sofidy(self.IDFournisseur)
                    tab_taux =  Sofidy_Instance.Get_Taux_et_NomProduit()

                case "PAREF":
                    Paref_Instance = Paref(self.IDFournisseur)
                    tab_taux =  Paref_Instance.Get_Taux_et_NomProduit()

                case "PRIMONIAL":
                    Primonial_Instance = Primonial(self.IDFournisseur)
                    tab_taux =  Primonial_Instance.Get_Taux_et_NomProduit()

                case "LAFRANCAISEAM":
                    LaFrancaise_Instance = LaFrancaise(self.IDFournisseur)
                    tab_taux =  LaFrancaise_Instance.Get_Taux_et_NomProduit()

                case _:
                    print("Aucun partenaire ne match")

        elif self.Groupe == 'INSINIA':
            match(self.Entite):
                case "ACTIONPATRIMOINE":
                    print("TODO ENTITE")

                case "ALLUREFINANCE":
                    print("TODO ENTITE")

                case "BCFINANCES":
                    print("TODO ENTITE")

                case "CAPIUM":
                    print("TODO ENTITE")

                case "FAMILYPATRIMOINE":
                    FamilyPatrimoine_Instance = FamilyPatrimoine(self.IDFournisseur)
                    tab_taux =  FamilyPatrimoine_Instance.Get_Taux_et_NomProduit()

                case "FIPAGEST":
                    Fipagest_Instance = Fipagest(self.IDFournisseur, self.Partenaire)
                    tab_taux =  Fipagest_Instance.Get_Taux_et_NomProduit()

                case "MYFAMILYOFFICER":
                    print("TODO ENTITE")

                case "PARISII":
                    print("TODO ENTITE")

                case "SOLVEPATRIMOINE":
                    print("TODO ENTITE")

                case "SYNERGIECONSEILSPATRIMOINE":
                    Synergie_Instance = Synergie(self.IDFournisseur)
                    tab_taux =  Synergie_Instance.Get_Taux_et_NomProduit()

                case "WATSONPATRIMOINE":
                    Watson_Instance = WatsonPatrimoine(self.IDFournisseur)
                    tab_taux =  Watson_Instance.Get_Taux_et_NomProduit()

                case _:
                    print("Aucune entité existante ne correspond !")


        if tab_taux:
            if self.ClientProduitDateOuverture is not None:
                if (tab_taux["TauxFraisTransaction"] == 0 or tab_taux["TauxFraisTransaction"] is None) and '2024' in self.ClientProduitDateOuverture:
                    if tab_taux["MontantTotalSouscrit"] != 0:
                        FraisEntree_Instance = FraisEntree(self.Partenaire, tab_taux["MontantTotalSouscrit"], tab_taux["NomProduit"])
                    else:
                        FraisEntree_Instance = FraisEntree(self.Partenaire, self.Compte_31_12, tab_taux["NomProduit"])
                    
                    tempDictionnaire = FraisEntree_Instance.Get_FraisEntree()
                    if tempDictionnaire :
                        tab_taux["TauxFraisTransaction"] = tempDictionnaire["TauxFraisTVAFinal"]
                        tab_taux["MontantFraisTransaction"] = tempDictionnaire["FraisEurosFinal"]
                    else:
                        tab_taux["TauxFraisTransaction"] = 0.00
                        tab_taux["MontantFraisTransaction"] = 0.00


            
            self.ModeleDeDonneesUtilisee = tab_taux["ModeleUtilise"]
            self.MiseEnFormeMontant(tab_taux["MontantTotalSouscrit"])
            self.CalculCompte31_12_AvecTaux(tab_taux["MontantTotalSouscritAnneeCourante"], tab_taux["TauxFraisTransaction"], tab_taux["TypeFrais1_p"])
            self.Produit_FichierFournisseur = tab_taux["NomProduit"]

            
            
            # applique les taux en fonction du modèle de données enregistrés dans la base
            match(self.ModeleDeDonneesUtilisee):

                # SmaltCapital, Keys, Eiffel
                case "M1":
                    self.Calcul_FraisEuros_Avec_FraisPourcent(tab_taux)

                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_7"], f"{tab_taux["TauxFraisTransaction"]:.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_8"], f"{(tab_taux["TypeFrais1_p"] + tab_taux["TypeFrais2_p"] + tab_taux["TypeFrais3_p"]):.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_9"], f"{tab_taux["TypeFrais2_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_10"], f"{tab_taux["TypeFrais1_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_11"], f"{tab_taux["TypeFrais3_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_13"], f"{(tab_taux["TypeFrais1_p"] + tab_taux["TypeFrais2_p"] + tab_taux["TypeFrais3_p"] + tab_taux["TauxFraisTransaction"]):.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_7"], self.format_align(tab_taux["MontantFraisTransaction"]), True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_8"], self.format_align(tab_taux["TypeFrais1_eu"] + tab_taux["TypeFrais2_eu"] + tab_taux["TypeFrais3_eu"]), True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_9"], self.format_align(tab_taux["TypeFrais2_eu"]))            
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_10"], self.format_align(tab_taux["TypeFrais1_eu"]))
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_11"], self.format_align(tab_taux["TypeFrais3_eu"]))
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_13"], self.format_align(tab_taux["TypeFrais1_eu"] + tab_taux["TypeFrais2_eu"] + tab_taux["TypeFrais3_eu"] + tab_taux["MontantFraisTransaction"]), True)


                # Alpheys (Activimmo, Pierval, Altixia, FranceValley, Perial, LaFrançaise, Epargne pierre, Epargne foncière, Sofidy, Sogenial)
                case "M2":
                    self.Calcul_FraisEuros_Avec_FraisPourcent(tab_taux)
                    
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_7"], f"{tab_taux["TauxFraisTransaction"]:.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_8"], f"{(tab_taux["TypeFrais1_p"] + tab_taux["TypeFrais2_p"] + tab_taux["TypeFrais3_p"]):.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_9"], f"{tab_taux["TypeFrais1_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_10"], f"{tab_taux["TypeFrais2_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_11"], f"{tab_taux["TypeFrais3_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_13"], f"{(tab_taux["TypeFrais1_p"] + tab_taux["TypeFrais2_p"] + tab_taux["TypeFrais3_p"] + tab_taux["TauxFraisTransaction"]):.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_7"], self.format_align(tab_taux["MontantFraisTransaction"]), True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_8"], self.format_align(tab_taux["TypeFrais1_eu"] + tab_taux["TypeFrais2_eu"] + tab_taux["TypeFrais3_eu"]), True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_9"], self.format_align(tab_taux["TypeFrais1_eu"]))
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_10"], self.format_align(tab_taux["TypeFrais2_eu"]))
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_11"], self.format_align(tab_taux["TypeFrais3_eu"]))
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_13"], self.format_align(tab_taux["TypeFrais1_eu"] + tab_taux["TypeFrais2_eu"] + tab_taux["TypeFrais3_eu"] + tab_taux["MontantFraisTransaction"]), True)


                # UrbanPremium, Sofidy
                case "M3":
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_7"], f"{tab_taux["TauxFraisTransaction"]:.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_8"], f"{(tab_taux["TypeFrais1_p"] + tab_taux["TypeFrais2_p"] + tab_taux["TypeFrais3_p"]):.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_9"], f"{tab_taux["TypeFrais2_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_10"], f"{tab_taux["TypeFrais1_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_11"], f"{tab_taux["TypeFrais3_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_13"], f"{(tab_taux["TypeFrais1_p"] + tab_taux["TypeFrais2_p"] + tab_taux["TypeFrais3_p"] + tab_taux["TauxFraisTransaction"]):.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_7"], self.format_align(tab_taux["MontantFraisTransaction"]), True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_8"], self.format_align(tab_taux["TypeFrais1_eu"] + tab_taux["TypeFrais2_eu"] + tab_taux["TypeFrais3_eu"]), True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_9"], self.format_align(tab_taux["TypeFrais2_eu"]))
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_10"], self.format_align(tab_taux["TypeFrais1_eu"]))
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_11"], self.format_align(tab_taux["TypeFrais3_eu"]))
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_13"], self.format_align(tab_taux["TypeFrais1_eu"] + tab_taux["TypeFrais2_eu"] + tab_taux["TypeFrais3_eu"] + tab_taux["MontantFraisTransaction"]), True)


                # Perial, Atland, Corum, Theoreim
                case "M4":
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_7"], f"{tab_taux["TauxFraisTransaction"]:.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_8"], f"{(tab_taux["TypeFrais1_p"] + tab_taux["TypeFrais2_p"] + tab_taux["TypeFrais3_p"]):.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_9"], f"{tab_taux["TypeFrais2_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_10"], f"{tab_taux["TypeFrais1_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_11"], f"{tab_taux["TypeFrais3_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_13"], f"{(tab_taux["TypeFrais1_p"] + tab_taux["TypeFrais2_p"] + tab_taux["TypeFrais3_p"] + tab_taux["TauxFraisTransaction"]):.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_7"], self.format_align(tab_taux["MontantFraisTransaction"]), True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_8"], self.format_align(tab_taux["TypeFrais1_eu"] + tab_taux["TypeFrais2_eu"] + tab_taux["TypeFrais3_eu"]), True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_9"], self.format_align(tab_taux["TypeFrais2_eu"]))
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_10"], self.format_align(tab_taux["TypeFrais1_eu"]))
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_11"], self.format_align(tab_taux["TypeFrais3_eu"]))
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_13"], self.format_align(tab_taux["TypeFrais1_eu"] + tab_taux["TypeFrais2_eu"] + tab_taux["TypeFrais3_eu"] + tab_taux["MontantFraisTransaction"]), True)

                
                # FranceValley
                case "M5":
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_7"], f"{tab_taux["TauxFraisTransaction"]:.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_8"], f"{(tab_taux["TypeFrais1_p"] + tab_taux["TypeFrais2_p"] + tab_taux["TypeFrais3_p"]):.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_9"], f"{tab_taux["TypeFrais1_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_10"], f"{tab_taux["TypeFrais2_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_11"], f"{tab_taux["TypeFrais3_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_13"], f"{(tab_taux["TypeFrais1_p"] + tab_taux["TypeFrais2_p"] + tab_taux["TypeFrais3_p"] + tab_taux["TauxFraisTransaction"]):.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_7"], self.format_align(tab_taux["MontantFraisTransaction"]), True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_8"], self.format_align(tab_taux["TypeFrais1_eu"] + tab_taux["TypeFrais2_eu"] + tab_taux["TypeFrais3_eu"]), True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_9"], self.format_align(tab_taux["TypeFrais1_eu"]))
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_10"], self.format_align(tab_taux["TypeFrais2_eu"]))
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_11"], self.format_align(tab_taux["TypeFrais3_eu"]))
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_13"], self.format_align(tab_taux["TypeFrais1_eu"] + tab_taux["TypeFrais2_eu"] + tab_taux["TypeFrais3_eu"] + tab_taux["MontantFraisTransaction"]), True)

                
                # Norma, Vatel
                case "M6":
                    tab_taux = self.Calcul_FraisPourcent_Avec_FraisEuros(tab_taux)

                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_7"], f"{tab_taux["TauxFraisTransaction"]:.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_8"], f"{(tab_taux["TypeFrais1_p"] + tab_taux["TypeFrais2_p"] + tab_taux["TypeFrais3_p"]):.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_9"], f"{tab_taux["TypeFrais1_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_10"], f"{tab_taux["TypeFrais2_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_11"], f"{tab_taux["TypeFrais3_p"]:.3f} %")
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_13"], f"{(tab_taux["TypeFrais1_p"] + tab_taux["TypeFrais2_p"] + tab_taux["TypeFrais3_p"] + tab_taux["TauxFraisTransaction"]):.3f} %", True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_7"], self.format_align(tab_taux["MontantFraisTransaction"]), True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_8"], self.format_align(tab_taux["TypeFrais1_eu"] + tab_taux["TypeFrais2_eu"] + tab_taux["TypeFrais3_eu"]), True)
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_9"], self.format_align(tab_taux["TypeFrais1_eu"]))
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_10"], self.format_align(tab_taux["TypeFrais2_eu"]))
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_11"], self.format_align(tab_taux["TypeFrais3_eu"]))
                    self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_13"], self.format_align(tab_taux["TypeFrais1_eu"] + tab_taux["TypeFrais2_eu"] + tab_taux["TypeFrais3_eu"] + tab_taux["MontantFraisTransaction"]), True)
           

        else:
            self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_7"], "0.00 %", True)
            self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_8"], "0.00 %", True)
            self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_9"], " ")
            self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_10"], " ")
            self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_11"], " ")
            self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_pourcent"]["Poucentage_13"], "0.00 %", True)
            self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_7"], "0.00 EUR", True)
            self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_8"], "0.00 EUR", True)
            self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_9"], " ")
            self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_10"], " ")
            self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_11"], " ")
            self.Inserer_TauxTableau_Coords(1, self.Coords_Fiche["Frais_euros"]["Montant_13"], "0.00 EUR", True)



    def format_align(self, val):
        if val < 100:
            base = f"{val:06.2f} EUR"
            base = "  " + base[1:]
        else:
            base = f"{val:.2f} EUR"
        return base



    def Definition_logo(self):
        BASE_DIR = Path(__file__).resolve().parent.parent.parent

        if self.Groupe == 'ASTORIA':
            match(self.Agence.upper()):
                case 'FIPAGEST':
                    self.Chemin_Logo = BASE_DIR / 'medias' / 'logos' / 'logo_fipagest.png'
                    self.Taille_Logo = 65

                case 'ASTORIA COURTAGE EST':
                    self.Chemin_Logo = BASE_DIR / 'medias' / 'logos' / 'logo_astoriacourtage.jpeg'
                    self.Taille_Logo = 60

                case _:
                    self.Chemin_Logo = BASE_DIR / 'medias' / 'logos' / 'astoriafinance2.jpg'
                    self.Taille_Logo = 75

        elif self.Groupe == 'INSINIA':
            match(self.Entite):
                case "ACTIONPATRIMOINE":
                    self.Chemin_Logo = BASE_DIR / 'medias' / 'logos' / 'logo_apc.jpg'
                    self.Taille_Logo = 65

                case "ALLUREFINANCE":
                    self.Chemin_Logo = BASE_DIR / 'medias' / 'logos' / 'logo_allurefinance.jpg'
                    self.Taille_Logo = 65

                case "BCFINANCES":
                    self.Chemin_Logo = BASE_DIR / 'medias' / 'logos' / 'logo_bcfinances.png'
                    self.Taille_Logo = 65

                case "CAPIUM":
                    self.Chemin_Logo = BASE_DIR / 'medias' / 'logos' / 'logo_capium.jpg'
                    self.Taille_Logo = 65

                case "FAMILYPATRIMOINE":
                    self.Chemin_Logo = BASE_DIR / 'medias' / 'logos' / 'logo_familypatrimoine.jpg'
                    self.Taille_Logo = 65

                case "FIPAGEST":
                    self.Chemin_Logo = BASE_DIR / 'medias' / 'logos' / 'logo_fipagest.png'
                    self.Taille_Logo = 65

                case "MYFAMILYOFFICER":
                    self.Chemin_Logo = BASE_DIR / 'medias' / 'logos' / 'logo_myfamilyofficer.jpeg'
                    self.Taille_Logo = 65

                case "PARISII":
                    self.Chemin_Logo = BASE_DIR / 'medias' / 'logos' / 'logo_parisii.png'
                    self.Taille_Logo = 65

                case "SOLVEPATRIMOINE":
                    self.Chemin_Logo = BASE_DIR / 'medias' / 'logos' / 'logo_solvepatrimoine.jpg'
                    self.Taille_Logo = 65

                case "SYNERGIECONSEILSPATRIMOINE":
                    self.Chemin_Logo = BASE_DIR / 'medias' / 'logos' / 'logo_synergie.png'
                    self.Taille_Logo = 65

                case "WATSONPATRIMOINE":
                    self.Chemin_Logo = BASE_DIR / 'medias' / 'logos' / 'logo_watson.jpg'
                    self.Taille_Logo = 50

                case _:
                    print("Aucune entité existante ne correspond !")


    def Definition_Mentions_Legales(self):
        if self.Groupe == 'INSINIA':
            match(self.Entite):
                case "ACTIONPATRIMOINE":
                    return """
ACTION PATRIMOINE CONSEIL  -  13 rue André Chénier 92130 Issy les Moulineaux - Tél. : 01.46.62.62.13 / contact@actionpatrimoineconseil.fr - www.actionpatrimoineconseil.fr - SAS au capital de 100 000 € - SIRET 444 726 483 00035 - R.C.S. de Nanterre 444 726 483  
Enregistré à l’ORIAS sous le n°07002709 (www.orias.fr) en qualité de courtier en assurance et conseiller en investissements financiers. 
Assurance responsabilité civile professionnelle : MMA IARD, 160 rue Henri Champion – 72030 Le Mans cedex 9.
Adhérent de la Chambre Nationale des Conseils en Gestion de Patrimoine, association agréée par l’Autorité des Marchés Financiers (AMF) et l’Autorité de contrôle prudentiel et de résolution (ACPR).
                    """

                case "ALLUREFINANCE":
                    return """
ALLURE FINANCE - 18 rue Troyon 75017 Paris - SAS au capital de 53 000 euros - RCS PARIS 521 019 521 - Code NAF 6622Z
Enregistrée à l’ORIAS sous le n°10054606 (www.orias.fr) en qualité de courtier d’assurance, de courtier en opérations de banque et en services de paiement et de conseiller en investissements financiers et adhérente de la CNCEF, association agréée par l'AMF et par l'ACPR. 
Activité de transactions sur immeubles et fonds de commerce, carte n° CPI75012018000028332 délivrée par la CCI de Paris Ile de France, sans détention de fonds.
Responsabilité civile professionnelle et garantie financière souscrites auprès de la compagnie MMA sise 160 Rue Henri Champion – 72030 Le Mans Cedex 9. 
                    """
                    
                case "BCFINANCES":
                    return """
BC FINANCES  -  1 rue Général Debeney 01000 Bourg-en-Bresse / 30 Rue Joannès Carret 69009 Lyon - Téléphone : 04 74 50 45 45 - SAS au capital de 42 000€ - SIRET : 414 732 164 00028 - RCS 414 732 164 Bourg-en-Bresse
Enregistrée à l’ORIAS sous le n°07 001 287 (www.orias.fr) en qualité de : Courtier en assurance - Conseiller en investissements financiers. Activité de transaction sur immeubles et fonds de commerce – Carte professionnelle n°CPI 01012017000018175 délivrée par la CCI de l’Ain 
Assurance responsabilité civile professionnelle : MMA IARD, 160 rue Henri Champion – 72030 Le Mans cedex 9 
Adhérent de la Chambre Nationale des Conseils en Gestion de Patrimoine, association agréée par l’Autorité des Marchés Financiers (AMF) et l’Autorité de contrôle prudentiel et de résolution (ACPR).
                    """
                    
                case "CAPIUM":
                    return """
CAPIUM  -  30, rue Joannès Carret – Immeuble Le BLOK – 69009 LYON - Téléphone : 04 72 69 97 00 - SAS CAPIUM, au capital de 100 000 € - SIRET : 483 588 570 00034 - RCS LYON 483 588 570
Enregistrée à l’ORIAS sous le n°07 005 070 en qualité de : Courtier d’assurance ou de réassurance (COA) ; Conseiller en investissements financiers (CIF) ; Courtier en opérations de banque et en services de paiement (COBSP)
Transaction sur Immeubles et Fonds de commerce – Carte professionnelle n°CPI 6901 2022 000 000 108, délivrée par la CCI de Lyon Métropole Saint-Etienne Roanne. Absence de garantie financière, non détention de fonds, effets ou valeurs pour compte de tiers.
Assurance responsabilité civile professionnelle : MMA IARD, 160 rue Henri Champion – 72030 Le Mans cedex 9 
Adhérent de la Chambre Nationale des Conseils en Gestion de Patrimoine, association agréée par l’Autorité des Marchés Financiers (AMF) et l’Autorité de contrôle prudentiel et de résolution (ACPR).
                    """
                    
                case "FAMILYPATRIMOINE":
                    return """
FAMILY PATRIMOINE  -  31 C Chemin du Vieux Chêne 38240 Meylan - T. 04 76 63 32 42 | contact@family-patrimoine.com | www.family-patrimoine.com - SAS au capital social de 136 200 € - Siret 51153725000025 - RCS de Grenoble n°511 537 250  
Enregistré à l’ORIAS sous le n°09050070 (www.orias.fr) en qualité de : Courtier en assurance ; Conseiller en investissement financier ; Intermédiaire en opérations de banque et services de paiement en qualité de Courtier. Transaction immobilière sur immeubles et fonds de commerce – Titulaire de la carte professionnelle n° CPI 3801 2018 000 032 357 délivrée par la CCI de Grenoble. 
Assurance responsabilité civile professionnelle : MMA IARD, 160 rue Henri Champion – 72030 Le Mans cedex 9 
Adhérent de la Chambre Nationale des Conseils en Gestion de Patrimoine, association agréée par l’Autorité des Marchés Financiers (AMF) et l’Autorité de contrôle prudentiel et de résolution (ACPR).
                    """
                    
                case "FIPAGEST":
                    return """
FIPAGEST  -  4 Boulevard Henry Vasnier – BP 90 398 – 51 064 REIMS Cedex - T 03 26 47 15 53 - patrimoine@fipagest.com - www.fipagest.com - SAS au capital de 1 000 000 € - Siret 39066146000068 - RCS REIMS 390 661 460 - Code APE 7022 Z 
Enregistrée à l’ORIAS sous le n° 07 001 060 (www.orias.fr), en qualité de courtier en assurance et de conseiller en investissements financiers – Activité de transaction sur immeubles et fonds de commerce – Carte professionnelle immobilière n° CPI 5102 2016 000 006 079 délivrée par la CCI de Reims et d’Epernay (Marne) – Activité de démarchage bancaire et financier.
Responsabilité civile professionnelle et garantie financière souscrites auprès de la compagnie MMA sise 160 Rue Henri Champion – 72030 Le Mans Cedex 9.
Adhérent de la Chambre Nationale des Conseils en Gestion de Patrimoine, association agréée par l’Autorité des Marchés Financiers (AMF) et l’Autorité de contrôle prudentiel et de résolution (ACPR).
                    """
                    
                case "MYFAMILYOFFICER":
                    return """
MY FAMILY OFFICER - SAS au capital de 10 210 euros - Siège social :  5-7 rue de Monttessuy 75007 Paris - Nos bureaux : 40 rue du Président Edouard Herriot 69001 Lyon
- SIRET : 84243929100027 - RCS PARIS 842 439 291 - Code NAF 7022Z - Tel : 06 18 04 40 34 - plb@myfamilyofficer.fr
Enregistrée à l’Orias sous le n°19001224 (www.orias.fr) en qualité de courtier d’assurance et de conseiller en investissements financiers, adhérent de la Chambre Nationale des Conseils en Gestion de Patrimoine, association agréée par l’Autorité des Marchés Financiers (AMF) et l’Autorité de contrôle prudentiel et de résolution (ACPR). Membre de l’Association Française du Family Office – www.affo.fr
Assurance responsabilité civile professionnelle : MMA IARD, 160 rue Henri Champion – 72030 Le Mans cedex 9
                    """
                    
                case "PARISII":
                    return """
PARISII GESTION PRIVEE  -  5-7 rue de Monttessuy 75007 Paris Cedex 07 - Tel : 01 86 95 91 96 / Email : contact@parisiigp.fr / Site : https://www.parisiigp.fr  - SAS au capital de 50 000 € - SIRET : 53428828700061 - RCS Paris 534 288 287 
Enregistrée à l’ORIAS sous le n° 11063403 en qualité de : Courtier d’assurance ou de réassurance (COA) ; Conseiller en investissements financiers (CIF) ; Courtier en opérations de banque et en services de paiement (COBSP)
Titulaire de la Carte de Transactions sur immeubles et fonds de commerce sans détention de fonds n°CPI 7501 2017 000 016 732 délivrée par la Chambre du Commerce et de l’Industrie d’Ile de France.
Responsabilité civile professionnelle et garantie financière souscrites auprès de la compagnie Zurich Insurance PLC 112 av. de Wagram 75017 Paris.
Adhérent de la Chambre Nationale des Conseils en Gestion de Patrimoine, association agréée par l’Autorité des Marchés Financiers (AMF) et l’Autorité de contrôle prudentiel et de résolution (ACPR).
                    """
                    
                case "SOLVEPATRIMOINE":
                    return """
SOLVE PATRIMOINE  -  301 rue Jacques Cellier - 73100 GRESY SUR AIX - Téléphone : 04 79 35 91 04 - SAS au capital de 20.000 euros - RCS de Chambéry 495 247 454  - SIRET 495 247 454 00053 
Enregistrée à l’ORIAS sous le n°07025862 ( www.orias.fr) en qualité de conseiller en investissements financiers (CIF), courtier en assurance et courtier en opérations de banque et en services de paiement. Titulaire de la carte professionnelle n° CPI 7301 2018 000 028 357, délivrée par la CCI de Savoie et permettant l’exercice de l’activité de transaction sur immeubles et fonds de commerce. 
Assurance responsabilité civile professionnelle : MMA IARD, 160 rue Henri Champion 72030 Le Mans cedex 9. 
Adhérent de la Chambre Nationale des Conseils en Gestion de Patrimoine, association agréée par l’Autorité des Marchés Financiers (AMF) et l’Autorité de contrôle prudentiel et de résolution (ACPR).
                    """
                    
                case "SYNERGIECONSEILSPATRIMOINE":
                    return """
SYNERGIE CONSEILS PATRIMOINE  -  5-7 rue de Monttessuy 75007 Paris - Tel : 04 97 10 04 08 /Email : scp@scpatrimoine.com / Site : www.scpatrimoine.com - SAS au capital de 10 000 € - SIREN : 388863037 - RCS Paris 388 863 037
Enregistrée à l’ORIAS sous le n° 07001251 en qualité de : Courtier d’assurance ou de réassurance (COA), Conseiller en investissements financiers (CIF) et Courtier en opérations de banque et en services de paiement (COBSP).
Titulaire de la carte professionnelle « transaction sur immeubles et fonds de commerce » n° CPI 7501 2017 000 016 691 délivrée par la Chambre de Commerce et d’Industrie de Paris Ile de France.
Responsabilité civile professionnelle et garantie financière souscrites auprès de la compagnie MMA sise 160 Rue Henri Champion – 72030 Le Mans Cedex 9.
Adhérent de la Chambre Nationale des Conseils en Gestion de Patrimoine, association agréée par l’Autorité des Marchés Financiers (AMF) et l’Autorité de contrôle prudentiel et de résolution (ACPR).
                    """
                    
                case "WATSONPATRIMOINE":
                    return """
WATSON PATRIMOINE  -  78, rue de la muse 17000 La Rochelle - Téléphone : 05 46 28 00 00 - SAS au capital de 1000€ - SIRET : 800 355 265 00029 - RCS 800 355 265 La Rochelle 
Enregistrée à l’ORIAS sous le n° 14002065 (www.orias.fr), en qualité de : Conseiller en investissements financiers. Courtier d’assurance ou de réassurance – Activité de transaction sur immeubles et fonds de commerce – Carte professionnelle n°CPI 1702 2020 000 044 979 délivrée par la CCI Charente-Maritime.
Assurance responsabilité civile professionnelle : MMA IARD, 160 rue Henri Champion 72030 Le Mans cedex 9.
Adhérent de la Chambre Nationale des Conseils en Gestion de Patrimoine, association agréée par l’Autorité des Marchés Financiers (AMF) et l’Autorité de contrôle prudentiel et de résolution (ACPR).
                    """
                    
                case _:
                    print("Aucune entité existante ne correspond !")

#-----------------------------------------------------------GÉNÉRATION-----------------------------------------------------------


    # Insertion des infos clients aux coordonnées stockés dans le dictionnaire de données
    def Inserer_Contenu_Coords(self, NumeroPage, EltDictionnaire, ValeurAjoutee, ABesoinDecalageGauche, Champs):
        coords_x0 = EltDictionnaire[0]
        coords_y0 = EltDictionnaire[1]
        coords_x1 = EltDictionnaire[2]
        coords_y1 = EltDictionnaire[3]
        page = self.doc[NumeroPage-1]

        # Ici, on le centre verticalement dans le rectangle
        hauteur_zone = coords_y1 - coords_y0
        
        # crée un rectangle blanc par dessus les placeholders
        rect = pymupdf.Rect(coords_x0, coords_y0+1, coords_x1, coords_y1)
        
        if Champs == "Produit":
            fontsize = 8
            fontname = "helv"
            width_text = pymupdf.get_text_length(ValeurAjoutee, fontsize=fontsize, fontname=fontname)

            # Calcule la largeur du placeholder
            largeur_placeholder = coords_x1 - coords_x0

            # Calcule la position X pour centrer le texte
            x_text = coords_x0 + (largeur_placeholder - width_text) / 2
            y_text = coords_y0 + hauteur_zone / 2  +3 

            # Insère le texte centré
            page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
            page.insert_text((x_text, y_text), ValeurAjoutee, fontsize=fontsize, fontname=fontname, color=(0, 0, 0))


        elif Champs == 'Logo':
            """
            # crée un rectangle pour contenir l'image
            rectImage = pymupdf.Rect(coords_x0-2, coords_y0-2, coords_x1+75, coords_y1+18)
            page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
            page.insert_image(rectImage, filename=ValeurAjoutee)
            """
            
            page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))

            pix = pymupdf.Pixmap(self.Chemin_Logo)

            # Définition de la largeur max du logo
            largeur_max = self.Taille_Logo

            # Calcul automatique de la hauteur en conservant les proportions (pour pas avoir une image écrasée)
            ratio = pix.height / pix.width
            hauteur_calculee = largeur_max * ratio

            # Définition des coordonnées du rectangle
            x0 = coords_x0
            y1 = coords_y1
            x1 = x0 + largeur_max
            y0 = y1 - hauteur_calculee

            image_rect = pymupdf.Rect(x0, y0, x1, y1)

            # Insertion de l'image avec taille exacte calculée avec keep_proportion=False
            page.insert_image(image_rect, pixmap=pix)  


        elif Champs == 'MentionsLegales':
            y_text = coords_y0 + hauteur_zone / 2  +3
            x_text = coords_x0 -35

            place_mentions = pymupdf.Rect(coords_x0+47, coords_y0-30, coords_x1-28, coords_y1+200)
            
            page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
            page.insert_textbox(place_mentions, ValeurAjoutee,fontsize=9,fontname="Times-Roman",color=(0, 0, 0),align=3)  # 0 = left, 1 = center, 2 = right, 3 = justified

        else:
            y_text = coords_y0 + hauteur_zone / 2  +3

            if ABesoinDecalageGauche == True:
                x_text = coords_x0 -15
            else:
                x_text = coords_x0 -5 

            #color (red, green, blue)
            page.draw_rect(rect, color=(1, 1, 1), fill=(1, 1, 1))
            page.insert_text((x_text, y_text), ValeurAjoutee, fontsize=9, fontname="helv", color=(0, 0, 0))


        """
        PDF_PATH_MODIFY = self.BASE_DIR / 'medias' / 'pdf' / 'modifie4.pdf'
        self.doc.save(PDF_PATH_MODIFY)
        """

    # Insertion des taux aux coordonnées stockés dans le dictionnaire de données
    def Inserer_TauxTableau_Coords(self, NumeroPage, EltDictionnaire, ValeurAjoutee, ligne_grise=False):
        coords_x0 = EltDictionnaire[0]
        coords_y0 = EltDictionnaire[1]
        coords_x1 = EltDictionnaire[2]
        coords_y1 = EltDictionnaire[3]
        page = self.doc[NumeroPage-1]

        # crée un rectangle blanc par dessus les placeholders
        rect = pymupdf.Rect(coords_x0, coords_y0+1, coords_x1, coords_y1)

        # Ici, on le centre verticalement dans le rectangle, avec un alignement différent pour la colonne EURO
        if ('EUR' in ValeurAjoutee):
            hauteur_zone = coords_y1 - coords_y0
            y_text = coords_y0 + hauteur_zone / 2  +5 
            x_text = coords_x0 -8
        else:
            hauteur_zone = coords_y1 - coords_y0
            y_text = coords_y0 + hauteur_zone / 2  +5 
            x_text = coords_x0 

        # gris clair ou blanc
        if ligne_grise:
            bg_color = (0.85, 0.85, 0.85)   
        else:
            bg_color = (1, 1, 1)  


        #color (red, green, blue)
        page.draw_rect(rect, color=bg_color, fill=bg_color)
        page.insert_text((x_text, y_text), ValeurAjoutee, fontsize=8, fontname="helv", color=(0, 0, 0))

        """
        PDF_PATH_MODIFY = self.BASE_DIR / 'medias' / 'pdf' / 'modifie4.pdf'
        self.doc.save(PDF_PATH_MODIFY)
        """        


    # Sauvegarde les modifs faite sur le pdf dans un buffer 
    # Sauvegarde ce fichier en mémoire et pas sur le disque pour pouvoir l'envoyer via une réponse HTTP
    def Sauver_dans_Buffer(self):
        buffer = io.BytesIO()
        self.doc.save(buffer)
        buffer.seek(0)
        return buffer


    # Reforme les données avant de les intégrer dans la fiche
    def ReformaterDonnées(self, Donnees, Variable):
        match(Variable):
            case "Bureau":
                if 'bureau' in Donnees.lower():
                    return Donnees.lower().replace("bureau ", "").title()
                elif Donnees == "" and self.Groupe == "INSINIA":

                    tempEntite = self.Entite.upper()
                    if tempEntite in self.VilleEntite:
                        return self.VilleEntite[tempEntite].title()
                else:
                    return Donnees.lower().title()
                
            case "FaitA":
                if 'bureau' in Donnees.lower():
                    tempDonnees = Donnees.lower().replace("bureau ", "")
                else:
                    tempDonnees = Donnees.lower()

                if tempDonnees.lower() in self.VilleBureau:
                    tempDonnees = self.VilleBureau[tempDonnees.lower()]
                    return tempDonnees.title()
                elif Donnees == "" and self.Groupe == "INSINIA":
                    tempEntite = self.Entite.upper()
                    if tempEntite in self.VilleEntite:
                        return self.VilleEntite[tempEntite].title()
                else:
                    return tempDonnees.title()
                
            case _:
                print("Mauvais champs")


    def Normaliser_texte_pdf(self, texte):
        return (texte
                .replace("’", "'")
                .replace("–", "-")
                .replace("€", " Euros"))


# s'exécute si ce fichier est exécuté directement
if __name__ == "__main__":
    test = Fiche_Reporting("", "", "","", "", "","", "", "","", "", "")
    test.Processus()
    




    # Structure détaillé après l'exécution de get_text("dict") dans la méthode d'analyse du fichier (pour les coords)

    # {
    #   "width": ...,
    #   "height": ...,
    #   "blocks": [
    #     {
    #       "type": 0,  # texte
    #       "bbox": (x0, y0, x1, y1),  # coordonnées du bloc
    #       "lines": [
    #         {
    #           "bbox": (x0, y0, x1, y1),  # coordonnées de la ligne
    #           "spans": [
    #             {
    #               "bbox": (x0, y0, x1, y1),  # coordonnées de la portion de texte (span)
    #               "text": "..."
    #               // autres infos (font, size, etc.)
    #             }
    #           ]
    #         }
    #       ]
    #     }
    #     // autres blocs...
    #   ]
    # }



    # Résultat renvoyé avec les coordonnées, par ex :
    # resultat un tuple : (x0, y0, x1, y1)

    # pymupdf axe : 
        
    #    ------------>  x
    #   |
    #   |
    #   |
    #   |
    #   V 
    #     y


    #   (x0, y0) -------------------------
    #   |                                |
    #   |         "Nom :   "             |
    #   |                                |
    #    -------------------------(x1, y1)