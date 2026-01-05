from flask import Blueprint, jsonify, request
from app.BDD.database import get_Database_connection
from mysql.connector import Error
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity)

from app.routes.audits.audit_authentification import audits_authentification

# Création du blueprint
auth_bp = Blueprint('auth', __name__)

# Définition d'une route dans ce blueprint
@auth_bp.route('/auth', methods=['POST', 'OPTIONS'])
def auth():
    try:

        if request.method == 'OPTIONS':
            return '', 200 #requete preflight
        
        data = request.get_json()
        if not data:
            return jsonify({"message": "Aucune donnée JSON reçue"}), 400
        
        Identifiant_Recu = data.get('username')
        MDP_Recu = data.get('password')
        infosIP_recu = data.get('infosIP')


        if any(x is None for x in [Identifiant_Recu, MDP_Recu]):
            return jsonify({"error": "Tous les champs sont requis"}), 400


        conn = None
        cursor = None

        try :     

            conn = get_Database_connection()
            if not conn:
                return jsonify({"message" : "Erreur de connexion à la base de données"}),500
            

            cursor = conn.cursor()
            requete = "SELECT * FROM `tcollaborateur` WHERE mail = %s and MDP_Outils = %s"
            cursor.execute(requete, (Identifiant_Recu, MDP_Recu))
            
            utilisateur = cursor.fetchone()
            

            #enregistre l'utilisateur qui se connecte
            if utilisateur:
                IdCollaborateur = str(utilisateur[0])
                Statut = 'RÉUSSITE'
            else:
                IdCollaborateur = 0
                Statut = 'ÉCHEC'
                
            audits_authentification(conn, IdCollaborateur, Statut, infosIP_recu)

        finally: 
                if cursor :
                    cursor.close()
                if conn:
                    conn.close()

        if utilisateur:
            access_token = create_access_token(identity=IdCollaborateur)
            print(access_token)
            return jsonify({"message" : "Connexion réussie", "IDCollaborateur" : str(utilisateur[0]), "access_token" : access_token}),200
        else:
            return jsonify({"message" : "Identifiants invalides"}),400

    except Error as e:
        return jsonify({"message": "Erreur lors de la récupération de données de la base", "erreur": str(e)}), 500

    except Exception as e:
        return jsonify({"message": "Erreur inattendue", "erreur": str(e)}), 500
