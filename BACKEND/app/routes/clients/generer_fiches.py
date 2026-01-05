from datetime import date
from flask import Flask, Blueprint, jsonify, make_response, request, current_app, send_file
from mysql.connector import Error
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity)

from app.BDD.database import get_Database_connection
from app.routes.clients.Classe_FicheReporting import Fiche_Reporting


GenererFiche_bp = Blueprint('generationFiche', __name__)
@GenererFiche_bp.route('/partenaire/fetch-pdf', methods = ['POST', 'OPTIONS'])
@jwt_required()
def fetchPDF():
    try:
        if request.method == 'OPTIONS':
            return '', 200 #requete preflight

        #token
        IDCollaborateur_user = get_jwt_identity()
        new_token = create_access_token(identity=IDCollaborateur_user)


        data = request.get_json()
        if not data:
            return jsonify({"error": "Aucune donnée JSON reçue"}), 400
        
        Groupe_recu = data.get('groupe')
        Fournisseur_recu = data.get('fournisseur')
        Entite_recu = data.get('entite')
        IDClient_recu = data.get('IDClient')
        IDFournisseur_recu = data.get('IDFournisseur')
        
        print(f"Groupe_recu : {Groupe_recu}, Fournisseur_recu : {Fournisseur_recu}, Entite_recu : {Entite_recu}, IDClient_recu : {IDClient_recu}, IDFournisseur_recu : {IDFournisseur_recu}")


        if any(x is None for x in [IDClient_recu, IDFournisseur_recu]):
            return jsonify({"message": "Tous les champs doivent être remplis"}), 400


        TablesClientsInsinia = {
            "ACTIONPATRIMOINE": "",
            "ALLUREFINANCE": "",
            "BCFINANCES": "",
            "CAPIUM": "",
            "FAMILYPATRIMOINE": "tfichier_clientinsinia_familypatrimoine",
            "FIPAGEST": "tfichier_clientastoria",
            "MYFAMILYOFFICER": "",
            "PARISII": "",
            "SOLVEPATRIMOINE": "",
            "SYNERGIECONSEILSPATRIMOINE": "tfichier_clientinsinia_synergieconseilspatrimoine",
            "WATSONPATRIMOINE": "tfichier_clientinsinia_watson",
        }

        if Groupe_recu == 'INSINIA':
            Table = TablesClientsInsinia[Entite_recu]
        elif Groupe_recu == 'ASTORIA':
            Table = "tfichier_clientastoria"


        conn = None
        cursor = None 

        try : 
            conn = get_Database_connection()
            if not conn:
                return jsonify({'message':'Erreur de connexion à la base de données'}),500

            cursor = conn.cursor(dictionary=True)

            if not Table:
                return jsonify({"error": "Entité inconnue"}), 400

            requete = ""
            requete = f"""
                        SELECT c.ID as IDClient, c.Nom as ClientNom, c.Prenom as ClientPrenom, c.Bureau as ClientBureau, c.Conseiller as ClientConseiller, c.Entreprise as ClientEntreprise,
                        c.EtablissementFournisseur as ProduitEtablissementFournisseur, c.TypeProduit as ProduitType, c.Produit as Produit, c.Intitule as ProduitIntitule, 
                        c.ID as IDClientProduit, c.NumeroCompte as ClientProduitNumCompte, DATE_FORMAT(c.DateOuverture, '%d/%m/%Y') as ClientProduitDateOuverture, 
                        replace(format(c.Compte_au_01_01_2024,2), ',', ' ') as ClientProduitCompte_01_01, replace(format(c.Compte_au_31_12_2024,2), ',', ' ') as ClientProduitCompte_31_12
                        FROM fraisexpost.{Table} c
                        WHERE c.ID = %s;
                    """


            cursor.execute(requete, (IDClient_recu, ))
            dataClient = cursor.fetchone()



            if dataClient:
                ClientNom = dataClient["ClientNom"]
                ClientPrenom = dataClient["ClientPrenom"]
                ClientProduitNumCompte = dataClient["ClientProduitNumCompte"]
                ClientEntreprise = dataClient["ClientEntreprise"]
                ClientBureau = dataClient["ClientBureau"]
                ClientConseiller = dataClient["ClientConseiller"]
                Produit = dataClient["Produit"]
                DateDuJour = str(date.today().strftime('%d/%m/%Y'))
                Signature = "SIGNATURE"

                ProduitIntitule = dataClient["ProduitIntitule"]
                ProduitEtablissementFournisseur = dataClient["ProduitEtablissementFournisseur"]
                ClientProduitDateOuverture = dataClient["ClientProduitDateOuverture"]
                ClientProduitNumCompte = dataClient["ClientProduitNumCompte"]
                ClientProduitCompte_31_12 = dataClient["ClientProduitCompte_31_12"]

               
                
                Nouvelle_Fiche = Fiche_Reporting(Groupe_recu, Entite_recu, Fournisseur_recu, ClientNom, ClientPrenom, ClientProduitNumCompte, ClientEntreprise, ClientBureau, ClientConseiller, 
                                                ProduitIntitule, ProduitEtablissementFournisseur, ClientProduitDateOuverture, ClientProduitNumCompte, Produit, 
                                                ClientProduitCompte_31_12, ClientBureau, DateDuJour, Signature, IDFournisseur_recu)
                

                doc = Nouvelle_Fiche.Processus()
                
                # Impossible de transmettre le token avec un send file, 
                # Donc on encapsule le fichier à envoyer et un en-tête qui contiendra le token qui doit être envoyé
                # Et on autorise le frontend à avoir accès à la variable placé dans le header
                reponse = make_response(send_file( doc, mimetype='application/pdf', as_attachment=False, download_name='Fiche_Reporting.pdf'))
                reponse.headers["Access-Control-Expose-Headers"] = "X-new-access-token"
                reponse.headers["X-new-access-token"] = new_token
                return reponse
                
            else:
                return jsonify({"message" : "Échec génération de la fiche"}),400


        finally: 
            if cursor :
                cursor.close()
            if conn:
                conn.close()

    except Error as e:
        return jsonify({"message": "Erreur lors de la récupération de données de la base", "erreur": str(e)}), 500
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"message": "Erreur inattendue", "erreur": str(e)}), 500



