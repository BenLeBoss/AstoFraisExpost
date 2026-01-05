import datetime

from flask import Blueprint, jsonify, request
from app.BDD.database import get_Database_connection
from mysql.connector import Error

def audits_authentification(conn, IDCollaborateur, Statut, infosIP):
    
    try:
        DateHeure = datetime.datetime.now()
        if infosIP :
            AdresseIP_Publique = infosIP.get('ip')
            Ville = infosIP.get('city')
            Pays = infosIP.get('country_name')
            Org = infosIP.get('org')
        else:
            AdresseIP_Publique = ""
            Ville = ""
            Pays = ""
            Org = ""


        cursor = conn.cursor()

        requete = """
                    INSERT INTO fraisexpost.taudits_authentification 
                    (IDCollaborateur, DateHeureConnexion, AdresseIP_Publique, Statut, Ville, Pays, Org)
                    VALUES (%s,%s,%s,%s,%s,%s,%s);
                """
        valeurs = (IDCollaborateur, DateHeure, AdresseIP_Publique, Statut, Ville, Pays, Org)

        cursor.execute(requete, valeurs)
        conn.commit()

    except Exception as e:
        print("Erreur lors de la création d'audits :", e)
        raise

    finally:
        cursor.close()