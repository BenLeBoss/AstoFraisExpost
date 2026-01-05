from flask import Flask, Blueprint, jsonify, request, current_app
from app.BDD.database import get_Database_connection
from mysql.connector import Error
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity)



test_bp = Blueprint('test', __name__)
@test_bp.route('/test', methods = ['GET', 'OPTIONS'])
@jwt_required()
def test_collab():
    try:
        if request.method == 'OPTIONS':
            return '', 200 #requete preflight

        #token
        IDCollaborateur_user = get_jwt_identity()
        new_token = create_access_token(identity=IDCollaborateur_user)


        conn = None
        cursor = None

        try : 
            conn = get_Database_connection()
            if not conn:
                return jsonify({'error':'Erreur de connexion à la base de données'}),500

            cursor = conn.cursor()
            #requête composée
            requete = """
                        select c.ID, c.description, c.nom, c.prenom, c.fonctiondescription, c.niveau, c.mail, c.estparti, c.idagence, a.description 
                        from tcollaborateur c, tagence a 
                        where c.EstParti = false
                        AND c.IDAgence = a.ID
                        AND c.ID in (1, 2,3,4,5,6,7,8,9)
                    """
            cursor.execute(requete)
            collaborateurs = cursor.fetchall()
        
        finally: 
            if cursor :
                cursor.close()
            if conn:
                conn.close()

        if not collaborateurs:
            return jsonify({'error':'Impossible de récupérer la liste des collaborateurs'}),400
            
        collaborateurs_liste = [
            {"ID": collab[0], "Description": collab[1], "Nom": collab[2], "Prenom": collab[3], "FonctionDescription": collab[4], "Niveau": collab[5], "Mail": collab[6], "EstParti": collab[7], "IDAgence": collab[8], "DescriptionAgence": collab[9]}
            for collab in collaborateurs
        ]
        return jsonify({"collaborateurs_liste": collaborateurs_liste,  "new_access_token" :new_token}), 200

    except Error as e:
        return jsonify({"message": "Erreur lors de la récupération de données de la base", "erreur": str(e)}), 500
    
    except Exception as e:
        return jsonify({"message": "Erreur inattendue", "erreur": str(e)}), 500