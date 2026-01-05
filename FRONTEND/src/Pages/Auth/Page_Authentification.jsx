import { useEffect, useState , useContext} from 'react';
import { useNavigate, useSearchParams} from 'react-router-dom';
import axios from 'axios';

import IconUser from '../../medias/img/user.svg'
import IconPW from '../../medias/img/lock.svg'
import IconEyeShow from '../../medias/img/eye_show.svg'
import IconEyeOff from '../../medias/img/eye_off.svg'
import LogoAstoria from '../../medias/img/Astoria.png'

import { AuthContext } from '../../Session/AuthContext';
import '../../index.css'

function Authentif() {

  //Le useState est un hook en React, il mémorise une valeur dans un composant et le met à jour
  const [identifiant, setIdentifiant] = useState('');
  const [mdp, setMotDePasse] = useState('');


  //création d'un token à la connexion
  const { login } = useContext(AuthContext);
  const [TimeOut, setTimeOut] = useState(false);


  //hook React, permet de naviguer vers une autre page
  const navigate = useNavigate();

  //récupère les paramètres dans l'url de la page qui contient l'id collaborateur
  const [searchParams] = useSearchParams();

  //récupère l'adresse IP publique d'un utilisateur
  const [InfosIP, setInfosIP] = useState('');


  useEffect(() => {

      const fetchIP = async () => {
          try {
              const response = await axios.get('https://ipapi.co/json');
              //console.log(response);
              setInfosIP(response.data);
          } catch (error) {
              console.error('Erreur lors de la récupération de l\'IP :', error);
              setInfosIP("");
          }
      };

      fetchIP()


      //si le paramètre existe dans l'url on affiche le timeout
      if (searchParams.get('timeout'))
        setTimeOut(true);

  }, [])



  //La fonction handleSubmit est appelé lors du clic sur un bouton de type submit, ici le bouton se connecter
  const handleSubmit = async (e) => {
    
    //Empêche le rechargement de la page
    e.preventDefault();

    try {
      //fetch est une fonction javascript native qui permet d'envoyer une requête HTTP, ici une requete POST puisqu'on envoie des données
      //le headers contient le type de contenu
      //le body contient les données à envoyer
      const res = await fetch('/api/auth', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ 
          username : identifiant, 
          password : mdp, 
          infosIP: InfosIP
        })
      });

      //Permet de décoder la réponse reçue envoyé par Flask via jsonify
      const data = await res.json();

      //en fonction de la réponse du backend Flask, si la connexion est réussi il renverra
      //le nombre 200 et un texte si la requête est réussie
      //le nombre 401 et un texte si l'utilisateur n'est pas authentifié
      if (res.ok) {
        login(data.access_token);

        const param = new URLSearchParams({id : data.IDCollaborateur});
        navigate(`/menu?${param.toString()}`);
      } 
      else {
        const status = res.status;
        const message = data.message || 'Erreur serveur';
        throw new Error(`Code ${status} : ${message}`);
      }
    } catch(err){
      console.error('Erreur coté frontend :', err);
      alert(`Erreur : ${err.message}`);
    }
  };

  
  //Permet d'afficher ou non le mot de passe avec les icones du champs input text password
  const[visible, setVisible] = useState(false);
  const toggleVisibility = () => setVisible((prev) => !prev);


  //redirige au clic sur le bouton créer un compte (no account)
  const handleClick = () => {
    navigate('/auth/creer');
  }

  return (
    <div className="PageAuthentification-root">
      <form onSubmit={handleSubmit} className="container">
        <img src={LogoAstoria} alt="Logo d'Astoria" className="logoAstoria" />
        <h1>Connexion</h1>
        {TimeOut &&
          <div className='container-timeout'>
            <p className='p-timeout'>Vous avez été automatiquement déconnecté en raison d'une période trop longue d'inactivité</p>
          </div>
        }
          <div className="inputs">

            <div className="inputs-icon">
              <img src={IconUser} alt="User Icon" className="icon" />
              <input type='email' id='username' placeholder='Email' onChange={(e) => setIdentifiant(e.target.value)}/>
            </div>

            <div className="inputs-icon">
              <img src={IconPW} alt="Password Icon" className="icon" />
              <input type={visible ? 'text' : 'password'} id='password' placeholder='Mot de passe' onChange={(e) => setMotDePasse(e.target.value)}/>
              <img src={visible ? IconEyeOff : IconEyeShow} alt="Afficher le mot de passe" className="eye-icon" onClick={toggleVisibility}/>
            </div>
          </div>
          
          <div className="ButtonEvent">
            <button type='submit'>Se connecter</button>
          </div>
            <label className="NoAccount" onClick={handleClick}>Créer un compte</label>
            <label className="ForgotPw">Mot de passe oublié ?</label>    
      </form>
      
    </div>
  );
}

export default Authentif;
