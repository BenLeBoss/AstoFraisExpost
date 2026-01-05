import os
import pandas as pd
from pathlib import Path

#Clients
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_Clients_data import getter_data_client

#Produits
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_Produits_data import getter_data_produits

#Produits par Clients
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_ClientProduits_data import getter_data_clientproduits

# AstoriaFinance Fournisseur
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_DATA_FichierClients import getter_data_FichierClients
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_Fournisseur_PERIAL import getter_data_fournisseur_Perial
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_Fournisseur_FRANCEVALLEY import getter_data_fournisseur_FranceValley
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_Fournisseur_ATLANDVOISIN import getter_data_fournisseur_AtlandVoisin
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_Fournisseur_CORUM import getter_data_fournisseur_Corum
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_Fournisseur_URBANPREMIUM import getter_data_fournisseur_UrbanPremium
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_Fournisseur_THEOREIM import getter_data_fournisseur_Theoreim
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_Fournisseur_SMALTCAPITAL import getter_data_fournisseur_SmaltCapital
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_Fournisseur_KEYS import getter_data_fournisseur_Keys
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_Fournisseur_EIFFEL import getter_data_fournisseur_Eiffel
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_Fournisseur_NORMACAPITAL import getter_data_fournisseur_NormaCapital
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_Fournisseur_LAFRANCAISE import getter_data_fournisseur_LaFrancaise
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_Fournisseur_123IM import getter_data_fournisseur_123IM
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_Fournisseur_ALPHEYS_AllProducts import getter_data_fournisseur_Alpheys_AllProduits
from app.routes.getter_setter_data.getter_data_from_xlsx.ASTORIA_FINANCE.getter_Fournisseur_VATEL import getter_data_fournisseur_Vatel



# Insinia Fournisseur
from app.routes.getter_setter_data.getter_data_from_xlsx.ENTITES_INSINIA.getter_DATA_FichierClientsInsinia import getter_data_FichierClientsInsinia
from app.routes.getter_setter_data.getter_data_from_xlsx.ENTITES_INSINIA.getter_AllFournisseur_AllEntites import getter_AllFournisseur_AllEntites




def Main():

    # Ouverture du fichier client Astoria
    BASE_DIR = Path(__file__).resolve().parents[2]  # 2 niveaux au-dessus de ce fichier
    """
    EXCEL_PATH_ASTORIA = BASE_DIR / 'medias' / 'excel' / '2025' / 'Astoria_Finance_Requete_client_CIF_31_12_24_Novembre.xlsx'
    Client_doc_Astoria = Connect_File_xlsx(EXCEL_PATH_ASTORIA, 0, "", True)
    """

    # DÉCOMMENTER LES LIGNES AU FUR ET A MESURE

    
    # ---------------------------- ASTORIA FINANCE ----------------------------

    # CLIENTS ASTORIA FINANCE

    """
    getter_data_FichierClients(Client_doc_Astoria)
    """
    """
    getter_data_client(Client_doc_Astoria)
    getter_data_produits(Client_doc_Astoria)
    getter_data_clientproduits(Client_doc_Astoria)
    """


    # Perial
    """
    EXCEL_PATH_PERIAL = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'Perial_Am_Frais_ex_post_2024.xlsx'
    Client_doc_Perial = Connect_File_xlsx(EXCEL_PATH_PERIAL, 0, "", True)
    getter_data_fournisseur_Perial(Client_doc_Perial)
    """

    # FranceValley
    """
    EXCEL_PATH_FRANCEVALLEY = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'France_Valley_Frais_ex_post_2024.xlsx'
    Client_doc_FranceValley = Connect_File_xlsx(EXCEL_PATH_FRANCEVALLEY, 1, "DATA", True)
    getter_data_fournisseur_FranceValley(Client_doc_FranceValley)
    """
    
    # Atland Voisin
    """
    EXCEL_PATH_ATLANDVOISIN = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'Atland_Voisin_Frais_ex_post_2024.xlsx'
    Client_doc_AtlandVoisin = Connect_File_xlsx(EXCEL_PATH_ATLANDVOISIN, 0, "", True)
    getter_data_fournisseur_AtlandVoisin(Client_doc_AtlandVoisin)
    """
    
    # Corum
    """
    EXCEL_PATH_CORUM = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'Corum_Epargne_Frais_ex_post_2024.xlsx'
    Client_doc_Corum = Connect_File_xlsx(EXCEL_PATH_CORUM, 0, "", True)
    getter_data_fournisseur_Corum(Client_doc_Corum)
    """
    
    # Urban premium
    """
    EXCEL_PATH_URBAN = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'Urban_Premium_Frais_ex_post_2024.xlsx'
    Client_doc_Urban = Connect_File_xlsx(EXCEL_PATH_URBAN, 0, "", True)
    getter_data_fournisseur_UrbanPremium(Client_doc_Urban)
    """

    # Theoreim
    """
    EXCEL_PATH_Theoreim = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'Theoreim_Frais_ex_post_2024.xlsx'
    Client_doc_Theoreim = Connect_File_xlsx(EXCEL_PATH_Theoreim, 0, "", True)
    getter_data_fournisseur_Theoreim(Client_doc_Theoreim)
    """

    # Smalt capital
    """    
    EXCEL_PATH_SMALT = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'Smalt_Capital_Frais_ex_post_2024.xlsx'
    Client_doc_Smalt = Connect_File_xlsx(EXCEL_PATH_SMALT, 0, "", True)
    getter_data_fournisseur_SmaltCapital(Client_doc_Smalt)
    """

    # Keys
    """
    EXCEL_PATH_KEYS = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'Keys_Frais_ex_post_2024.xlsx'
    Client_doc_Keys = Connect_File_xlsx(EXCEL_PATH_KEYS, 1, "", False)
    getter_data_fournisseur_Keys(Client_doc_Keys, "I")
    """

    # Eiffel
    """
    EXCEL_PATH_EIFFEL = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'Eiffel_Frais_ex_post_2024.xlsx'
    Client_doc_Eiffel = Connect_File_xlsx(EXCEL_PATH_EIFFEL, 0, "", True)
    getter_data_fournisseur_Eiffel(Client_doc_Eiffel)
    """

    # Norma capital
    """
    EXCEL_PATH_NORMA = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'Norma_Capital_Frais_ex_post_2024.xlsx'
    getter_data_fournisseur_NormaCapital(EXCEL_PATH_NORMA)
    """

    # La Française
    """
    EXCEL_PATH_FRANCAISE = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'La_Francaise_Frais_ex_post_2024.xlsx'
    Client_doc_Eiffel = Connect_File_xlsx(EXCEL_PATH_FRANCAISE, 0, "La Française Real Estate Manage", True)
    getter_data_fournisseur_LaFrancaise(Client_doc_Eiffel)
    """

    # 123IM
    """
    EXCEL_PATH_FOURNISSEURS123IM = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / '123IM_Frais_ex_post_2024.xlsx'
    Client_doc_123IM = Connect_File_xlsx(EXCEL_PATH_FOURNISSEURS123IM, 1, "Fonds 2018", False)
    getter_data_fournisseur_123IM(Client_doc_123IM, "D")
    Client_doc_123IM = Connect_File_xlsx(EXCEL_PATH_FOURNISSEURS123IM, 1, "Fonds 2019", False)
    getter_data_fournisseur_123IM(Client_doc_123IM, "D")
    Client_doc_123IM = Connect_File_xlsx(EXCEL_PATH_FOURNISSEURS123IM, 1, "Fonds 2020", False)
    getter_data_fournisseur_123IM(Client_doc_123IM, "D")
    Client_doc_123IM = Connect_File_xlsx(EXCEL_PATH_FOURNISSEURS123IM, 1, "Fonds 2021", False)
    getter_data_fournisseur_123IM(Client_doc_123IM, "D")
    Client_doc_123IM = Connect_File_xlsx(EXCEL_PATH_FOURNISSEURS123IM, 1, "Fonds 2022", False)
    getter_data_fournisseur_123IM(Client_doc_123IM, "D")
    Client_doc_123IM = Connect_File_xlsx(EXCEL_PATH_FOURNISSEURS123IM, 1, "Fonds 2022 bis", False)
    getter_data_fournisseur_123IM(Client_doc_123IM, "C")
    Client_doc_123IM = Connect_File_xlsx(EXCEL_PATH_FOURNISSEURS123IM, 1, "Fonds 2023", False)
    getter_data_fournisseur_123IM(Client_doc_123IM,  "D")
    Client_doc_123IM = Connect_File_xlsx(EXCEL_PATH_FOURNISSEURS123IM, 1, "Fonds 2024", False)
    getter_data_fournisseur_123IM(Client_doc_123IM, "D")
    """

    # ALPHEYS
    # Pierval Santé
    """
    EXCEL_PATH_PRODUITPIERVAL = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'ALPHEYS_Pierval_Sante_Frais_ex_post_2024.xlsx'
    Client_doc_PiervalSante = Connect_File_xlsx(EXCEL_PATH_PRODUITPIERVAL, 0, "", True)
    getter_data_fournisseur_Alpheys_AllProduits(Client_doc_PiervalSante, "Produits")
    """
    # Activimmo
    """
    EXCEL_PATH_ACTIVIMMO = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'ALPHEYS_Activimmo_Frais_ex_post_2024.xlsx'
    Client_doc_Activimmo = Connect_File_xlsx(EXCEL_PATH_ACTIVIMMO, 0, "Synthèse", True)
    getter_data_fournisseur_Alpheys_AllProduits(Client_doc_Activimmo, "Pourcentage")
    """


    # Vatel
    """
    EXCEL_PATH_VATEL = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'Vatel_Frais_ex_post_2024.xlsx'
    Client_doc_VatelAstoFinance = Connect_File_xlsx(EXCEL_PATH_VATEL, 0, "Astoria Finance", True)
    getter_data_fournisseur_Vatel(Client_doc_VatelAstoFinance)
    Client_doc_VatelAstoCourtage = Connect_File_xlsx(EXCEL_PATH_VATEL, 0, "Astoria Courtage", True)
    getter_data_fournisseur_Vatel(Client_doc_VatelAstoCourtage)
    """



    # ---------------------------- ENTITÉS INSINIA ----------------------------

    
    # CLIENTS WATSON
    """
    EXCEL_PATH_CLIENTSINSINIA = BASE_DIR / 'medias' / 'excel' / '2025' / '2024_INSINIA_FichierClients_Watson_Frais_expost.xlsx'
    Client_doc_ClientsInsinia = Connect_File_xlsx(EXCEL_PATH_CLIENTSINSINIA, 0, "", True)
    getter_data_FichierClientsInsinia(Client_doc_ClientsInsinia, "WATSON")
    """
    
    # FOURNISSEUR WATSON
    """
    EXCEL_PATH_FOURNISSEURSINSINIAKEYS1 = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'INSINIA' / 'WATSON' / 'KEYS' / '2024_WATSON_Keys_Rendement_6_ans.xlsx'
    Client_doc_InsiniaWatson = Connect_File_xlsx(EXCEL_PATH_FOURNISSEURSINSINIAKEYS1, 1, "PART A", False)
    getter_AllFournisseur_AllEntites(Client_doc_InsiniaWatson, "KEYS", "WATSON", "I")

    EXCEL_PATH_FOURNISSEURSINSINIAKEYS2 = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'INSINIA' / 'WATSON' / 'KEYS' / '2024_WATSON_Keys_Rendement_Liberté.xlsx'
    Client_doc_InsiniaWatson = Connect_File_xlsx(EXCEL_PATH_FOURNISSEURSINSINIAKEYS2, 1, "PART A", False)
    getter_AllFournisseur_AllEntites(Client_doc_InsiniaWatson, "KEYS", "WATSON", "I")

    EXCEL_PATH_FOURNISSEURSINSINIAKEYS3 = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'INSINIA' / 'WATSON' / 'KEYS' / '2024_WATSON_Keys_Selection.xlsx'
    Client_doc_InsiniaWatson = Connect_File_xlsx(EXCEL_PATH_FOURNISSEURSINSINIAKEYS3, 1, "PART A", False)
    getter_AllFournisseur_AllEntites(Client_doc_InsiniaWatson, "KEYS", "WATSON", "I")

    EXCEL_PATH_FOURNISSEURSINSINIAKEYS4 = BASE_DIR / 'medias' / 'excel' / '2025' / 'partenaires' / 'INSINIA' / 'WATSON' / 'KEYS' / '2024_WATSON_Keys_Value_Added.xlsx'
    Client_doc_InsiniaWatson = Connect_File_xlsx(EXCEL_PATH_FOURNISSEURSINSINIAKEYS4, 1, "PART A", False)
    getter_AllFournisseur_AllEntites(Client_doc_InsiniaWatson, "KEYS", "WATSON", "I")
    """




# Lit le fichier à l'aide du répertoire et nom du fichier, à quelle ligne se trouve les titres de colonne, et dans quelle feuille il faut parcourir les données
def Connect_File_xlsx(EXCEL_PATH, header, sheetname, fichier_encolonne):
    
    # Si le fichier est rédigé en colonnes
    if fichier_encolonne:
        if sheetname != "":
            Client_doc = pd.read_excel(EXCEL_PATH, header=header, sheet_name=sheetname)
        else:
            Client_doc = pd.read_excel(EXCEL_PATH, header=header)

    # Si le fichier est rédigé en lignes
    else:
        if sheetname != "":
            Client_doc = pd.read_excel(EXCEL_PATH, header=None, sheet_name=sheetname)
        else:
            Client_doc = pd.read_excel(EXCEL_PATH, header=None)
        
        # Commence à la colonne choisie
        if header > 0 :
            Client_doc = Client_doc.iloc[:, header:]
    

    Client_doc.info()
    print(f"Nombre de lignes dans le fichier : {len(Client_doc)}\n\n")

    return Client_doc

Main()