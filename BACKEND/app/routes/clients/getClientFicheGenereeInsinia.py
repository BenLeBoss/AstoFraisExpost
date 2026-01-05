from flask import Flask, Blueprint, jsonify, request, current_app
from app.BDD.database import get_Database_connection
from mysql.connector import Error
from flask_jwt_extended import (JWTManager, create_access_token, jwt_required, get_jwt_identity)


getClientFicheGenereeInsinia_bp = Blueprint('getClientFicheGenereeInsinia', __name__)
@getClientFicheGenereeInsinia_bp.route('/client/consultation/fichesgenereesinsinia', methods = ['POST', 'OPTIONS'])
@jwt_required()
def getClient_FicheGeneree_INSINIA():
    try:
        if request.method == 'OPTIONS':
            return '', 200 #requete preflight

        #token
        IDCollaborateur_user = get_jwt_identity()
        new_token = create_access_token(identity=IDCollaborateur_user)

        data = request.get_json()
        if not data:
            return jsonify({"error": "Aucune donnée JSON reçue"}), 400
        
        Entite_Recu = data.get('entite')

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

        Table = Tables_ClientsInsinia[Entite_Recu]
        if not Table:
            return jsonify({'message':'Erreur de table pour les entités'}),400

        try : 
            conn = get_Database_connection()
            if not conn:
                return jsonify({'message':'Erreur de connexion à la base de données'}),500

            cursor = conn.cursor(dictionary=True)

            requete = ""
            if Entite_Recu != "FIPAGEST":
                requete = f"""
                        select  c.ID as IDClient, c.Nom as ClientNom, c.Prenom as ClientPrenom, c.NumeroCompte as ClientNumCompte, c.EtablissementFournisseur as FournisseurNom,
                                c.Produit FournisseurProduit, c.Compte_au_31_12_2024 as ClientCompte_31_12 
                        from {Table} c
                        where c.EstGenere = True
                        order by c.Nom;
                        """
            else:
                requete = f"""
                        select  c.ID as IDClient, c.Nom as ClientNom, c.Prenom as ClientPrenom, c.NumeroCompte as ClientNumCompte, c.EtablissementFournisseur as FournisseurNom,
                                c.Produit FournisseurProduit, c.Compte_au_31_12_2024 as ClientCompte_31_12 
                        from {Table} c
                        where c.EstGenere = True
                        and bureau = 'FIPAGEST'
                        order by c.Nom;
                        """


            cursor.execute(requete)
            clients = cursor.fetchall()
            
        finally: 
            if cursor :
                cursor.close()
            if conn:
                conn.close()

        if not clients:
            return jsonify({'message': 'Aucun client à afficher'}),400
            
        clients_liste = [
            {"IDClient": client["IDClient"], "Nom": client["ClientNom"], "Prenom": client["ClientPrenom"], "EtablissementFournisseur": client["FournisseurNom"], 
                "Produit": client["FournisseurProduit"], "NumeroCompte": client["ClientNumCompte"], 
                "Compte_au_31_12_2024": format(client["ClientCompte_31_12"], ',.2f').replace(',', ' ') + ' €'}
            for client in clients
        ]

        # tri par ordre alphabétique sur le nom
        clients_liste = sorted(clients_liste, key=lambda x: x["Nom"].lower())

        return jsonify({"client_liste" : clients_liste,  "new_access_token" :new_token}), 200

    except Error as e:
        return jsonify({"message": "Erreur lors de la récupération de données de la base", "erreur": str(e)}), 500
    
    except Exception as e:
        return jsonify({"message": "Erreur inattendue", "erreur": str(e)}), 500





getClientFicheNonGenereeInsinia_bp = Blueprint('getClientFicheNonGenereeInsinia', __name__)
@getClientFicheNonGenereeInsinia_bp.route('/client/consultation/fichesnongenereesinsinia', methods = ['POST', 'OPTIONS'])
@jwt_required()
def getClient_FicheNonGeneree_INSINIA():
    try:
        if request.method == 'OPTIONS':
            return '', 200 #requete preflight

        #token
        IDCollaborateur_user = get_jwt_identity()
        new_token = create_access_token(identity=IDCollaborateur_user)

        data = request.get_json()
        if not data:
            return jsonify({"error": "Aucune donnée JSON reçue"}), 400
        
        Entite_Recu = data.get('entite')

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

        Table = Tables_ClientsInsinia[Entite_Recu]
        if not Table:
            return jsonify({'message':'Erreur de table pour les entités'}),400

        try : 
            conn = get_Database_connection()
            if not conn:
                return jsonify({'message':'Erreur de connexion à la base de données'}),500

            cursor = conn.cursor(dictionary=True)


            requete = ""
            if Entite_Recu != "FIPAGEST":
                requete = f"""
                        select  c.ID as IDClient, c.Nom as ClientNom, c.Prenom as ClientPrenom, c.NumeroCompte as ClientNumCompte, c.EtablissementFournisseur as FournisseurNom,
                                c.Produit FournisseurProduit, c.Compte_au_31_12_2024 as ClientCompte_31_12 
                        from {Table} c
                        where c.EstGenere = False
                        order by c.Nom;
                        """
            else:
                requete = f"""
                        select  c.ID as IDClient, c.Nom as ClientNom, c.Prenom as ClientPrenom, c.NumeroCompte as ClientNumCompte, c.EtablissementFournisseur as FournisseurNom,
                                c.Produit FournisseurProduit, c.Compte_au_31_12_2024 as ClientCompte_31_12 
                        from {Table} c
                        where c.EstGenere = False
                        and bureau = 'FIPAGEST'
                        order by c.Nom;
                        """
            
            print(requete)
            print(f"Table : {Table}")

            cursor.execute(requete)
            clients = cursor.fetchall()
            
        finally: 
            if cursor :
                cursor.close()
            if conn:
                conn.close()

        if not clients:
            return jsonify({'message': 'Aucun client à afficher'}),400
            
        clients_liste = [
            {"IDClient": client["IDClient"], "Nom": client["ClientNom"], "Prenom": client["ClientPrenom"], "EtablissementFournisseur": client["FournisseurNom"], 
                "Produit": client["FournisseurProduit"], "NumeroCompte": client["ClientNumCompte"], 
                "Compte_au_31_12_2024": format(client["ClientCompte_31_12"], ',.2f').replace(',', ' ') + ' €'}
            for client in clients
        ]

        # tri par ordre alphabétique sur le nom
        clients_liste = sorted(clients_liste, key=lambda x: x["Nom"].lower())

        return jsonify({"client_liste" : clients_liste,  "new_access_token" :new_token}), 200

    except Error as e:
        return jsonify({"message": "Erreur lors de la récupération de données de la base", "erreur": str(e)}), 500
    
    except Exception as e:
        return jsonify({"message": "Erreur inattendue", "erreur": str(e)}), 500