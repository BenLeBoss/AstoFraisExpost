
function ClientProduits({IDClient, Index, Ligne, Nom, Prenom, Region, Bureau, Conseiller,  NumeroCompte, DateOuverture,Compte_au_01_01_2024, Compte_au_31_12_2024, Etablissement, 
                            Type, ProduitClient, EstGenere, Produits, load_InfosClient_Fiche, EstCoche, CheckUncheck_checkbox}){

    return(
        <div className={ EstGenere ? "container-item-client-produits genere" 
                            : EstCoche ? "container-item-client-produits coche"
                            : "container-item-client-produits"}>

            <div className="container-infos-client">
                <div className="header-infos titre">
                    <h3>{Ligne}. Informations Client</h3>
                    {!EstGenere && Produits.length === 1 && (
                        <input type="checkbox" className="checkboxes-telecharger" checked={EstCoche ?? false} name={"checkbox-telecharger-" + Ligne} onChange={() => CheckUncheck_checkbox(Index)}/>
                    )}
                </div>
                <div className="main-infos">
                    <div className="label-input Nom">
                        <div className="container-label-infos">
                            <label className="label-infos"> Nom </label>
                        </div>
                        <input type="text" value={Nom || ""} className="input-infos" readOnly="readOnly" />
                    </div>
                    <div className="label-input Prenom">
                        <div className="container-label-infos">
                            <label className="label-infos"> Prénom </label>
                        </div>
                        <input type="text" value={Prenom || ""} className="input-infos" readOnly="readOnly"/>
                    </div>
                    <div className="label-input Bureau">
                        <div className="container-label-infos">
                            <label className="label-infos"> Bureau </label>
                        </div>
                        <input type="text" value={Bureau || ""} className="input-infos" readOnly="readOnly"/>
                    </div>
                    <div className="label-input Conseiller">
                        <div className="container-label-infos">
                            <label className="label-infos"> Conseiller </label>
                        </div>
                        <input type="text" value={Conseiller || ""} className="input-infos" readOnly="readOnly"/>
                    </div>
                </div>
            </div>

            <div className="container-infos-produit">
                <div className="header-infos">
                    <h3>Informations Produit</h3>
                </div>
                <div className="main-infos-1">
                    <div className="label-input Etablissement">
                        <div className="container-label-infos">
                            <label className="label-infos"> Établissement </label>
                        </div>
                        <input type="text" value={Etablissement || ""} className="input-infos" readOnly="readOnly"/>
                    </div>
                    <div className="label-input Type">
                        <div className="container-label-infos">
                            <label className="label-infos"> Type </label>
                        </div>
                        <input type="text" value={Type || ""} className="input-infos" readOnly="readOnly"/>
                    </div>
                    
                </div>
            </div>

            <div className="container-infos-produit">
                <div className="header-infos">
                    <h3>Informations client sur le produit</h3>
                </div>
                <div className="main-infos-1">
                        <div className="label-input NumCompte">
                            <label>Numéro de compte</label>
                            <input value={NumeroCompte || ""} className="input-infos" readOnly />
                        </div>
                        <div className="label-input DateOuverture">
                            <label>Date d'ouverture</label>
                            <input value={DateOuverture || ""} className="input-infos" readOnly />
                        </div>
                        <div className="label-input Compte-1erJanvier">
                            <label>Compte au 01/01/2024</label>
                            <input value={Compte_au_01_01_2024 || ""} className="input-infos" readOnly />
                        </div>
                </div>
            </div>

            {Produits.map((produit, index) => (
                <div className="container-infos-clientproduit" key={index}>
                    <div className="header-infos">
                        <h3>Éléments à comparer {index + 1}</h3>
                    </div>

                    <div className="main-infos-comparaison">
                        <div className="titre-comparaison">
                            <h4 className="titre-fournisseur">Fournisseur (EMT)</h4>
                            <h4 className="titre-client">Client (Fichier data)</h4>
                        </div>
                        <div className="NomProduit-comparaison">
                            <div className="label-input ProduitFournisseur">
                                <div className="container-label-infos">
                                    <label className="label-infos">Produit</label>
                                </div>
                                <input value={produit.ProduitFournisseur || ""} className="input-infos" readOnly />
                            </div>
                            <div className="arrow" />
                            <div className="label-input ProduitClient">
                                <input type="text" value={ProduitClient || ""} className="input-infos" readOnly="readOnly"/>
                                <div className="container-label-infos">
                                    <label className="label-infos"> Produit</label>
                                </div>
                            </div>
                        </div>    
                        <div className="Montant-comparaison">
                            <div className="label-input Compte-1erJanvier">
                                <div className="container-label-infos">
                                    <label className="label-infos">Montant total des encours</label>
                                </div>
                                <input value={produit.FournisseurMontantTotalSouscrit || ""} className="input-infos" readOnly />
                            </div>
                            <div className="arrow" />
                            <div className="label-input Compte-31Decembre">
                                <input value={Compte_au_31_12_2024 || ""} className="input-infos" readOnly />
                                <div className="container-label-infos">
                                    <label className="label-infos">Compte au 31/12/2024</label>
                                </div>
                            </div>
                        </div>
                    </div>



                    <div className="container-button">
                        <button className={EstGenere ? "button-create genere" : "button-create"} onClick={() => load_InfosClient_Fiche(IDClient, produit.IDFournisseur,Region,Bureau,produit.ProduitFournisseur,Nom,Prenom, "Visionner")}>
                            Créer la fiche de reporting
                        </button>
                        <button className={EstGenere ? "button-create genere" : "button-create"} onClick={() => load_InfosClient_Fiche(IDClient, produit.IDFournisseur,Region,Bureau,produit.ProduitFournisseur,Nom,Prenom, "Telecharger")}>
                            Télécharger la fiche de reporting
                        </button>
                    </div>
                </div>
            ))}

        </div>
    );

}
export default ClientProduits