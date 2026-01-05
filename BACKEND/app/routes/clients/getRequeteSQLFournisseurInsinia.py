

def getRequeteSQLFournisseurInsinia(Table, Partenaire):

    match(Table):

        # ----------- WATSON
        case 'tfichier_clientinsinia_watson':
            return """
                    select c.ID as IDClient, 
                        f.ID as IDFournisseur,
                        c.Nom as ClientNom, 
                        c.Prenom as ClientPrenom, 
                        c.Region as ClientRegion,
                        c.Bureau as ClientBureau, 
                        c.Conseiller as ClientConseiller, 
                        c.EtablissementFournisseur as ProduitEtablissementFournisseur, 
                        c.TypeProduit as ProduitTypeProduit,
                        c.Produit as ProduitProduit, 
                        c.Intitule as ProduitIntitule, 
                        c.NumeroCompte as ClientProduitNumeroCompte, 
                        DATE_FORMAT(c.DateOuverture, '%d/%m/%Y') as ClientProduitDateOuverture, 
                        replace(format(c.Compte_au_01_01_2024,2), ',', ' ') as ClientProduitCompte_01_01, 
                        replace(format(c.Compte_au_31_12_2024,2), ',', ' ') as ClientProduitCompte_31_12, 
                        f.EstGenere as FournisseurEstGenere, 
                        c.EstGenere as ClientEstGenere,  
                        f.NomProduit as FournisseurNomProduit,
                        f.MontantTotalSouscrit as FournisseurMontantTotalSouscrit
                    from tfichier_clientinsinia_watson c
                    join tfournisseur_insinia_watsonall f on 
                        LOWER(TRIM(c.Produit)) like concat ('%', LOWER(TRIM(f.NomProduit)), '%')
                    where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                    and c.etablissementfournisseur = %s
                    order by c.Nom asc;
            """
            

        # ----------- FIPAGEST
        case 'tfichier_clientastoria':
            match(Partenaire):
                case "123 INVESTMENT MANAGERS":
                    return """

                    """

                case "ALPHEYS":
                    return """
                        select c.ID as IDClient, 
                            f.ID as IDFournisseur,
                            c.Nom as ClientNom, 
                            c.Prenom as ClientPrenom, 
                            c.Region as ClientRegion,
                            c.Bureau as ClientBureau, 
                            c.Conseiller as ClientConseiller, 
                            c.EtablissementFournisseur as ProduitEtablissementFournisseur, 
                            c.TypeProduit as ProduitTypeProduit,
                            c.Produit as ProduitProduit, 
                            c.Intitule as ProduitIntitule, 
                            c.NumeroCompte as ClientProduitNumeroCompte, 
                            DATE_FORMAT(c.DateOuverture, '%d/%m/%Y') as ClientProduitDateOuverture, 
                            replace(format(c.Compte_au_01_01_2024,2), ',', ' ') as ClientProduitCompte_01_01, 
                            replace(format(c.Compte_au_31_12_2024,2), ',', ' ') as ClientProduitCompte_31_12, 
                            f.EstGenere as FournisseurEstGenere, 
                            c.EstGenere as ClientEstGenere,  
                            f.NomProduit as FournisseurNomProduit,
                            f.MontantTotalSouscrit as FournisseurMontantTotalSouscrit
                        from tfichier_clientastoria c
                        join tfournisseur_alpheys f on c.Produit like concat('%',f.NomProduit,'%')
                        where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                        and c.etablissementfournisseur = %s
                        and c.Bureau = 'FIPAGEST'
                        and f.ID = %s
                        order by c.Nom asc;
                    """
                
                case "CORUM L'EPARGNE":
                    return """

                    """
                
                case "EIFFEL INVESTMENT GROUP" :
                    return """
                        select c.ID as IDClient, 
                            f.ID as IDFournisseur,
                            c.Nom as ClientNom, 
                            c.Prenom as ClientPrenom, 
                            c.Region as ClientRegion,
                            c.Bureau as ClientBureau, 
                            c.Conseiller as ClientConseiller, 
                            c.EtablissementFournisseur as ProduitEtablissementFournisseur, 
                            c.TypeProduit as ProduitTypeProduit,
                            c.Produit as ProduitProduit, 
                            c.Intitule as ProduitIntitule, 
                            c.NumeroCompte as ClientProduitNumeroCompte, 
                            DATE_FORMAT(c.DateOuverture, '%d/%m/%Y') as ClientProduitDateOuverture, 
                            replace(format(c.Compte_au_01_01_2024,2), ',', ' ') as ClientProduitCompte_01_01, 
                            replace(format(c.Compte_au_31_12_2024,2), ',', ' ') as ClientProduitCompte_31_12, 
                            f.EstGenere as FournisseurEstGenere, 
                            c.EstGenere as ClientEstGenere,  
                            f.NomProduit as FournisseurNomProduit,
                            f.MontantTotalSouscrit as FournisseurMontantTotalSouscrit
                        from tfichier_clientastoria c
                        join tfournisseur_eiffel f on c.Produit = f.NomProduit
                        where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                        and c.etablissementfournisseur = %s
                        and c.Bureau = 'FIPAGEST'
                        order by c.Nom asc;
                    """
                
                case "LA FRANCAISE AM":
                    return """
                        select c.ID as IDClient, 
                            f.ID as IDFournisseur,
                            c.Nom as ClientNom, 
                            c.Prenom as ClientPrenom, 
                            c.Region as ClientRegion,
                            c.Bureau as ClientBureau, 
                            c.Conseiller as ClientConseiller, 
                            c.EtablissementFournisseur as ProduitEtablissementFournisseur, 
                            c.TypeProduit as ProduitTypeProduit,
                            c.Produit as ProduitProduit, 
                            c.Intitule as ProduitIntitule, 
                            c.NumeroCompte as ClientProduitNumeroCompte, 
                            DATE_FORMAT(c.DateOuverture, '%d/%m/%Y') as ClientProduitDateOuverture, 
                            replace(format(c.Compte_au_01_01_2024,2), ',', ' ') as ClientProduitCompte_01_01, 
                            replace(format(c.Compte_au_31_12_2024,2), ',', ' ') as ClientProduitCompte_31_12, 
                            f.EstGenere as FournisseurEstGenere, 
                            c.EstGenere as ClientEstGenere,  
                            f.NomProduit as FournisseurNomProduit,
                            f.MontantTotalSouscrit as FournisseurMontantTotalSouscrit
                        from tfichier_clientastoria c
                        join tfournisseur_lafrancaise f on c.Produit like concat('%', f.NomProduit, '%')
                        where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                        and c.etablissementfournisseur = %s
                        and c.Produit not like '%/%'
                        and c.bureau = 'FIPAGEST'
                        order by c.Nom asc;
                    """
                
                case "NORTIA":
                    return """

                    """
                
                case "PRIMONIAL":
                    return """
                        select c.ID as IDClient, 
                            f.ID as IDFournisseur,
                            c.Nom as ClientNom, 
                            c.Prenom as ClientPrenom, 
                            c.Region as ClientRegion,
                            c.Bureau as ClientBureau, 
                            c.Conseiller as ClientConseiller, 
                            c.EtablissementFournisseur as ProduitEtablissementFournisseur, 
                            c.TypeProduit as ProduitTypeProduit,
                            c.Produit as ProduitProduit, 
                            c.Intitule as ProduitIntitule, 
                            c.NumeroCompte as ClientProduitNumeroCompte, 
                            DATE_FORMAT(c.DateOuverture, '%d/%m/%Y') as ClientProduitDateOuverture, 
                            replace(format(c.Compte_au_01_01_2024,2), ',', ' ') as ClientProduitCompte_01_01, 
                            replace(format(c.Compte_au_31_12_2024,2), ',', ' ') as ClientProduitCompte_31_12, 
                            f.EstGenere as FournisseurEstGenere, 
                            c.EstGenere as ClientEstGenere,  
                            f.NomProduit as FournisseurNomProduit,
                            f.MontantTotalSouscrit as FournisseurMontantTotalSouscrit
                        from tfichier_clientastoria c
                        join tfournisseur_primonial f on c.Produit like concat('%', f.NomProduit, '%')
                        where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                        and c.etablissementfournisseur = %s
                        and c.bureau = 'FIPAGEST'
                        order by c.Nom asc;
                    """
                
                case "XERYS INVEST":
                    return """

                    """
                

        # ----------- SYNERGIE
        case 'tfichier_clientinsinia_synergieconseilspatrimoine':
            return """
                    select c.ID as IDClient, 
                        f.ID as IDFournisseur,
                        c.Nom as ClientNom, 
                        c.Prenom as ClientPrenom, 
                        c.Region as ClientRegion,
                        c.Bureau as ClientBureau, 
                        c.Conseiller as ClientConseiller, 
                        c.EtablissementFournisseur as ProduitEtablissementFournisseur, 
                        c.TypeProduit as ProduitTypeProduit,
                        c.Produit as ProduitProduit, 
                        c.Intitule as ProduitIntitule, 
                        c.NumeroCompte as ClientProduitNumeroCompte, 
                        DATE_FORMAT(c.DateOuverture, '%d/%m/%Y') as ClientProduitDateOuverture, 
                        replace(format(c.Compte_au_01_01_2024,2), ',', ' ') as ClientProduitCompte_01_01, 
                        replace(format(c.Compte_au_31_12_2024,2), ',', ' ') as ClientProduitCompte_31_12, 
                        f.EstGenere as FournisseurEstGenere, 
                        c.EstGenere as ClientEstGenere,  
                        f.NomProduit as FournisseurNomProduit,
                        f.MontantTotalSouscrit as FournisseurMontantTotalSouscrit
                    from tfichier_clientinsinia_synergieconseilspatrimoine c
                    join tfournisseur_insinia_synergieconseilspatrimoineall f on LOWER(TRIM(c.intitule)) like concat('%',LOWER(TRIM(f.NomProduit)),'%')
                    where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                    and c.etablissementfournisseur = %s
                    and produit != 'GFV (LA FRANCAISE AM)'
                    order by c.Nom asc;
            """        
        

        # ----------- FAMILY PATRIMOINE
        case 'tfichier_clientinsinia_familypatrimoine':
            return """
                select c.ID as IDClient, 
                    f.ID as IDFournisseur,
                    c.Nom as ClientNom, 
                    c.Prenom as ClientPrenom, 
                    c.Region as ClientRegion,
                    c.Bureau as ClientBureau, 
                    c.Conseiller as ClientConseiller, 
                    c.EtablissementFournisseur as ProduitEtablissementFournisseur, 
                    c.TypeProduit as ProduitTypeProduit,
                    c.Produit as ProduitProduit, 
                    c.Intitule as ProduitIntitule, 
                    c.NumeroCompte as ClientProduitNumeroCompte, 
                    DATE_FORMAT(c.DateOuverture, '%d/%m/%Y') as ClientProduitDateOuverture, 
                    replace(format(c.Compte_au_01_01_2024,2), ',', ' ') as ClientProduitCompte_01_01, 
                    replace(format(c.Compte_au_31_12_2024,2), ',', ' ') as ClientProduitCompte_31_12, 
                    f.EstGenere as FournisseurEstGenere, 
                    c.EstGenere as ClientEstGenere,  
                    f.NomProduit as FournisseurNomProduit,
                    f.MontantTotalSouscrit as FournisseurMontantTotalSouscrit
                from tfichier_clientinsinia_familypatrimoine c
                join tfournisseur_insinia_familypatrimoineall f on LOWER(TRIM(c.intitule)) like concat('%',LOWER(TRIM(f.NomProduit)),'%')
                where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                and c.etablissementfournisseur = %s
                order by c.Nom asc;
            """


        case _ :
            raise ValueError(f"Table inconnue : {Table}")