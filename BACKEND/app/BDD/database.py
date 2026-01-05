import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def get_Database_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            port=int(os.getenv("DB_PORT", 3306)),
            database=os.getenv("DB_DATABASE"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )

        if connection.is_connected():
            #print("Connexion réussie à la base de données MySQL")
            return connection

    except Error as e:
        print("Erreur de connexion à MySQL :", e)

    return None