import unicodedata

# Initialise les frais d'entrée et calcule le montant en euros 
class FraisEntree:

    def __init__(self, Founisseur, MontantTotal, NomProduit):
        self.Fournisseur = Founisseur
        self.MontantTotal = MontantTotal
        self.NomProduit = self.TransfoNom(NomProduit)
        
        # Les frais à appliquer aux produits partenaire qui ne les ont pas renseignés DIRECTEMENT dans leur fichier EMT
        # Ces frais peuvent être appliqués aux éléments qui ont une date d'ouverture et qui ont des comptes qui ont été ouverts sur l'année courante
        self.FournisseurFraisEntree = {
            "ALPHEYS" : {
                    "PIERVAL SANTE" : { "TauxFrais" : 5.5, "TVA" : 20 },
                    "ACTIVIMMO" : { "TauxFrais" : 6, "TVA" : 20 },
                    "EPARGNE PIERRE" : { "TauxFrais" : 5.5, "TVA" : 20 },
                    "EPARGNE FONCIERE" : { "TauxFrais" : 5.65, "TVA" : 20 },
                    "ALTIXIA COMMERCES" : { "TauxFrais" : 6, "TVA" : 20 },
                    "ALTIXIA CADENCE XII" : { "TauxFrais" : 7, "TVA" : 20 },
                    "LF EUROPIMMO" : { "TauxFrais" : 6, "TVA" : 20 },
                    "COEUR DE VILLE" : { "TauxFrais" : 6.75, "TVA" : 20 },
                    "COEUR DE REGIONS" : { "TauxFrais" : 6.75, "TVA" : 20 },
                    "COEUR D'EUROPE" : { "TauxFrais" : 6.75, "TVA" : 20 },
                    "ALTA CONVICTIONS" : { "TauxFrais" : 7, "TVA" : 20 },
                    "VENDOME REGIONS" : { "TauxFrais" : 6, "TVA" : 20 },
                    "ALTA CONVICTIONS" : { "TauxFrais" : 7, "TVA" : 20 },
                    "PRIMOVIE" : { "TauxFrais" : 5.5, "TVA" : 0 },
            },

            "ATLAND VOISIN" : {
                    "EPARGNE PIERRE" : { "TauxFrais" : 5.5, "TVA" : 0 }
            },

            "CORUM L\'EPARGNE" : {
                    "CC" : { "TauxFrais" : 3, "TVA" : 20 },
                    "EU" : { "TauxFrais" : 5.5, "TVA" : 20 },
                    "XL" : { "TauxFrais" : 6, "TVA" : 0 }
            },

            "PERIAL ASSET MANAGEMENT" : {
                    "PF GRAND PARIS" : { "TauxFrais" : 5.5, "TVA" : 20 }, 
                    "PF HOSPITALITE EUROPE" : { "TauxFrais" : 5.5, "TVA" : 20 }, 
                    "PFO" : { "TauxFrais" : 5.5, "TVA" : 20 },
                    "PFO2" : { "TauxFrais" : 5.8, "TVA" : 20 }
            },

            "THEOREIM" : {
                    "LOG IN" : {"TauxFrais" : 5.5, "TVA" : 0 }
            },

            "URBAN PREMIUM" : {
                    "URBAN PRESTIGIMMO 2" : { "TauxFrais" : 5.5, "TVA" : 0 }
            },

        }

    def __del__(self):
        pass


    def TransfoMontantFloat(self):
        tempCompte_31_12 = self.MontantTotal
        if " " in tempCompte_31_12:
            tempCompte_31_12 = float(tempCompte_31_12.replace(" ", ""))
            tempCompte_31_12 = round(tempCompte_31_12, 2)
        else:
            tempCompte_31_12 = round(float(self.MontantTotal), 2)

        self.MontantTotal = tempCompte_31_12


    def TransfoNom(self, NomProduit):
        champ = NomProduit.upper()

        # décompose les accents et enlève les accents
        champ = unicodedata.normalize('NFKD', champ)  
        champ = ''.join(c for c in champ if not unicodedata.combining(c))  


        return champ




    def Get_FraisEntree(self):
        print(self.NomProduit)
        if self.Fournisseur in self.FournisseurFraisEntree:
            
            if self.FournisseurFraisEntree[self.Fournisseur][self.NomProduit]["TauxFrais"] > 0:

                self.TransfoMontantFloat()

                TauxFrais = self.FournisseurFraisEntree[self.Fournisseur][self.NomProduit]["TauxFrais"]
                TVA = self.FournisseurFraisEntree[self.Fournisseur][self.NomProduit]["TVA"]
                TauxFraisTVAFinal = TauxFrais + (TauxFrais * (TVA / 100))
                FraisEurosFinal = ((float(self.MontantTotal) * TauxFraisTVAFinal) / 100)

                print(f"valeur TauxFraisTVAFinal = {TauxFraisTVAFinal} et valeur FraisEurosFinal = {FraisEurosFinal}")

                ListeFraisCalcule = {
                    "TauxFraisTVAFinal" : TauxFraisTVAFinal,
                    "FraisEurosFinal" : FraisEurosFinal
                }

                return ListeFraisCalcule


