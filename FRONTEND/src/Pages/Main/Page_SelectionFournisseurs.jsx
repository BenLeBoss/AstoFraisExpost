import { useEffect, useState, useRef, useContext } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { AuthContext } from '../../Session/AuthContext';

import '../../styles/Main/Page_SelectionFournisseurs.css';

function Selection_Fournisseur(){

    //Collaborateur actuellement connecté
    const [IDCollaborateur, setIDCollaborateur] = useState('')

    //récupère les paramètres dans l'url de la page qui contient l'id collaborateur
    const [searchParams] = useSearchParams();

    //session
    const { token, login, logout } = useContext(AuthContext);

    //hook React, permet de naviguer vers une autre page
    const navigate = useNavigate();

    //chargement après une action (spinner)
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        if (!token) return;

        const IDCollaborateur = searchParams.get('id');
        setIDCollaborateur(IDCollaborateur);
    }, [token])



    const Selection_Fournisseur = (Fournisseur, Groupe) => {
        if (Fournisseur !== null){
            const Fournisseur_ValeurBaseDeDonnées = Fournisseur
            const param1 = new URLSearchParams({id : IDCollaborateur});
            const param2 = new URLSearchParams({fournisseur : Fournisseur_ValeurBaseDeDonnées});
            const param3 = new URLSearchParams({groupe : Groupe});
            navigate(`/partenaire?${param1.toString()}&${param2.toString()}&${param3.toString()}`);
        }
    }
    
    /*Navigation vers les fiches qui ont été générées*/
    const Consultation_fichesgenerees = (Groupe) => {
        const param1 = new URLSearchParams({id : IDCollaborateur});
        const param2 = new URLSearchParams({groupe : Groupe});
        navigate(`/client/consultation/fichesgenerees?${param1.toString()}&${param2.toString()}`);
    }


    /*Navigation vers les fiches qui ont été générées*/
    const Consultation_fichesnongenerees = (Groupe) => {
        const param1 = new URLSearchParams({id : IDCollaborateur});
        const param2 = new URLSearchParams({groupe : Groupe});
        navigate(`/client/consultation/fichesnongenerees?${param1.toString()}&${param2.toString()}`);
    }


    return(
        <div className='Page_SelectionFournisseur-root'>
            <div className='main main-Astoria'>
                <div className='main-titre'>
                    <h1>Groupe ASTORIA - Sélection de fournisseurs</h1>
                </div>
                <div className='container-liste-button'>
                    <div className='main-liste'>
                            <select name="listes_fournisseurs" className='liste-fournisseurs' onChange={(e) => Selection_Fournisseur(e.target.value, "ASTORIA") }>
                                <option value="null">Choisir un fournisseur</option>
                                <option value="123IM">123Im</option>
                                <option value="ALPHEYS">Alpheys</option>
                                <option value="ALTAROC">Altaroc</option>
                                <option value="APICAP">Apicap</option>
                                <option value="ATLAND VOISIN">Atland voisin</option>
                                <option value="BanqueLeonardo">Banque leonardo</option>
                                <option value="BILBanqueInternationalLuxembourg">Bil banque international luxembourg</option>
                                <option value="BNPPARIBAS">Bnp paribas</option>
                                <option value="BOURSORAMA">Boursorama</option>
                                <option value="CORUM L'EPARGNE">Corum</option>
                                <option value="EIFFEL INVESTMENT GROUP">Eiffel investement group</option>
                                <option value="EXTENDAM">Extendam</option>
                                <option value="FRANCE VALLEY INVESTISSEMENTS">France valley</option>
                                <option value="INOCAP">Inocap</option>
                                <option value="intergestion">Intergestion</option>
                                <option value="KEYSAM">Keys am</option>
                                <option value="Lafinancièredel'échiquier">La financière de l'échiquier</option>
                                <option value="LAFRANCAISEAM">La francaise am</option>
                                <option value="MeaningsCapitalPartners">Meanings capital partners</option>
                                <option value="Mymoneybank">Mymoneybank</option>
                                <option value="NORMA CAPITAL">Norma capital</option>
                                <option value="OCPFinance">Ocp finance</option>
                                <option value="ODDO">Oddo</option>
                                <option value="Odyssee-Venture">Odyssee - venture</option>
                                <option value="PAREF">Paref</option>
                                <option value="PERIAL ASSET MANAGEMENT">Perial</option>
                                <option value="PRIMONIAL">Primonial</option>
                                <option value="SMALT CAPITAL">Smalt capital</option>
                                <option value="SOCIETEGENERALE">Societe generale</option>
                                <option value="SOFIDY">Sofidy</option>
                                <option value="Suravenir">Suravenir</option>
                                <option value="TeorabyNatixis">Teora by natixis</option>
                                <option value="THEOREIM">Theoreim</option>
                                <option value="UAFLIFE">Uaf life</option>
                                <option value="URBAN PREMIUM">Urban premium</option>
                                <option value="VATELCAPITAL">Vatel capital</option>
                                <option value="XERYSINVEST">Xerys Invest</option>
                                
                            </select>
                    </div>
                    <div className='main-button'>
                        <button className='button-consult'  onClick={() => Consultation_fichesgenerees("ASTORIA")}>Consulter les fiches générées</button>
                        <button className='button-consult'  onClick={() => Consultation_fichesnongenerees("ASTORIA")}>Consulter les fiches non générées</button>
                    </div>
                </div>
            </div>



            <div className='main main-Insinia'>
                <div className='main-titre'>
                    <h1>Groupe INSINIA - Sélection d'entités</h1>
                </div>
                <div className='container-liste-button'>
                    <div className='main-liste'>
                            <select name="listes_fournisseurs" className='liste-fournisseurs' onChange={(e) => Selection_Fournisseur(e.target.value, "INSINIA") }>
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
                    <div className='main-button'>
                        <button className='button-consult'  onClick={() => Consultation_fichesgenerees("INSINIA")}>Consulter les fiches générées</button>
                        <button className='button-consult'  onClick={() => Consultation_fichesnongenerees("INSINIA")}>Consulter les fiches non générées</button>
                    </div>
                </div>
            </div>

            {loading && (
                    <div className="loading-overlay">
                        <div className="spinner"></div>
                    </div>
            )}
        </div>
    )

}export default Selection_Fournisseur;