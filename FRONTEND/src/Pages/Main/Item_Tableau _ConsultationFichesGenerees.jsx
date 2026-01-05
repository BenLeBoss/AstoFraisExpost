function Client_Liste_FicheGeneree({ Numero, Nom, Prenom, NumeroCompte, Partenaire, Produit, Compte_31_12}){

    return(
        <tr>
            <td>{Numero}</td>
            <td scope="row">{Nom}</td>
            <td>{Prenom}</td>
            <td>{Partenaire}</td>
            <td>{Produit}</td>
            <td>{NumeroCompte}</td>
            <td>{Compte_31_12}</td>
        </tr>
    );
}
export default Client_Liste_FicheGeneree;