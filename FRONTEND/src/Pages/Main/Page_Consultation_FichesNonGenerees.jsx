import { useEffect, useState, useRef, useContext } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { AuthContext } from '../../Session/AuthContext';

import '../../styles/Main/Page_Consultation_FichesGenerees.css';
import Client_Liste_FicheGeneree from './Item_Tableau _ConsultationFichesGenerees';

import IconSort from '../../medias/img/sortable.svg'
import IconSortUp from '../../medias/img/sort-up.svg'
import IconSortDown from '../../medias/img/sort-down.svg'

function Consultation_FichesNonGenerees(){

    //Variables récupérées dans l'URL
    const [IDCollaborateur, setIDCollaborateur] = useState('');
    const [Groupe, setGroupe] = useState('');

    //récupère les paramètres dans l'url de la page qui contient l'id collaborateur
    const [searchParams] = useSearchParams();

    //session
    const { token, login, logout } = useContext(AuthContext);

    //hook React, permet de naviguer vers une autre page
    const navigate = useNavigate();

    //chargement après une action (spinner)
    const [loading, setLoading] = useState(false);

    
    //Variables récupérées par l'appel à la base
    const [Clients, setClients] = useState([]);
    const [NombreFiches, setNombreFiches] = useState();


    //Variable de tri sur le tableau
    //Avec une clé correspondant aux colonne du tableau à trier
    //Avec un ordre alphabétique ou inversé ("asc"/"desc")
    const [triTab, setTriTab] = useState({clé : null, ordre: "asc"});

    //Variable triant le tableau de clients en fonction de la clé
    const ClientTrie = [...Clients].sort((a,b) => {

        /*si triTab n'est pas null, alors on recalcule auto la variable ClientTrie*/
        if (!triTab.clé) return 0;
 
        let ValeurA;
        let ValeurB;

        if (typeof(a[triTab.clé]) === "string"){
            ValeurA = a[triTab.clé].toLowerCase();
        } else {
            ValeurA = a[triTab.clé];
        }
 
        if (typeof(b[triTab.clé]) === "string"){
            ValeurB = b[triTab.clé].toLowerCase();
        } else {
            ValeurB = b[triTab.clé];
        }


        if (!ValeurA) return 0;
        if (!ValeurB) return 0;


        if (ValeurA > ValeurB) return triTab.ordre === "asc" ? 1 : -1 
        if (ValeurA < ValeurB) return triTab.ordre === "asc" ? -1 : 1 
        
        return 0;
        
    });



    useEffect(() => {
        
        const IDCollaborateur = searchParams.get('id');
        setIDCollaborateur(IDCollaborateur);
        const Groupe = searchParams.get('groupe');
        setGroupe(Groupe);

        if (Groupe === 'ASTORIA')
            load_fiches_nongenerees_ASTORIA();

    }, [])


    const load_fiches_nongenerees_ASTORIA = async() => {
        try{
            setClients([]);
            setNombreFiches(0);

            setLoading(true);
            const res = await fetch('/api/client/consultation/fichesnongenerees', {
                method: 'GET',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization' : `Bearer ${token}`
                }
            });

            const data = await res.json();

            if (res.ok) {
                login(data.new_access_token);
                setClients(data.client_liste);
                setNombreFiches(data.client_liste.length);
            }
            else if (res.status === 401){
                logout();
                const param = new URLSearchParams({timeout : "true"});
                navigate(`/?${param.toString()}`);
            }
            else {
                const status = res.status;
                const message = data.message || 'Erreur serveur';
                throw new Error(`Code ${status} : ${message}`);
            }
        } catch(err){
            console.error('Erreur coté frontend :', err);
            //alert(`Erreur : ${err.message}`);
        } finally{
            setLoading(false);
        }
    }


    const load_fiches_generees_INSINIA = async(Entite) => {
        try{
            setClients([]);
            setNombreFiches(0);

            setLoading(true);
            const res = await fetch('/api/client/consultation/fichesnongenereesinsinia', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization' : `Bearer ${token}`
                },
                body : JSON.stringify({ 
                    entite : Entite
                })
            });

            const data = await res.json();

            if (res.ok) {
                login(data.new_access_token);
                setClients(data.client_liste);
                setNombreFiches(data.client_liste.length);
            }
            else if (res.status === 401){
                logout();
                const param = new URLSearchParams({timeout : "true"});
                navigate(`/?${param.toString()}`);
            }
            else {
                const status = res.status;
                const message = data.message || 'Erreur serveur';
                throw new Error(`Code ${status} : ${message}`);
            }
        } catch(err){
            console.error('Erreur coté frontend :', err);
            //alert(`Erreur : ${err.message}`);
        } finally{
            setLoading(false);
        }
    }


    //implémentation du tri du tableau en fonction de la colonne cliquée
    const activerTri = (clé) => {
        setLoading(true);

        let tempOrdre = "asc";
        if (triTab.clé === clé && triTab.ordre === "asc")
            tempOrdre = "desc";

        // Déclenche le tri
        setTriTab({clé : clé, ordre : tempOrdre});
        
        setTimeout(() => setLoading(false), 100);
    }


    return(
        <div className='Page_Consultation_FichesGenerees-root'>

            <div className='header'>
                <div className='header-titre'>
                    <h1> Fiches non générées pour les clients suivants </h1>
                </div>
                <div className='container-ligne-listepartenaires'>
                    <div className='header-ligne'>
                        <label> {(NombreFiches ?? 0) + " Fiches n'ont pas été générées"}  </label>
                    </div>

                    {Groupe === 'INSINIA' &&
                            <div className='header-listepartenaires'>            
                                <select name="listes_partenaires" className='liste-partenaires' onChange={(e) => load_fiches_generees_INSINIA(e.target.value)} >
                                        <option value="null">Choisir une entité</option>
                                        <option value="ACTIONPATRIMOINE">Action patrimoine</option>
                                        <option value="ALLUREFINANCE">Allure finance</option>
                                        <option value="BCFINANCES">Bc finances</option>
                                        <option value="CAPIUM">Capium</option>
                                        <option value="FAMILYPATRIMOINE">Family patrimoine</option>
                                        <option value="FIPAGEST">Fipagest</option>
                                        <option value="MYFAMILYOFFICER">My family officer</option>
                                        <option value="PARISII">Parisii</option>
                                        <option value="SOLVEPATRIMOINE">Solve patrimoine</option>
                                        <option value="SYNERGIECONSEILSPATRIMOINE">Synergie conseils patrimoine</option>
                                        <option value="WATSONPATRIMOINE">Watson patrimoine</option>
                                </select>
                            </div>
                    }
                </div>
            </div>
            <div className='main'>
                <table className="main-table-data">
                    <thead>
                        <tr>
                            <th scope="col" className="table-col-Numero"></th>
                            <th scope="col" onClick={() => activerTri("Nom")} className="table-col-Nom">Nom {triTab.clé === 'Nom' 
                                                    ? (triTab.ordre === 'asc' ? <img src={IconSortUp} alt='sort' width={20} className='icon-tab-colonne'/> : <img src={IconSortDown} alt='sort' width={20} className='icon-tab-colonne'/>) 
                                                    : <img src={IconSort} alt='sort' width={14} className='icon-tab-colonne'/>}</th>
                            
                            <th scope="col" onClick={() => activerTri("Prenom")} className="table-col-Prenom">Prénom {triTab.clé === 'Prenom'
                                                    ? (triTab.ordre === 'asc' ? <img src={IconSortUp} alt='sort' width={20} className='icon-tab-colonne'/> : <img src={IconSortDown} alt='sort' width={20} className='icon-tab-colonne'/>) 
                                                    : <img src={IconSort} alt='sort' width={14} className='icon-tab-colonne'/>}</th>
                            
                            <th scope="col" onClick={() => activerTri("EtablissementFournisseur")} className="table-col-Partenaire">Partenaire {triTab.clé === 'EtablissementFournisseur' 
                                                    ? (triTab.ordre === 'asc' ? <img src={IconSortUp} alt='sort' width={20} className='icon-tab-colonne'/> : <img src={IconSortDown} alt='sort' width={20} className='icon-tab-colonne'/>) 
                                                    : <img src={IconSort} alt='sort' width={14} className='icon-tab-colonne'/>}</th>
                            
                            <th scope="col" onClick={() => activerTri("Produit")} className="table-col-Produit">Produit {triTab.clé === 'Produit' 
                                                    ? (triTab.ordre === 'asc' ? <img src={IconSortUp} alt='sort' width={20} className='icon-tab-colonne'/> : <img src={IconSortDown} alt='sort' width={20} className='icon-tab-colonne'/>) 
                                                    : <img src={IconSort} alt='sort' width={14} className='icon-tab-colonne'/>}</th>
                            
                            <th scope="col" className="table-col-Compte">Compte </th>
                            
                            <th scope="col" className="table-col-Compte_31_12">Compte au 31/12</th>
                        </tr>
                    </thead>
                    <tbody>
                        {ClientTrie.map((client, index) => (
                            <Client_Liste_FicheGeneree 
                                key={index} 
                                Numero={index+1} 
                                Nom={client.Nom}
                                Prenom={client.Prenom} 
                                NumeroCompte={client.NumeroCompte} 
                                Partenaire={client.EtablissementFournisseur} 
                                Produit={client.Produit} 
                                Compte_31_12={client.Compte_au_31_12_2024} 
                            />
                        ))}
                    </tbody>
                </table>
            </div>
            {loading && (
                    <div className="loading-overlay">
                        <div className="spinner"></div>
                    </div>
            )}
        </div>
    );

}
export default Consultation_FichesNonGenerees
