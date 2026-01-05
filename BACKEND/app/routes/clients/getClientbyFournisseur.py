import traceback

from flask import Flask, Blueprint, jsonify, request, current_app
from app.BDD.database import get_Database_connection
from mysql.connector import Error
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity)

from app.routes.clients.getRequeteSQLFournisseur import getRequeteSQLFournisseur

getClientbyFournisseur_bp = Blueprint('getClientbyFournisseur', __name__)
@getClientbyFournisseur_bp.route('/partenaire', methods = ['POST', 'OPTIONS'])
@jwt_required()
def getClient_by_Fournisseur():
    try:
        if request.method == 'OPTIONS':
            return '', 200 #requete preflight

        #token
        IDCollaborateur_user = get_jwt_identity()
        new_token = create_access_token(identity=IDCollaborateur_user)


        data = request.get_json()
        if not data:
            return jsonify({"message": "Aucune donnée JSON reçue"}), 400
        
        Fournisseur_Recu = data.get('fournisseur')
        IDProduitAlpheys = data.get('idproduitalpheys')


        if Fournisseur_Recu is None:
            return jsonify({"message": "Le champs est vide"}), 400


        Tables = {
            'ALPHEYS': {
                'Table': 'tfournisseur_alpheys'
            },
            #'ATLAND VOISIN': {
            #    'Table': 'tfournisseur_atlandvoisin'
            #},
            'ATLAND VOISIN': {
                'Table': 'tfournisseur_atlandvoisin2'
            },
            'CORUM L\'EPARGNE': {
                'Table': 'tfournisseur_corum'
            },
            'EIFFEL INVESTMENT GROUP': {
                'Table': 'tfournisseur_eiffel'
            },
            'FRANCE VALLEY INVESTISSEMENTS': {
                'Table': 'tfournisseur_francevalley'
            },
            'KEYSAM': {
                'Table': 'tfournisseur_keys'
            },
            'LAFRANCAISEAM': {
                'Table': 'tfournisseur_lafrancaise'
            },
            'NORMA CAPITAL': {
                'Table': 'tfournisseur_normacapital'
            },
            'PERIAL ASSET MANAGEMENT': {
                'Table': 'tfournisseur_perial'
            },
            'SMALT CAPITAL': {
                'Table': 'tfournisseur_smaltcapital'
            },
            'SOFIDY': {
                'Table': 'tfournisseur_sofidy'
            },
            'THEOREIM': {
                'Table': 'tfournisseur_theoreim'
            },
            'URBAN PREMIUM': {
                'Table': 'tfournisseur_urbanpremium'
            },
            'VATELCAPITAL': {
                'Table': 'tfournisseur_vatel'
            },
            'PAREF': {
                'Table': 'tfournisseur_paref'
            },
            'PRIMONIAL': {
                'Table': 'tfournisseur_primonial'
            },
        }

        if Fournisseur_Recu not in Tables:
            return jsonify({'message': 'Fournisseur inconnu'}), 400

        Table_courante = Tables[Fournisseur_Recu]['Table']

        conn = None
        cursor = None

        try : 
            conn = get_Database_connection()
            if not conn:
                return jsonify({'message':'Erreur de connexion à la base de données'}),500

            cursor = conn.cursor(dictionary=True)

            # récupère la requete correspondante
            requete = getRequeteSQLFournisseur(Table_courante)


            if Fournisseur_Recu != 'ALPHEYS':
                cursor.execute(requete) 
            else:
                if (IDProduitAlpheys is not None):
                    cursor.execute(requete,(IDProduitAlpheys,))            
            
            clients = cursor.fetchall()
        
        finally: 
            if cursor :
                cursor.close()
            if conn:
                conn.close()

        if not clients:
            return jsonify({'message': 'Aucun client à afficher'}),400
            
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