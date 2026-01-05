import pandas as pd
from app.routes.getter_setter_data.setter_data_from_xlsx.setter_Clients_data import setter_data_tclients



def getter_data_client(Client_doc):
    
    Entreprises = ['ACP', 'ASTORIA COURTAGE', 'KARA FINANCES', 'ERP COURTAGE', 'INVEST CONSULTING', 'SPI CONSEIL', 'FIPAGEST', 'EQUATIO FINANCES', 'SAPIENTA GESTION', 'IN PATRIMOINE', 'ACTION PATRIMOINE CONSEIL',
                   'APC IMMOBILIER', 'PARISII', 'BC FINANCES', 'SOLVE PATRIMOINE', 'CAPIUM', 'FAMILY PATRIMOINE', 'PB WEALTH MANAGER', 'CV FINANCES', 'SYNERGIE CONSEILS PATRIMOINE',
                   'MY FAMILY OFFICER']
    
    Contenu_NonDesire_Colonne_ConseillerPrincipal = Recuperation_contenu_colonne_conseillerprincipal(Client_doc, Entreprises)
    Contenu_NonDesire_Colonne_AutreConseiller = Recuperation_contenu_colonne_autreconseiller(Client_doc, Contenu_NonDesire_Colonne_ConseillerPrincipal, Entreprises)
    Tab_Clients = []
    NumClient = 1
    
    print(Contenu_NonDesire_Colonne_ConseillerPrincipal)
    print(Contenu_NonDesire_Colonne_AutreConseiller)
    print("\n\n")

    for index, row in Client_doc.iterrows():

        #si la colonne 'NOM' est remplie
        if pd.notna(row["Nom"]):
            Num_ligne = index
            Nom = str(row["Nom"]).upper()
            if pd.notna(row["Prénom"]):
                Prenom = str(row["Prénom"]).lower().capitalize()
            else:
                Prenom = ''
            Entreprise = 'Astoria'

            Region = ''
            Bureau = ''
            ConseillerPrincipal = ''

            # SI la région est contenue dans la colonne Conseiller Principal
            # ET SI le bureau est contenu dans la colonne Autre Conseiller 
            """
            if row["Conseiller principal"] in Contenu_NonDesire_Colonne_ConseillerPrincipal and row["Autre conseiller"] in Contenu_NonDesire_Colonne_AutreConseiller:
                if 'region' in str(row["Conseiller principal"]).lower():
                    Region = row["Conseiller principal"]
                if 'bureau' in str(row["Autre conseiller"]).lower():
                    Bureau = row["Autre conseiller"]
                if str(row["Assistant(e)"]).lower() != 'non défini(e)' and str(row["Assistant(e)"]).lower() != 'nan':
                    ConseillerPrincipal = row["Assistant(e)"]
            
            # SI le bureau est contenu dans la colonne Conseiller Principal
            # SI le conseiller est contenu dans la colonne Autre Conseiller
            elif 'bureau' in str(row["Conseiller principal"]).lower() or row["Conseiller principal"] in Entreprises:
                Bureau = row["Conseiller principal"]
                if str(row["Autre conseiller"]).lower() != 'non défini(e)' and str(row["Autre conseiller"]).lower() != 'nan':
                    ConseillerPrincipal = row["Autre conseiller"]
            """

            if row["Conseiller principal"] in Contenu_NonDesire_Colonne_ConseillerPrincipal:
                if 'region' in str(row["Conseiller principal"]).lower():
                    Region = row["Conseiller principal"]
            
            if row["Autre conseiller"] in Contenu_NonDesire_Colonne_AutreConseiller:
                if 'bureau' in str(row["Autre conseiller"]).lower():
                    Bureau = row["Autre conseiller"]

            if row["Conseiller principal"] in Entreprises:
                Bureau = row["Conseiller principal"]
                if str(row["Autre conseiller"]).lower().strip() not in ['non défini(e)', 'nan'] and not pd.isna(row["Autre conseiller"]):
                    ConseillerPrincipal = row["Autre conseiller"]

            if str(row["Assistant(e)"]).lower().strip() not in ['non défini(e)', 'nan'] and not pd.isna(row["Assistant(e)"]):
                    ConseillerPrincipal = row["Assistant(e)"]


            Description = f"{Nom} {Prenom}"

            if Description not in Tab_Clients:
                 #print(f"Ligne {Num_ligne+2} =  Client nom : '{Nom}', Prénom : '{Prenom}', Région : '{Region}', Bureau : '{Bureau}', Conseiller : '{ConseillerPrincipal}'")
                print(f"Ligne {NumClient} =  Client nom : '{Nom}', Prénom : '{Prenom}', Région : '{Region}', Bureau : '{Bureau}', Conseiller : '{ConseillerPrincipal}'\n")
                NumClient += 1
                #print(f"Ligne {Num_ligne+2} = Nom/Prenom : {Description}")
                Tab_Clients.append(Description)
                #setter_data_tclients(Nom, Prenom, Description, Region, Bureau, ConseillerPrincipal, Entreprise)



#permet de récupérer toutes lignes qui ont la colonne de Compte au 31/12/2024 qui est égale à 0.00 (ou inférieur à 0.01 = 1 centime)
def Recuperation_colonne_Compte31decembre(Client_doc):
    valeur = 0
    for index, row in Client_doc.iterrows():
        Num_ligne = index
        Nom = row["Nom"]
        Prenom = row["Prénom"]
        Date_Decembre = row["Compte au 31/12/2024 (€)"]

        if pd.notna(Date_Decembre) and (Date_Decembre < 0.01):
            valeur += 1
            print(f"Ligne {Num_ligne+2} =  Client nom : {Nom}, prénom : {Prenom}")

    print(f"Nombre de compte au 31/12/24 à moins de 1 centime : {valeur}")



#permet de récupérer toutes les valeurs parasites qui ne devraient pas être dans la colonne de Conseiller principal
def Recuperation_contenu_colonne_conseillerprincipal(Client_doc, Entreprise):
    Contenu_Colonne_ConseillerPrincipal = []
    
    for index, row in Client_doc.iterrows():
        col_conseillerPrincipal = str(row["Conseiller principal"])

        if ((col_conseillerPrincipal in Entreprise) or ('region' in col_conseillerPrincipal.lower()) or ('bureau' in col_conseillerPrincipal.lower())
            or (col_conseillerPrincipal.lower() == 'nan')):
            if col_conseillerPrincipal not in Contenu_Colonne_ConseillerPrincipal:
                Contenu_Colonne_ConseillerPrincipal.append(col_conseillerPrincipal)
    """
    print(f'\nTaille tableau d\'éléments non désirés conseiller principal : {len(Contenu_Colonne_ConseillerPrincipal)}')
    for elt in Contenu_Colonne_ConseillerPrincipal:
        print(f"'{elt}',")
    """

    return Contenu_Colonne_ConseillerPrincipal




#permet de récupérer toutes les valeurs parasites qui ne devraient pas être dans la colonne de Autre Conseiller
def Recuperation_contenu_colonne_autreconseiller(Client_doc, Contenu_NonDesire_Colonne_ConseillerPrincipal, Entreprises):
    Contenu_Colonne_AutreConseiller = []
    
    for index, row in Client_doc.iterrows():
        col_autreConseiller = str(row["Autre conseiller"])

        if ((col_autreConseiller in Entreprises) or (col_autreConseiller in Contenu_NonDesire_Colonne_ConseillerPrincipal) 
            or ('bureau' in col_autreConseiller.lower()) or ('region' in col_autreConseiller.lower())
            or (col_autreConseiller.lower() == 'non défini(e)') or (col_autreConseiller.lower() == 'nan')):
            if (col_autreConseiller not in Contenu_Colonne_AutreConseiller):
                Contenu_Colonne_AutreConseiller.append(col_autreConseiller)

    """
    print(f'\nTaille tableau d\'éléments non désirés autre conseiller : {len(Contenu_Colonne_AutreConseiller)}')
    for elt in Contenu_Colonne_AutreConseiller:
        print(f"'{elt}',")
    """

    return Contenu_Colonne_AutreConseiller

