import os
from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import (JWTManager)
from datetime import timedelta
from dotenv import load_dotenv


# ASTORIA FINANCE
from app.routes.authentification.auth import auth_bp
from app.routes.clients.getClientbyFournisseur import getClientbyFournisseur_bp
from app.routes.clients.generer_fiches import GenererFiche_bp
from app.routes.clients.set_ClientProduit_EstGenere import set_ClientProduit_EstGenere_bp, set_AllClientsProduit_EstGenere_bp
from app.routes.clients.getClientFicheGeneree import getClientFicheGeneree_bp
from app.routes.clients.getClientFicheGeneree import getClientFicheNonGeneree_bp


# INSINIA
from app.routes.clients.getClientbyFournisseurInsinia import getClientbyFournisseurInsinia_bp
from app.routes.clients.set_ClientProduit_EstGenereInsinia import set_ClientProduit_EstGenereInsinia_bp, set_AllClientsProduit_EstGenereInsinia_bp
from app.routes.clients.getClientFicheGenereeInsinia import getClientFicheGenereeInsinia_bp
from app.routes.clients.getClientFicheGenereeInsinia import getClientFicheNonGenereeInsinia_bp


# REST
from app.routes.REST.getList import ProduitsAlpheys_bp


from app.routes.clients.test import test_bp

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config["DEBUG"] = True
    
    #accéder les communications venant du frontend VITE
    CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}}, supports_credentials=True)


    #paramétrage des sessions avec la clé secrète, le temps avant l'expiration du token, et l'initialisation de JWT
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=20)
    JWTManager(app)

    print("Clé JWT chargée :", app.config['JWT_SECRET_KEY'])


    #authentification
    app.register_blueprint(auth_bp, url_prefix="/api")

    #client 
    app.register_blueprint(getClientbyFournisseur_bp, url_prefix="/api")
    app.register_blueprint(GenererFiche_bp, url_prefix="/api")
    app.register_blueprint(set_ClientProduit_EstGenere_bp, url_prefix="/api")
    app.register_blueprint(set_AllClientsProduit_EstGenere_bp, url_prefix="/api")
    app.register_blueprint(getClientFicheGeneree_bp, url_prefix="/api")
    app.register_blueprint(getClientFicheNonGeneree_bp, url_prefix="/api")


    app.register_blueprint(getClientbyFournisseurInsinia_bp, url_prefix="/api")
    app.register_blueprint(set_ClientProduit_EstGenereInsinia_bp, url_prefix="/api")
    app.register_blueprint(set_AllClientsProduit_EstGenereInsinia_bp, url_prefix="/api")
    app.register_blueprint(getClientFicheGenereeInsinia_bp, url_prefix="/api")
    app.register_blueprint(getClientFicheNonGenereeInsinia_bp, url_prefix="/api")
    
   
    app.register_blueprint(ProduitsAlpheys_bp, url_prefix="/api")


    #test session
    app.register_blueprint(test_bp, url_prefix="/api")

    return app