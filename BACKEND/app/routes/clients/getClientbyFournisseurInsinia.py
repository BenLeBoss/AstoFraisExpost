import traceback

from flask import Flask, Blueprint, jsonify, request, current_app
from app.BDD.database import get_Database_connection
from mysql.connector import Error
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity)

from app.routes.clients.getRequeteSQLFournisseurInsinia import getRequeteSQLFournisseurInsinia

getClientbyFournisseurInsinia_bp = Blueprint('getClientbyFournisseurInsinia', __name__)
@getClientbyFournisseurInsinia_bp.route('/partenaireinsinia', methods = ['POST', 'OPTIONS'])
@jwt_required()
def getClient_by_Fournisseur_Insinia():
    try:
        if request.method == 'OPTIONS':
            return '', 200 #requete preflight

        #token
        IDCollaborateur_user = get_jwt_identity()
        new_token = create_access_token(identity=IDCollaborateur_user)


        data = request.get_json()
        if not data:
            return jsonify({"message": "Aucune donnée JSON reçue"}), 400
        
        Entite_recu = data.get('entite')
        Partenaire_recu = data.get('partenaire')
        IDProduitAlpheys = data.get('idproduitalpheys')

        print(f"Entité : {Entite_recu}, Partenaire : {Partenaire_recu}, IDProduitAlpheys : {IDProduitAlpheys}")

        if Entite_recu is None:
            return jsonify({"message": "Le champs est vide"}), 400


        Tables = {
            'WATSONPATRIMOINE' : { 
                    'Table' : 'tfichier_clientinsinia_watson'
            },
            'FIPAGEST' : { 
                    'Table' : 'tfichier_clientastoria'
            },
            'SYNERGIECONSEILSPATRIMOINE' : { 
                    'Table' : 'tfichier_clientinsinia_synergieconseilspatrimoine'
            },
            'FAMILYPATRIMOINE' : { 
                    'Table' : 'tfichier_clientinsinia_familypatrimoine'
            },
            
    
        }

        if Entite_recu not in Tables:
            return jsonify({'message': 'Fournisseur inconnu'}), 400

        Table_courante = Tables[Entite_recu]['Table']

        conn = None
        cursor = None

        try : 
            conn = get_Database_connection()
            if not conn:
                return jsonify({'message':'Erreur de connexion à la base de données'}),500

            cursor = conn.cursor(dictionary=True)

            # récupère la requete correspondante
            requete = getRequeteSQLFournisseurInsinia(Table_courante, Partenaire_recu)

            if Partenaire_recu != 'ALPHEYS':
                cursor.execute(requete, (Partenaire_recu,))  
            else:
                if (IDProduitAlpheys is not None):
                    cursor.execute(requete, (Partenaire_recu,IDProduitAlpheys, )) 


            clients = cursor.fetchall()
        
        finally: 
            if cursor :
                cursor.close()
            if conn:
                conn.close()

        if not clients:
            return jsonify({'error': 'table_vide', 'message': 'La table est vide et aucun client à afficher'}),400
            
        clients_liste = [
            {"IDClient": client["IDClient"], "Nom": client["ClientNom"], "Prenom": client["ClientPrenom"], 
             "Region": client["ClientRegion"].lower().replace("region ", "").upper() if 'region' in client["ClientRegion"].lower() else client["ClientRegion"].upper(), 
             "Bureau": client["ClientBureau"].lower().replace("bureau ", "").title() if 'bureau' in client["ClientBureau"].lower() else client["ClientBureau"], 
             "Conseiller": client["ClientConseiller"], "EtablissementFournisseur": client["ProduitEtablissementFournisseur"], 
             "TypeProduit": client["ProduitTypeProduit"], "ProduitClient": client["ProduitProduit"], "Intitule": client["ProduitIntitule"], 
             "NumeroCompte": client["ClientProduitNumeroCompte"], "DateOuverture": client["ClientProduitDateOuverture"], 
             "Compte_au_01_01_2024": str(client["ClientProduitCompte_01_01"]) + ' €', "Compte_au_31_12_2024": str(client["ClientProduitCompte_31_12"])+ ' €', 
             "EstGenereFournisseur": client["FournisseurEstGenere"], "EstGenereClient": client["ClientEstGenere"], "IDFournisseur": client["IDFournisseur"], 
             "ProduitFournisseur" : client["FournisseurNomProduit"], "FournisseurMontantTotalSouscrit": str(client["FournisseurMontantTotalSouscrit"])+ ' €'}
            for client in clients
        ]


        # tri par ID 
        clients_liste = sorted(clients_liste, key=lambda x: x["IDClient"])

        return jsonify({"client_liste" : clients_liste,  "new_access_token" :new_token}), 200

    except Error as e:
        traceback.print_exc()
        return jsonify({"message": "Erreur lors de la récupération de données de la base", "erreur": str(e)}), 500
    
    except Exception as e:
        return jsonify({"message": "Erreur inattendue", "erreur": str(e)}), 500