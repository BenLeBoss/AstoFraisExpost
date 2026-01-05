from flask import Flask, Blueprint, jsonify, request, current_app
from app.BDD.database import get_Database_connection
from mysql.connector import Error
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity)


set_ClientProduit_EstGenereInsinia_bp = Blueprint('setClientProduitEstGenereInsinia', __name__)
@set_ClientProduit_EstGenereInsinia_bp.route('/client/fiche_EstGenereeInsinia', methods = ['PATCH', 'OPTIONS'])
@jwt_required()
def set_ClientProduit_EstGenereInsinia():
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
        Entite_recu = data.get('entite')

        if IDClient_recu is None:
            return jsonify({"message": "Le champs requis est vide"}), 400


        Tables_ClientsInsinia = {
            "ACTIONPATRIMOINE": "tfichier_clientinsinia_actionpatrimoine",
            "ALLUREFINANCE": "tfichier_clientinsinia_allurefinance",
            "BCFINANCES": "tfichier_clientinsinia_bcfinances",
            "CAPIUM": "tfichier_clientinsinia_capium",
            "FAMILYPATRIMOINE": "tfichier_clientinsinia_familypatrimoine",
            "FIPAGEST": "tfichier_clientastoria",
            "MYFAMILYOFFICER": "tfichier_clientinsinia_myfamilyofficer",
            "PARISII": "tfichier_clientinsinia_parisii",
            "SOLVEPATRIMOINE": "tfichier_clientinsinia_solvepatrimoine",
            "SYNERGIECONSEILSPATRIMOINE": "tfichier_clientinsinia_synergieconseilspatrimoine",
            "WATSONPATRIMOINE": "tfichier_clientinsinia_watson"
        }

        conn = None
        cursor = None

        Table = Tables_ClientsInsinia[Entite_recu]
        if not Table:
            return jsonify({'message':'Erreur de table pour les entités'}),400

        
        print(f"Entite: {Entite_recu}")
        print(f"Table: {Table}")
        print(f"IDClient_recu: {IDClient_recu}")

        try : 
            conn = get_Database_connection()
            if not conn:
                return jsonify({'message':'Erreur de connexion à la base de données'}),500

            cursor = conn.cursor()

            
            requete = f"""
                        UPDATE fraisexpost.{Table} SET EstGenere = true WHERE id = %s;
                    """

            cursor.execute(requete, (IDClient_recu,))
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
    





set_AllClientsProduit_EstGenereInsinia_bp = Blueprint('setAllClientsProduitEstGenereInsinia', __name__)
@set_AllClientsProduit_EstGenereInsinia_bp.route('/client/allfiches_EstGenereeInsinia', methods = ['PATCH', 'OPTIONS'])
@jwt_required()
def set_AllClientsProduit_EstGenereInsinia():
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
        Entite_recu = data.get('entite')

        if TabIDClient_recu is None:
            return jsonify({"message": "Le champs requis est vide"}), 400


        Tables_ClientsInsinia = {
            "ACTIONPATRIMOINE": "tfichier_clientinsinia_actionpatrimoine",
            "ALLUREFINANCE": "tfichier_clientinsinia_allurefinance",
            "BCFINANCES": "tfichier_clientinsinia_bcfinances",
            "CAPIUM": "tfichier_clientinsinia_capium",
            "FAMILYPATRIMOINE": "tfichier_clientinsinia_familypatrimoine",
            "FIPAGEST": "tfichier_clientastoria",
            "MYFAMILYOFFICER": "tfichier_clientinsinia_myfamilyofficer",
            "PARISII": "tfichier_clientinsinia_parisii",
            "SOLVEPATRIMOINE": "tfichier_clientinsinia_solvepatrimoine",
            "SYNERGIECONSEILSPATRIMOINE": "tfichier_clientinsinia_synergieconseilspatrimoine",
            "WATSONPATRIMOINE": "tfichier_clientinsinia_watson"
        }

        conn = None
        cursor = None

        Table = Tables_ClientsInsinia[Entite_recu]
        if not Table:
            return jsonify({'message':'Erreur de table pour les entités'}),400


        try : 
            conn = get_Database_connection()
            if not conn:
                return jsonify({'message':'Erreur de connexion à la base de données'}),500

            cursor = conn.cursor()

            for IDClient in TabIDClient_recu:

                requete = f"""
                            UPDATE fraisexpost.{Table} SET EstGenere = true WHERE id = %s;
                        """
                cursor.execute(requete, (IDClient,))
                
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