import pandas as pd
from app.routes.getter_setter_data.setter_data_from_xlsx.setter_Fournisseurs_data import setter_data_fournisseur_norma



def getter_data_fournisseur_NormaCapital(PATH_NORMA):
    
    PersonnesMorales_Doc_Norma = Connect_File_xlsx(PATH_NORMA, 6, "Personnes Morales", True)
    get_PersonnesMorales(PersonnesMorales_Doc_Norma)

    PersonnesPhysiques_Doc_Norma = Connect_File_xlsx(PATH_NORMA, 7, "Personnes physiques", True)
    get_PersonnesPhysiques(PersonnesPhysiques_Doc_Norma)




def Connect_File_xlsx(EXCEL_PATH, header, sheetname, fichier_encolonne):
    
    if fichier_encolonne:
        if sheetname != "":
            Client_doc = pd.read_excel(EXCEL_PATH, header=header, sheet_name=sheetname)
        else:
            Client_doc = pd.read_excel(EXCEL_PATH, header=header)

    Client_doc.info()
    print(f"Nombre de lignes dans le fichier : {len(Client_doc)}\n\n")

    return Client_doc


# Récupère et intègre les personnes morales
def get_PersonnesMorales(Fournisseur_doc):
    
    print("Colonnes disponibles :", Fournisseur_doc.columns.tolist())

    for index, row in Fournisseur_doc.iterrows():

        if pd.notna(row["Raison Sociale - Souscripteur"]):
            if ("total" not in str(row["Raison Sociale - Souscripteur"]).lower()):

                Num_ligne = index
                Nom = str(row["Raison Sociale - Souscripteur"]).upper().strip()
                Prenom = ''

                MontantTotalSouscritAnneeCourante = row["Encours 2024"]

                TypeFrais1_percent = 0.0
                TypeFrais1_euros = row["Frais récurrent - 2024"] + row["Frais immobilier 2024"]
                TypeFrais2_percent = 0.0
                TypeFrais2_euros = row["Frais unique 2024"]
                TypeFrais3_percent = 0.0
                TypeFrais3_euros = row["Frais de transation 2024"]


                print(f"Ligne {Num_ligne+2} =  Client : '{Nom}', Montant souscrit 2024 : {MontantTotalSouscritAnneeCourante}")
                print(f"            Frais 1 (%, euros) : '{str(TypeFrais1_percent)}, {str(TypeFrais1_euros)}' // Frais 2 (%, euros) : '{str(TypeFrais2_percent)}, {str(TypeFrais2_euros)}' // Frais 3 (%, euros) : '{str(TypeFrais3_percent)}, {str(TypeFrais3_euros)}' \n")
                setter_data_fournisseur_norma(Prenom, Nom, TypeFrais1_euros, TypeFrais2_euros,TypeFrais3_euros, MontantTotalSouscritAnneeCourante, "M6")



# Récupère et intègre les personnes physiques
def get_PersonnesPhysiques(Fournisseur_doc):
    
    print("Colonnes disponibles :", Fournisseur_doc.columns.tolist())

    for index, row in Fournisseur_doc.iterrows():

        if pd.notna(row["Nom - Souscripteur"]):
            if ("total" not in str(row["Raison Sociale - Souscripteur"]).lower()):
                Num_ligne = index
                Nom = str(row["Nom - Souscripteur"]).upper().strip()
                
                if pd.notna(row["Prénom - Souscripteur"]):
                    Prenom = str(row["Prénom - Souscripteur"]).lower().capitalize().strip()
                else:
                    Prenom = ''

                MontantTotalSouscritAnneeCourante = row["Encours 2024"]

                TypeFrais1_percent = 0.0
                TypeFrais1_euros = row["Frais récurrent - 2024"] + row["Frais immobilier 2024"]
                TypeFrais2_percent = 0.0
                TypeFrais2_euros = row["Frais unique 2024"]
                TypeFrais3_percent = 0.0
                TypeFrais3_euros = row["Frais de transation 2024"]


                print(f"Ligne {Num_ligne+2} =  Client : '{Nom} {Prenom}', Montant souscrit 2024 : {MontantTotalSouscritAnneeCourante}")
                print(f"            Frais 1 (%, euros) : '{str(TypeFrais1_percent)}, {str(TypeFrais1_euros)}' // Frais 2 (%, euros) : '{str(TypeFrais2_percent)}, {str(TypeFrais2_euros)}' // Frais 3 (%, euros) : '{str(TypeFrais3_percent)}, {str(TypeFrais3_euros)}' \n")
                setter_data_fournisseur_norma(Prenom, Nom, TypeFrais1_euros, TypeFrais2_euros,TypeFrais3_euros, MontantTotalSouscritAnneeCourante, "M6")

