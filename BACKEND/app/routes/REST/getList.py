from flask import  Blueprint, jsonify, request
from mysql.connector import Error
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity)

from app.BDD.database import get_Database_connection

#Récupère tous les formateurs occasionnels ou externes à l'entreprise
ProduitsAlpheys_bp = Blueprint('produitsAlpheys', __name__)
@ProduitsAlpheys_bp.route('/REST/liste/produitsAlpheys', methods=['OPTIONS', 'POST'])
def GetList_ProduitsAlpheys():
    try:
        if request.method == 'OPTIONS':
            return '', 200 #requete preflight

        data = request.get_json()
        if not data:
            return jsonify({"error": "Aucune donnée JSON reçue"}), 400
        
        Groupe_recu = data.get('groupe')


        conn = get_Database_connection()
        cursor = conn.cursor()


        if Groupe_recu == 'ASTORIA':
            requete = ('SELECT * FROM fraisexpost.tfournisseur_alpheys where ApparaitAstoria = true order by nomproduit asc')
        
        elif Groupe_recu == 'INSINIA':
            requete = ('SELECT * FROM fraisexpost.tfournisseur_alpheys where ApparaitInsinia = true order by nomproduit asc')


        cursor.execute(requete)

        Produits = cursor.fetchall()
        conn.close()


        #si la liste retournée est vide
        if not Produits:
            jsonify({"error":"Impossible de retourner la liste, elle est vide"}), 401
        else:
            Produits_Liste = [
                {"ID" : prod[0], "NomProduit" : prod[5]}
                for prod in Produits
            ]


        return jsonify({"produits_liste" : Produits_Liste}), 200
    
    except Error as e:
        return jsonify({"message": "Erreur lors de la récupération de données de la base", "erreur": str(e)}), 500
    
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({"message": "Erreur inattendue", "erreur": str(e)}), 500