
/* Cette function sert à remplir la liste des partenaires dans la page Fournisseur des entités Insinia */
function Liste_Partenaire_EntitesInsinia(Entite){
    let ListePartenaires = [];

    switch(Entite){
        case "ACTIONPATRIMOINE":
            return ListePartenaires;

        case "ALLUREFINANCE":
            return ListePartenaires;

        case "BCFINANCES":
            return ListePartenaires;

        case "CAPIUM":
            return ListePartenaires;

        case "FAMILYPATRIMOINE":
            ListePartenaires.push(
                { Libelle: "Atland-Voisin", Nom: "ATLAND-VOISIN" },
                { Libelle: "La Française", Nom: "LA FRANCAISE REAL ESTATE MANAGERS" },
                { Libelle: "France Valley", Nom: "FRANCE VALLEY INVESTISSEMENTS" }
            );
            return ListePartenaires;

        case "FIPAGEST":
            ListePartenaires.push(
                { Libelle: "123IM", Nom: "123 INVESTMENT MANAGERS" },
                { Libelle: "Alpheys", Nom: "ALPHEYS" },
                { Libelle: "Eiffel", Nom: "EIFFEL INVESTMENT GROUP" },
                { Libelle: "La Française", Nom: "LA FRANCAISE AM" },
                { Libelle: "Primonial", Nom: "PRIMONIAL" },
                { Libelle: "Xerys", Nom: "XERYS INVEST" }
            );
            return ListePartenaires;

        case "MYFAMILYOFFICER":
            return ListePartenaires;

        case "PARISII":
            return ListePartenaires;

        case "SOLVEPATRIMOINE":
            return ListePartenaires;

        case "SYNERGIECONSEILSPATRIMOINE":
            ListePartenaires.push(
                { Libelle: "La Française", Nom: "LA FRANCAISE AM" },
                { Libelle: "LBO", Nom: "LBO FRANCE GESTION" },
                { Libelle: "Paref", Nom: "PAREF GESTION" },
                { Libelle: "Primonial", Nom: "PRIMONIAL" },
                { Libelle: "Sofidy", Nom: "SOFIDY" },
            );
            return ListePartenaires;

        case "WATSONPATRIMOINE":
            ListePartenaires.push({ Libelle: "Keys", Nom: "KEYS AM" });
            return ListePartenaires;

        default:
            return ListePartenaires;

    }
}export default Liste_Partenaire_EntitesInsinia;