from flask import Flask, Blueprint, jsonify, request, current_app
from app.BDD.database import get_Database_connection
from mysql.connector import Error
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity)


set_ClientProduit_EstGenere_bp = Blueprint('setClientProduitEstGenere', __name__)
@set_ClientProduit_EstGenere_bp.route('/client/fiche_EstGeneree', methods = ['PATCH', 'OPTIONS'])
@jwt_required()
def set_ClientProduit_EstGenere():
    try:
        if request.method == 'OPTIONS':
            return '', 200 #requete preflight

        #token
        IDCollaborateur_user = get_jwt_identity()
        new_token = create_access_token(identity=IDCollaborateur_user)


        data = request.get_json()
        if not data:
            return jsonify({"message": "Aucune donnée JSON reçue"}), 400
        
        IDClient_recu = data.get('IDClient')
        Fournisseur_recu = data.get('Fournisseur')

        if IDClient_recu is None:
            return jsonify({"message": "Le champs requis est vide"}), 400

        conn = None
        cursor = None

        try : 
            conn = get_Database_connection()
            if not conn:
                return jsonify({'message':'Erreur de connexion à la base de données'}),500

            cursor = conn.cursor()
            
            requeteClient = f"""
                        UPDATE fraisexpost.tfichier_clientastoria SET EstGenere = true WHERE id = %s;
                    """

            cursor.execute(requeteClient, (IDClient_recu,))
            conn.commit()
        
        finally: 
            if cursor :
                cursor.close()
            if conn:
                conn.close()

        return jsonify({"new_access_token" :new_token}), 200

    except Error as e:
        return jsonify({"message": "Erreur lors de la récupération de données de la base", "erreur": str(e)}), 500
    
    except Exception as e:
        return jsonify({"message": "Erreur inattendue", "erreur": str(e)}), 500
    



set_AllClientsProduit_EstGenere_bp = Blueprint('setAllClientsProduitEstGenere', __name__)
@set_AllClientsProduit_EstGenere_bp.route('/client/allfiches_EstGeneree', methods = ['PATCH', 'OPTIONS'])
@jwt_required()
def set_AllClientsProduit_EstGenere():
    try:
        if request.method == 'OPTIONS':
            return '', 200 #requete preflight

        #token
        IDCollaborateur_user = get_jwt_identity()
        new_token = create_access_token(identity=IDCollaborateur_user)


        data = request.get_json()
        if not data:
            return jsonify({"message": "Aucune donnée JSON reçue"}), 400
        
        TabIDClient_recu = data.get('tabIDClient')

        if TabIDClient_recu is None:
            return jsonify({"message": "Le champs requis est vide"}), 400

        conn = None
        cursor = None

        try : 
            conn = get_Database_connection()
            if not conn:
                return jsonify({'message':'Erreur de connexion à la base de données'}),500

            cursor = conn.cursor()
            
            for IDClient in TabIDClient_recu:
                requeteClient = f"""
                            UPDATE fraisexpost.tfichier_clientastoria SET EstGenere = true WHERE id = %s;
                        """

                cursor.execute(requeteClient, (IDClient,))

            conn.commit()
        
        finally: 
            if cursor :
                cursor.close()
            if conn:
                conn.close()

        return jsonify({"new_access_token" :new_token}), 200

    except Error as e:
        return jsonify({"message": "Erreur lors de la récupération de données de la base", "erreur": str(e)}), 500
    
    except Exception as e:
        return jsonify({"message": "Erreur inattendue", "erreur": str(e)}), 500