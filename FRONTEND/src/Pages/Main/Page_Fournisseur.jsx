import { useEffect, useState, useRef, useContext } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { AuthContext } from '../../Session/AuthContext';
import JSZip from 'jszip';
import { saveAs } from 'file-saver';


import '../../styles/Main/Page_Fournisseur.css';
import ClientProduits from './Item_ClientProduits';
import ConfirmationPopup from '../Popups/Popup_Confirmation';
import Liste_Partenaire_EntitesInsinia from './Liste_Partenaires_EntitesInsinia';
import Liste_Produits_Alpheys from './Liste_Produits_Alpheys';


function Generation_Fiche_Fournisseur(){

    //Variables récupérées dans l'URL
    const [IDCollaborateur, setIDCollaborateur] = useState('');
    const [Fournisseur, setFournisseur] = useState('');
    const [Groupe, setGroupe] = useState('');
    const [Entite, setEntite] = useState('');

    const [AucunClient, setAucunClient] = useState(false);
    const [PartenairesEntite, setPartenairesEntite] = useState([]);
    const [InsiniaPartenaireSelectionne, setInsiniaPartenaireSelectionne] = useState('');
    
    const [ProduitsAlpheys, setProduitsAlpheys] = useState([]);


    //récupère les paramètres dans l'url de la page qui contient l'id collaborateur
    const [searchParams] = useSearchParams();

    //session
    const { token, login, logout } = useContext(AuthContext);

    //hook React, permet de naviguer vers une autre page
    const navigate = useNavigate();

    //chargement après une action (spinner)
    const [loading, setLoading] = useState(false);
    const [barreRecherche, setbarreRecherche] = useState(false);
    const [progressBar, setProgressBar] = useState(0);


    
    //Variables récupérées par l'appel à la base
    const [Clients, setClients] = useState([]);
    const [NombreClients, setNombreClients] = useState();


    //Variables de checkboxes permettant le téléchargement du zip
    const [masterChecked, setMasterChecked] = useState(false);
    const [tabCheckboxes, setTabCheckboxes] = useState([]);
    const [NombreCheckboxesCochees, setNombreCheckboxesCochees] = useState();
    const [tabIDClientAGenere, setTabIDClientAGenere] = useState([]);


    //popup de confirmation de génération des fiches
    const [isPopupConfirmOpen, setIsPopupConfirmOpen] = useState(false);
    const [tempIDFournisseur, settempIDFournisseur] = useState();
    const [tempIDClient, settempIDClient] = useState();
    const [tempNomFichier, setTempNomFichier] = useState('');

    
    useEffect(() => {
        
        const IDCollaborateur = searchParams.get('id');
        setIDCollaborateur(IDCollaborateur);
        const Fournisseur = searchParams.get('fournisseur');
        setFournisseur(Fournisseur);
        const Groupe = searchParams.get('groupe');
        setGroupe(Groupe);

        let Liste_Partenaires = []

        if ((Groupe === 'ASTORIA') && (Fournisseur !== 'ALPHEYS')){
            loadData(Fournisseur);
        }
        else if ((Groupe === 'INSINIA') && (Fournisseur !== 'ALPHEYS')){
            Liste_Partenaires = Liste_Partenaire_EntitesInsinia(Fournisseur);
            setPartenairesEntite(Liste_Partenaires);
            setEntite(searchParams.get('fournisseur'));
        }
         
    }, [])


    // Si le fournisseur sélectionné est Alpheys
    useEffect(() => {
        
        loadProduits(Fournisseur);

    }, [Groupe]);


    //lorsque le tableau de clients est reçu par le frontend, on stocke les noms des checkboxes 
    //en récupérant les infos de si la fiche a été déjà générée et si elle a plusieurs produits, dans ces cas, la master checkbox ne les sélectionnera pas
    useEffect(() => {
        const tempTabCheckboxes =
            Clients.map((elt, index) => ({
                    nom: "checkbox-telecharger-" + (index+1), checked: false, EstGenere: elt.EstGenereClient, NbProduits: elt.Produits.length
            }));
           

        setTabCheckboxes(tempTabCheckboxes);

        console.log(tabCheckboxes);

    },[Clients])

    //lorsqu'il y a des modifs faites sur les checkboxes de la page (cochées/décochées)
    useEffect(() => {
        const tempNombreCheckboxesCochees = tabCheckboxes.filter(elt => elt.checked).length;

        console.log("Cochées : " + tempNombreCheckboxesCochees);
        setNombreCheckboxesCochees(tempNombreCheckboxesCochees);

    }, [tabCheckboxes]);


    // Remplit la liste des produits disponibles en Bdd si le fournisseur/partenaire sélectionné est Alpheys
    const loadProduits = async (Partenaire) => {
        let Liste_Produits = []
        if (Partenaire === 'ALPHEYS'){
            Liste_Produits = await Liste_Produits_Alpheys(Groupe);
            setProduitsAlpheys(Liste_Produits);
        }
    }


    const loadData = async(Fournisseur, IDProduitAlpheys = 0) => {
        try{
            setLoading(true);
            const res = await fetch('/api/partenaire', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization' : `Bearer ${token}`
                },
                body : JSON.stringify({ 
                    groupe : Groupe,
                    fournisseur : Fournisseur,
                    idproduitalpheys : IDProduitAlpheys
                })
            });

            const data = await res.json();
            
            if (res.ok) {
                setAucunClient(false);
                login(data.new_access_token);
                const groupesClients = MiseEnForme_GroupesClient(data.client_liste);
                setClients(groupesClients);
                setNombreClients(data.client_liste.length);

            }
            else if ((res.status === 400) && (data.error === 'table_vide')){
                setAucunClient(true);
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
            console.error('Erreur coté frontend :', err.message);
            //alert(`Erreur : ${err.message}`);
        } finally{
            setLoading(false);
        }
    }


    const loadDataInsinia = async(Entite, Partenaire, IDProduitAlpheys = 0) => {
        console.log("Entite : " + Entite + ", Partenaire : " + Partenaire + ", IDProduitAlpheys : " + IDProduitAlpheys);
        try{
            setLoading(true);
            setInsiniaPartenaireSelectionne(Partenaire);
            setFournisseur(Partenaire);

            const res = await fetch('/api/partenaireinsinia', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization' : `Bearer ${token}`
                },
                body : JSON.stringify({ 
                    entite : Entite,
                    partenaire : Partenaire,
                    idproduitalpheys : IDProduitAlpheys
                })
            });

            const data = await res.json();
            
            if (res.ok) {
                setAucunClient(false);
                login(data.new_access_token);
                const groupesClients = MiseEnForme_GroupesClient(data.client_liste);
                setClients(groupesClients);
                setNombreClients(data.client_liste.length);

                console.log(data.client_liste);
            }
            else if ((res.status === 400) && (data.error === 'table_vide')){
                setAucunClient(true);
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
            console.error('Erreur coté frontend :', err.message);
            //alert(`Erreur : ${err.message}`);
        } finally{
            setLoading(false);
        }
    }

    // A la sélection d'un élément dans la liste des partenaires INSINIA
    const Selection_Elts_Insinia = async (Entite, Partenaire) => {
        setFournisseur(Partenaire);
        setClients([]);
        setNombreClients(0);
        if (Partenaire !== 'ALPHEYS'){
            loadDataInsinia(Entite, Partenaire)
            setEntite(Entite);
            setProduitsAlpheys([]);
        }
        else{
            await loadProduits(Partenaire);
        }
            
    };


    const PreloadData = (IDProduitAlpheys) => {
        setClients([]);
        setNombreClients(0);

        if (Groupe === 'ASTORIA'){
            if (IDProduitAlpheys !== "null"){
                loadData(Fournisseur, IDProduitAlpheys);
            }
        }
        else if (Groupe === 'INSINIA'){
            if (IDProduitAlpheys !== "null"){
                loadDataInsinia(Entite, Fournisseur, IDProduitAlpheys);
            }
        }
            
    }


    // Regroupe les clients qui ont le même IDClient
    const MiseEnForme_GroupesClient = (client_liste) => {

        //Variable pour grouper les IDs client qui sont les mêmes
        const clientsGroupes = [];

        client_liste.forEach((ligne) => {
            const clientExistant = clientsGroupes.find(c => c.IDClient === ligne.IDClient);

            const produit = {
                ProduitFournisseur: ligne.ProduitFournisseur,
                FournisseurMontantTotalSouscrit : ligne.FournisseurMontantTotalSouscrit,
                IDFournisseur: ligne.IDFournisseur,
            };

            if (clientExistant) {
                clientExistant.Produits.push(produit);
            } else {
                clientsGroupes.push({
                    IDClient: ligne.IDClient,
                    Nom: ligne.Nom,
                    Prenom: ligne.Prenom,
                    Region: ligne.Region,
                    Bureau: ligne.Bureau,
                    Conseiller: ligne.Conseiller,
                    NumeroCompte: ligne.NumeroCompte,
                    DateOuverture: ligne.DateOuverture,
                    Compte_au_01_01_2024: ligne.Compte_au_01_01_2024,
                    Compte_au_31_12_2024: ligne.Compte_au_31_12_2024,
                    EstGenereClient: ligne.EstGenereClient,
                    EtablissementFournisseur: ligne.EtablissementFournisseur,
                    TypeProduit: ligne.TypeProduit,
                    ProduitClient: ligne.ProduitClient,
                    Produits: [produit]
                });
            }
        });

        return clientsGroupes;
    }


    const load_InfosClient_Fiche = async (IDClient, IDFournisseur, Region, Bureau, Produit, Nom, Prenom, Resultat) => {

        console.log(IDClient, IDFournisseur, Bureau, Produit, Nom, Prenom);
        try{
            setLoading(true);
            const res = await fetch('/api/partenaire/fetch-pdf', {
                method: 'POST',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization' : `Bearer ${token}`
                },
                body : JSON.stringify({ 
                    groupe: Groupe,
                    fournisseur: Fournisseur,
                    entite: Entite,
                    IDClient : IDClient,
                    IDFournisseur : IDFournisseur
                })
            });

            
            if (res.ok) {
                const newToken = res.headers.get("X-new-access-token")
                if (newToken)
                    login(newToken);
                
                const blob = await res.blob();
                const pdfURL = window.URL.createObjectURL(blob);

                let NomFichier = SetUp_NomFichier(Region, Bureau, Produit, Nom, Prenom);

                // Visionner dans une nouvel fenêtre
                if (Resultat === "Visionner"){
                    const newWindow = window.open(pdfURL, '_blank');
                }
                // Télécharger la fiche directement 
                else if (Resultat === "Telecharger"){
                    const link = document.createElement('a');
                    link.href = pdfURL;
                    link.download = NomFichier;
                    document.body.appendChild(link);
                    link.click();
                    link.remove();

                    setTimeout(() => URL.revokeObjectURL(pdfURL), 1000);
                }
                

                setIsPopupConfirmOpen(true);
                settempIDFournisseur(IDFournisseur);
                settempIDClient(IDClient);
            }
            else if (res.status === 401){
                logout();
                const param = new URLSearchParams({timeout : "true"});
                navigate(`/?${param.toString()}`);
            }
            else {
                const data = await res.json();
                const status = res.status;
                const message = data.message || 'Erreur serveur';
                throw new Error(`Code ${status} : ${message}`);
            }
        } catch(err){
            console.error('Erreur coté frontend :', err);
            alert(`Erreur : ${err.message}`);
        } finally{
            setLoading(false);
        }
    }

    /*Permet de créer un nom de fichier pour enregistrer les documents*/
    const SetUp_NomFichier = (Region, Bureau, Produit, Nom, Prenom) => {
        let temp = ''

        if (Groupe === 'ASTORIA'){
            if ((Region !== '') && (Region !== null) && Region !== undefined)
                temp += `${Region.replace(/ /g, "_")}`;
            if (Bureau !== '')
                if (temp === '')
                    temp += `${Bureau.replace(/ /g, "_")}`;
                else
                    temp += `_${Bureau.replace(/ /g, "_")}`;
        }
        else if (Groupe === 'INSINIA'){
            if ((Entite !== '') && (Entite !== null)){
                temp += `${Entite.replace(/ /g, "_")}`;
            }
        }

        if ((Produit !== '') && (Produit !== null))
            if (temp === '')
                temp += `${Produit.replace(/ /g, "_")}`;
            else
                temp += `_${Produit.replace(/ /g, "_")}`;
        if (Nom !== '')
            temp += `_${Nom}`;
        if (Prenom !== '')
            temp += `_${Prenom}`;
        temp += '.pdf'

        setTempNomFichier(temp);
        return temp;
    }


    const Check_NomFichier = (TableauNomFichiers = [], NomFichier = "", Numero = 2) => {
        let NouveauNomFichier = NomFichier;
        let chiffreAvantVirgule = Math.floor(Numero).toString().length

        if (TableauNomFichiers.includes(NomFichier)){
            if (Numero > 2){
                NouveauNomFichier = NouveauNomFichier.slice(0, -4 -chiffreAvantVirgule -1) + '_' + String(Numero) + '.pdf'
            }
            else {
                NouveauNomFichier = NouveauNomFichier.slice(0, -4) + '_' + String(Numero) + '.pdf'
            }
            return Check_NomFichier(TableauNomFichiers, NouveauNomFichier, Numero +1);
        }

        return NouveauNomFichier;

    }



    // flag une fiche qui vient d'être générer pour changer l'affichage de la fenetre (griser les composant dont la fiche a déjà été générée)
    const update_data_EstGenere_ASTORIA = async () => {
        try{
            console.log(tempIDFournisseur);
            setLoading(true);
            const res = await fetch('/api/client/fiche_EstGeneree', {
                method: 'PATCH',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization' : `Bearer ${token}`
                },
                body : JSON.stringify({ 
                    IDClient : tempIDClient,
                    Fournisseur : Fournisseur
                })
            });

            const data = await res.json();

            if (res.ok) {
                login(data.new_access_token);
                settempIDFournisseur('');
                settempIDClient('');
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
            alert(`Erreur : ${err.message}`);
        } finally{
            setLoading(false);
            setIsPopupConfirmOpen(false);
        }
    }

    const update_data_EstGenere_INSINIA = async () => {
        try{
            console.log(tempIDFournisseur);
            setLoading(true);
            const res = await fetch('/api/client/fiche_EstGenereeInsinia', {
                method: 'PATCH',
                headers: { 
                    'Content-Type': 'application/json',
                    'Authorization' : `Bearer ${token}`
                },
                body : JSON.stringify({ 
                    IDClient : tempIDClient,
                    entite : Entite
                })
            });

            const data = await res.json();

            if (res.ok) {
                login(data.new_access_token);
                settempIDClient('');
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
            alert(`Erreur : ${err.message}`);
        } finally{
            setLoading(false);
            setIsPopupConfirmOpen(false);
        }
    };


    const griser_composant_genere = () => {
        setClients(prevClients =>
                prevClients.map(client =>
                    client.IDClient === tempIDClient
                        ? { ...client, EstGenereClient: true }
                        : client
                )
        );
    };


    const griser_all_composant_genere = (tabIDClient) => {
        for (let IDClient of tabIDClient){
            setClients(prevClients =>
                prevClients.map(client =>
                    client.IDClient === IDClient
                        ? { ...client, EstGenereClient: true }
                        : client
                )
            );
        }
    };



    // Au clic du bouton 'oui' sur la popup de confirmation, après avoir cliqué sur le bouton 'Générer la fiche'
    const ConfirmClic = () => {

        if (Groupe === 'ASTORIA')
            update_data_EstGenere_ASTORIA();
        else if (Groupe === 'INSINIA')
            update_data_EstGenere_INSINIA();

        griser_composant_genere();
        
    }


    // coche/décoche TOUTES les checkboxes de la page (sauf pour les clients déjà générés)
    const Checker_toutes_les_checkboxes = (event) => {
        const CheckboxCochee = event.target.checked;

        const tempTabCheckboxes = tabCheckboxes.map(item => ({
            ...item, checked: ((item.EstGenere || item.NbProduits > 1) ? false : CheckboxCochee)
        }));


        setMasterChecked(CheckboxCochee);
        setTabCheckboxes(tempTabCheckboxes);
    };


    // coche/décoche INDIVIDUELLEMENT les checkboxes de la page (checkbox enfant)
    const CheckUncheck_checkbox = (indexElt) => {
        setTabCheckboxes(previous => 
            previous.map((item, i) => 
                i === indexElt
                    ? { ...item, checked: !item.checked}
                    : item
                )
        );

        console.log(tabCheckboxes);
    };


    //Puis on télécharge tous les éléments qui ont été cochées dans la page
    const load_ToutesFiches_Cochees = async () => {

        const clientsCoches = Clients.filter((client, index) =>
            tabCheckboxes[index]?.checked === true
        );

        if (clientsCoches.length === 0) {
            alert("Aucune checkbox n'a été cochée ou alors les fiches ont déjà été sorties !");
            return;
        }

        const MAX_PDF_PAR_ZIP = 100;

        let zip = new JSZip();
        let indexZip = 1;
        let nbPdfDansZip = 0;

        setbarreRecherche(true);

        let tempTabIDClientAGenere = [];
        let TableauNomFichier = [];

        // === Barre de chargement ===
        let totalPDF = 0;
        clientsCoches.forEach(client => {
            totalPDF += client.Produits.length;
        });

        let currentPDF = 0;
        let index =1;

        for (let client of clientsCoches) {

            for (let produit of client.Produits) {

                console.log("index : " + index);
                index ++;
                console.log(client)

                const res = await fetch("/api/partenaire/fetch-pdf", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json",
                        "Authorization": `Bearer ${token}`,
                    },
                    body: JSON.stringify({
                        groupe: Groupe,
                        fournisseur: Fournisseur,
                        entite: Entite,
                        IDClient: client.IDClient,
                        IDFournisseur: produit.IDFournisseur
                    })
                });

                if (!res.ok) {
                    console.error("statut :", res.status);
                    continue;
                }

                const blob = await res.blob();
                const buffer = await blob.arrayBuffer();

                const tempnomFichier = SetUp_NomFichier(
                    client.Region,
                    client.Bureau,
                    client.ProduitClient,
                    client.Nom,
                    client.Prenom
                );

                const nomFichierFinal = Check_NomFichier(
                    TableauNomFichier,
                    tempnomFichier
                );

                zip.file(nomFichierFinal, buffer);
                TableauNomFichier.push(nomFichierFinal);

                nbPdfDansZip++;
                currentPDF++;

                // === Progress bar ===
                setProgressBar(Math.round((currentPDF / totalPDF) * 100));

                // === Si on atteint la limite → on génère le ZIP ===
                if (nbPdfDansZip >= MAX_PDF_PAR_ZIP) {

                    const contenuZip = await zip.generateAsync({ type: "blob" });
                    saveAs(contenuZip, `Fiches_Reporting_part_${indexZip}.zip`);

                    // reset mémoire
                    zip = new JSZip();
                    nbPdfDansZip = 0;
                    indexZip++;
                    TableauNomFichier = [];
                }
            }

            tempTabIDClientAGenere.push(client.IDClient);
        }

        // === Dernier ZIP s'il reste des PDF ===
        if (nbPdfDansZip > 0) {
            const contenuZip = await zip.generateAsync({ type: "blob" });
            saveAs(contenuZip, `Fiches_Reporting_part_${indexZip}.zip`);
        }

        console.log("Tableau d'IDs Client : ", tempTabIDClientAGenere);
        setTabIDClientAGenere(tempTabIDClientAGenere);
        update_all_data_EstGenere(tempTabIDClientAGenere);
        griser_all_composant_genere(tempTabIDClientAGenere);

        setMasterChecked(false);
        setbarreRecherche(false);
    };


    const update_all_data_EstGenere = async (TabIDClientAGenere) => {
        try{
            setLoading(true);
            let res;

            if (Groupe === 'ASTORIA'){
                res = await fetch('/api/client/allfiches_EstGeneree', {
                    method: 'PATCH',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Authorization' : `Bearer ${token}`
                    },
                    body : JSON.stringify({ 
                        tabIDClient : TabIDClientAGenere
                    })
                });
            }
            else if (Groupe === 'INSINIA'){
                res = await fetch('/api/client/allfiches_EstGenereeInsinia', {
                    method: 'PATCH',
                    headers: { 
                        'Content-Type': 'application/json',
                        'Authorization' : `Bearer ${token}`
                    },
                    body : JSON.stringify({ 
                        tabIDClient : TabIDClientAGenere,
                        entite : Entite
                    })
                });
            }

            const data = await res.json();

            if (res.ok) {
                login(data.new_access_token);
                settempIDClient('');
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
            alert(`Erreur : ${err.message}`);
        } finally{
            setLoading(false);
            setIsPopupConfirmOpen(false);
        }
    }


    return(
        <div className='Page_Fournisseur-root'>

            <div className='header'>
                <div className='header-titre'>
                    {Groupe === 'ASTORIA' &&
                        <h1> {Fournisseur || "Chargement ..."} </h1>
                    }
                    {Groupe === 'INSINIA' &&
                        <h1> {Entite || "Chargement ..."} </h1>
                    }
                </div>
                <div className='container-ligne-listepartenaires'>
                    
                    <div className='header-ligne'>
                        <label> {(NombreClients ?? 0) + " Lignes"}  </label>
                    </div>
                    
                    <div className='container-listes'>
                        {Groupe === 'INSINIA' &&
                            <div className='header-listepartenaires'>            
                                <select name="listes_partenaires" className='liste-partenaires' onChange={(e) => Selection_Elts_Insinia(Entite, e.target.value)} >
                                        <option value="null">Choisir un partenaire</option>
                                        {PartenairesEntite.map((elt) => (
                                            <option key={elt.Nom} value={elt.Nom}>{elt.Libelle}</option>
                                    ))}
                                </select>
                            </div>
                        }
                        
                        {ProduitsAlpheys.length > 0 &&
                            <div className='header-listeproduits'>            
                                <select name="listes_produits" className='liste-produits' onChange={(e) => PreloadData(e.target.value)} >
                                        <option value="null">Choisir un produit</option>
                                        {ProduitsAlpheys.map((elt) => (
                                            <option key={elt.NomProduit} value={elt.ID}>{elt.NomProduit}</option>
                                    ))}
                                </select>
                            </div>
                        }
                    </div>
                </div>
                <div className='container-checkboxmaster-btntelechargertous'>
                    <div className='container-checkbox-label'>
                        <input type="checkbox" className={NombreClients > 0 ? "checkbox-tout" : "checkbox-tout inactive"} name="checkbox-master" checked={masterChecked} onChange={(e) => Checker_toutes_les_checkboxes(e)}/>
                        <label htmlFor="checkbox-master" className={NombreClients > 0 ? "" : "inactive"}>Tout cocher</label>
                    </div>
                    <button className={NombreClients > 0 ? "header-telecharger" : "header-telecharger inactive"} onClick={load_ToutesFiches_Cochees}>Télécharger ({NombreCheckboxesCochees} fiches)</button>
                    
                </div>
            </div>
            
            <div className='main'>
                {AucunClient &&
                    <div className='container-libelle-aucunclient'>
                        <h2 className='main-libelle-aucunclient'>Aucun client à afficher</h2>
                    </div>
                }
                {Clients.map((client, index) => (
                    <ClientProduits
                        key={index}
                        Index={index}
                        Ligne={index + 1}
                        IDClient={client.IDClient}
                        Nom={client.Nom}
                        Prenom={client.Prenom}
                        Region={client.Region}
                        Bureau={client.Bureau}
                        Conseiller={client.Conseiller}
                        NumeroCompte= {client.NumeroCompte}
                        DateOuverture= {client.DateOuverture}
                        Compte_au_01_01_2024= {client.Compte_au_01_01_2024}
                        Compte_au_31_12_2024= {client.Compte_au_31_12_2024}
                        Etablissement={client.EtablissementFournisseur}
                        Type={client.TypeProduit}
                        ProduitClient={client.ProduitClient}
                        EstGenere={client.EstGenereClient}
                        Produits={client.Produits}
                        load_InfosClient_Fiche={load_InfosClient_Fiche}
                        EstCoche={tabCheckboxes[index]?.checked}
                        CheckUncheck_checkbox={CheckUncheck_checkbox}
                    />
                ))}
            </div>

            <ConfirmationPopup
                    isOpen={isPopupConfirmOpen}
                    message= {<>
                        Voulez-vous considérer la fiche <span className='span-nom-fichier'>{tempNomFichier}</span> sur laquelle vous venez de cliquer comme 'générée' ? 
                        </>}
                    onConfirm={() => {ConfirmClic(); setTempNomFichier('')}}
                    onCancel={() => {setIsPopupConfirmOpen(false); setTempNomFichier('')}}
            />

            {loading && (
                    <div className="loading-overlay">
                        <div className="spinner"></div>
                    </div>
            )}


            {barreRecherche && (
                <div className="progress-overlay">
                    <div className="progress-container">
                        <div className="progress-bar" style={{ width: progressBar + "%" }}>
                            {progressBar}%
                        </div>
                    </div>
                </div>
            )}
        </div>
    )

}export default Generation_Fiche_Fournisseur;