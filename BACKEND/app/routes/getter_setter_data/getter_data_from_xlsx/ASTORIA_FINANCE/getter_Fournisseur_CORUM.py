import pandas as pd
from app.routes.getter_setter_data.setter_data_from_xlsx.setter_Fournisseurs_data import setter_data_fournisseur_corum



def getter_data_fournisseur_Corum(Fournisseur_doc):
    
    print("Colonnes disponibles :", Fournisseur_doc.columns.tolist())


    for index, row in Fournisseur_doc.iterrows():

        #si la colonne 'NOM' est remplie
        if pd.notna(row["Nom client"]):
            Num_ligne = index

            Civilite = ''
            Nom = ''
            Prenom = ''
            tempNomPrenom = ''

            if 'M. ET MME' in row["Nom client"].upper() or 'MME ET M.' in row["Nom client"].upper():
                Civilite = 'M. et Mme'
                if pd.notna(row["Client personne physique"]):
                    if 'MR'  in row["Client personne physique"].upper():
                        Civilite = 'Monsieur'
                        tempNomPrenom = row["Client personne physique"].removeprefix('Mr')
                    elif 'MME' in row["Client personne physique"].upper():
                        Civilite = 'Madame'
                        tempNomPrenom = row["Client personne physique"].removeprefix('Mme')
                

            elif 'MME' in row["Nom client"].upper():
                Civilite = 'Madame'
                tempNomPrenom = row["Nom client"].removeprefix('Mme')

            elif 'M.'  in row["Nom client"].upper():
                Civilite = 'Monsieur'
                tempNomPrenom = row["Nom client"].removeprefix('M.')

            elif 'HOLDING' in row["Nom client"].upper():
                Civilite = 'HOLDING'
                tempNomPrenom = row["Nom client"].removeprefix('HOLDING')



            if Civilite == 'HOLDING':
                NomPrenom = tempNomPrenom.split()
                NomCompose = False
                for elt in NomPrenom:
                    if NomCompose:
                        Nom += ' '
                    if elt.isupper():
                        Nom += elt.encode('latin1').decode('utf-8')
                        NomCompose = True

            elif Civilite in ('Madame', 'Monsieur'):
                NomPrenom = tempNomPrenom.split()
                NomCompose = False
                PrenomCompose = False
                for elt in NomPrenom:
                    if NomCompose:
                        Nom += ' '
                    if PrenomCompose:
                        Prenom += ' '
                    if elt.isupper():
                        Nom += elt.encode('latin1').decode('utf-8')
                        NomCompose = True
                    else:
                        Prenom += elt.encode('latin1').decode('utf-8')
                        PrenomCompose = True

            else:
                Nom = row["Nom client"].strip()
                
                
            if Civilite == '':
                Civilite = 'SCI'


            #NumCompte = str(row["Code Client"]).zfill(6)
            IntituleProduit = str(row["Produit"])

            TypeFrais1_percent = row["Pourcentage frais rÃ©currents"]
            TypeFrais1_euros = row["Frais rÃ©currents"]
            TypeFrais2_percent = row["Pourcentage frais immobiliers"]
            TypeFrais2_euros = row["Frais immobiliers"]
            TypeFrais3_percent = row["Pourcentage coÃ»ts transaction"]
            TypeFrais3_euros = row["CoÃ»ts transaction"]

            Total = float(TypeFrais1_euros) + float(TypeFrais2_euros) + float(TypeFrais3_euros) 

            TauxCommission = 5.5    # 5.5%
            TVA = 20    # 20%
            TauxPaiementTiers = ((TauxCommission * TVA) / 100)

            print(f"Ligne {Num_ligne+2} =  Client nom : '{Nom}', Prénom : '{Prenom}', Produit : '{IntituleProduit}'")
            print(f"           Total : {Total},  Frais 1 (%, euros) : '{str(TypeFrais1_percent)}, {str(TypeFrais1_euros)}' // Frais 2 (%, euros) : '{str(TypeFrais2_percent)}, {str(TypeFrais2_euros)}' // Frais 3 (%, euros) : '{str(TypeFrais3_percent)}, {str(TypeFrais3_euros)}' ")
            setter_data_fournisseur_corum(Civilite, Nom, Prenom, IntituleProduit, TypeFrais1_percent, TypeFrais1_euros, TypeFrais2_percent, TypeFrais2_euros, 
                                                    TypeFrais3_percent, TypeFrais3_euros, "M4")







