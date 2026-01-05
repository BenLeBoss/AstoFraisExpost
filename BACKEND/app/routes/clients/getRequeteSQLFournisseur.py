

def getRequeteSQLFournisseur(Table):

    match(Table):

        # ----------- PERIAL
        case 'tfournisseur_perial':
            return """
                    select c.ID as IDClient, 
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
                        f.ID as IDFournisseur, 
                        f.NomProduit as FournisseurNomProduit,
                        replace(format(f.MontantTotalSouscrit,2), ',', ' ') as FournisseurMontantTotalSouscrit
                    from tfournisseur_perial f
                    join tfichier_clientastoria c on c.NumeroCompte = f.NumeroCompte
                    where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                    and bureau != 'FIPAGEST'
                    order by c.Description asc;
            """
        
        # ----------- FRANCE VALLEY
        case 'tfournisseur_francevalley':
            return """
                    select c.ID as IDClient, 
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
                        f.ID as IDFournisseur, 
                        f.NomProduit as FournisseurNomProduit,
                        replace(format(f.MontantTotalSouscrit,2), ',', ' ') as FournisseurMontantTotalSouscrit
                    from tfournisseur_francevalley f 
                    join fraisexpost.tfichier_clientastoria c on 
                        LOWER(TRIM(REPLACE(f.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci = LOWER(TRIM(REPLACE(c.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci
                        AND LOWER(TRIM(REPLACE(f.Prenom, '-', ' '))) COLLATE utf8mb4_unicode_ci = LOWER(TRIM(REPLACE(c.Prenom, '-', ' '))) COLLATE utf8mb4_unicode_ci
                    where c.EtablissementFournisseur = 'FRANCE VALLEY INVESTISSEMENTS'
                    /*and f.NomProduit = c.Produit*/
                    and SUBSTRING_INDEX(c.Produit, ' ', -1) = SUBSTRING_INDEX(f.NomProduit, ' ', -1)
                    and (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                    and bureau != 'FIPAGEST'
                    order by f.id asc;
            """
        
        # ----------- ATLAND VOISIN
        case 'tfournisseur_atlandvoisin':
            return """
                    WITH FournisseurData AS (
                        SELECT
                            f.ID AS IDFournisseur,
                            f.Civilite as FournisseurCivilite, 
                            f.Nom AS FournisseurNom,
                            f.Prenom AS FournisseurPrenom,
                            f.NumeroCompte as FournisseurNumeroCompte,
                            f.NomProduit as FournisseurNomProduit,
                            f.EstGenere as FournisseurEstGenere,
                            replace(format(f.MontantTotalSouscrit,2), ',', ' ') as MontantTotalSouscrit,
                            ROW_NUMBER() OVER (PARTITION BY f.Nom, f.Prenom, f.NomProduit ORDER BY f.ID) AS rn
                        FROM tfournisseur_atlandvoisin f
                        ),
                    ClientData AS (
                        SELECT
                            c.ID AS IDClient,
                            c.Nom AS ClientNom,
                            c.Prenom AS ClientPrenom,
                            c.NumeroCompte as ClientProduitNumeroCompte,
                            c.Region as ClientRegion,
                            c.Bureau as ClientBureau, 
                            c.Conseiller as ClientConseiller,
                            DATE_FORMAT(c.DateOuverture, '%d/%m/%Y') as ClientProduitDateOuverture,
                            replace(format(c.Compte_au_01_01_2024,2), ',', ' ') as ClientProduitCompte_01_01, 
                            replace(format(c.Compte_au_31_12_2024,2), ',', ' ') as ClientProduitCompte_31_12,
                            c.EtablissementFournisseur as ProduitEtablissementFournisseur, 
                            c.TypeProduit as ProduitTypeProduit, 
                            c.Produit as ProduitProduit,
                            c.Intitule as ProduitIntitule,
                            c.EstGenere as ClientEstGenere, 
                            ROW_NUMBER() OVER (PARTITION BY c.Nom, c.Prenom, c.Intitule ORDER BY c.ID) AS rn
                        FROM fraisexpost.tfichier_clientastoria c
                        WHERE c.EtablissementFournisseur = 'ALPHEYS'
                        AND (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                        )
                    SELECT 
                            f.IDFournisseur as IDFournisseur,
                            f.FournisseurCivilite as FournisseurCivilite, 
                            f.FournisseurNom as FournisseurNom,
                            f.FournisseurPrenom as FournisseurPrenom,
                            f.FournisseurNumeroCompte as FournisseurNumeroCompte,
                            f.FournisseurNomProduit as FournisseurNomProduit,
                            f.FournisseurEstGenere as FournisseurEstGenere,
                            f.MontantTotalSouscrit as FournisseurMontantTotalSouscrit,
                            c.IDClient as IDClient,
                            c.ClientNom as ClientNom,
                            c.ClientPrenom as ClientPrenom,
                            c.ClientProduitNumeroCompte as ClientProduitNumeroCompte,
                            c.ClientRegion as ClientRegion,
                            c.ClientBureau as ClientBureau, 
                            c.ClientConseiller as ClientConseiller,
                            c.ClientProduitDateOuverture as ClientProduitDateOuverture,
                            c.ClientProduitCompte_01_01 as ClientProduitCompte_01_01, 
                            c.ClientProduitCompte_31_12 as ClientProduitCompte_31_12,
                            c.ProduitEtablissementFournisseur as ProduitEtablissementFournisseur, 
                            c.ProduitTypeProduit as ProduitTypeProduit, 
                            c.ProduitProduit as ProduitProduit,
                            c.ProduitIntitule as ProduitIntitule,
                            c.ClientEstGenere as ClientEstGenere
                    FROM FournisseurData f
                    JOIN ClientData c ON (
                    (
                            (UPPER(f.FournisseurCivilite) IN ('MONSIEUR', 'MADAME', 'MONSIEUR ET MADAME', 'MR', 'MME') OR f.FournisseurCivilite IS NULL)
                            AND LOWER(TRIM(REPLACE(f.FournisseurNom, '-', ' '))) COLLATE utf8mb4_unicode_ci = LOWER(TRIM(REPLACE(c.ClientNom, '-', ' '))) COLLATE utf8mb4_unicode_ci
                            AND LOWER(TRIM(REPLACE(f.FournisseurPrenom, '-', ' '))) COLLATE utf8mb4_unicode_ci = LOWER(TRIM(REPLACE(c.ClientPrenom, '-', ' '))) COLLATE utf8mb4_unicode_ci
                    )
                    OR
                    (
                            UPPER(f.FournisseurCivilite) IN ('SCI','SAS','ASSOCIATION', 'SASU')
                            AND (
                            LOWER(TRIM(REPLACE(CONCAT(f.FournisseurCivilite, ' ', f.FournisseurNom), '-', ' '))) COLLATE utf8mb4_unicode_ci = LOWER(TRIM(REPLACE(c.ClientNom, '-', ' '))) COLLATE utf8mb4_unicode_ci
                            OR LOWER(TRIM(REPLACE(f.FournisseurNom, '-', ' '))) COLLATE utf8mb4_unicode_ci = LOWER(TRIM(REPLACE(c.ClientNom, '-', ' '))) COLLATE utf8mb4_unicode_ci
                            )
                        )
                    )
                    WHERE LOWER(TRIM(c.ProduitIntitule)) like concat ('%', LOWER(TRIM(f.FournisseurNomProduit)), '%')
                    AND f.rn = c.rn
                    AND c.ClientBureau != 'FIPAGEST'
                    ORDER BY f.FournisseurNom ASC;
            """
        
        # ----------- ATLAND VOISIN 2 
        case 'tfournisseur_atlandvoisin2':
            print("dednas")
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
                    join tfournisseur_atlandvoisin2 f on c.Intitule like concat('%', f.NomProduit, '%')
                    where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                    and c.etablissementfournisseur = 'ATLAND-VOISIN'
                    and c.bureau != 'fipagest'
                    order by c.Nom asc;
            """
        
        # ----------- CORUM
        case 'tfournisseur_corum':
            return """
                    select c.ID as IDClient, 
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
                        f.ID as IDFournisseur, 
                        f.NomProduit as FournisseurNomProduit,
                        replace(format(f.MontantTotalSouscrit,2), ',', ' ') as FournisseurMontantTotalSouscrit
                    from tfournisseur_corum f 
                    join tfichier_clientastoria c on (
                            (UPPER(f.Civilite) IN ('MONSIEUR', 'MADAME', 'MONSIEUR ET MADAME', 'MR', 'MME'))
                            AND LOWER(TRIM(REPLACE(f.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci  = LOWER(TRIM(REPLACE(c.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci 
                            AND LOWER(TRIM(REPLACE(c.Prenom, '-', ' '))) COLLATE utf8mb4_unicode_ci like concat('%', LOWER(TRIM(REPLACE(f.Prenom, '-', ' '))) COLLATE utf8mb4_unicode_ci, '%') )
                        OR (
                            (UPPER(f.Civilite) IN ('SCI','SAS','ASSOCIATION', 'SASU', 'HOLDING')  OR f.Civilite IS NULL)
                            AND (LOWER(TRIM(REPLACE(CONCAT(f.Civilite, ' ', f.Nom), '-', ' '))) COLLATE utf8mb4_general_ci = LOWER(TRIM(REPLACE(c.Nom, '-', ' '))) COLLATE utf8mb4_general_ci
                            OR LOWER(TRIM(REPLACE(f.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci  = LOWER(TRIM(REPLACE(c.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci  )
                        )
                    where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                        AND
                            CASE
                            WHEN f.NomProduit LIKE '%XL%' 
                                        THEN c.Produit = 'SCPI (CORUM XL)' or c.Produit = 'SCPI (CORUM)'
                            WHEN f.NomProduit LIKE '%EU%' 
                                        THEN c.Produit = 'SCPI EURION'
                            WHEN f.NomProduit LIKE '%CC%' 
                                        THEN c.Produit = 'SCPI CORUM ORIGIN' or c.Produit = 'SCPI (CORUM ORIGIN)' or c.Produit = 'SCPI (CORUM)'
                            end
                        AND bureau != 'FIPAGEST'
                    order by f.ID;
            """
        
        # ----------- URBAN PREMIUM
        case 'tfournisseur_urbanpremium' :
            return """
                    select c.ID as IDClient, 
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
                        f.ID as IDFournisseur, 
                        f.NomProduit as FournisseurNomProduit,
                        f.MontantTotalSouscrit as FournisseurMontantTotalSouscrit
                    from tfournisseur_urbanpremium f
                    join tfichier_clientastoria c on LOWER(TRIM(REPLACE(f.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci  = LOWER(TRIM(REPLACE(c.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci 
                                                    AND LOWER(TRIM(REPLACE(c.Prenom, '-', ' '))) COLLATE utf8mb4_unicode_ci like concat('%', LOWER(TRIM(REPLACE(f.Prenom, '-', ' '))) COLLATE utf8mb4_unicode_ci, '%')
                    where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                    and EtablissementFournisseur = 'URBAN PREMIUM'
                    and bureau != 'FIPAGEST'
                    order by c.Nom asc;
            """
        
        # ----------- THEOREIM
        case 'tfournisseur_theoreim' :
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
                    from tfournisseur_theoreim f
                    join tfichier_clientastoria c on (
                            (UPPER(f.Civilite) IN ('MONSIEUR', 'MADAME', 'MONSIEUR ET MADAME', 'MR', 'MME'))
                            AND LOWER(TRIM(REPLACE(f.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci  = LOWER(TRIM(REPLACE(c.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci 
                            AND LOWER(TRIM(REPLACE(c.Prenom, '-', ' '))) COLLATE utf8mb4_unicode_ci like concat('%', LOWER(TRIM(REPLACE(f.Prenom, '-', ' '))) COLLATE utf8mb4_unicode_ci, '%') )
                        OR (
                            (UPPER(f.Civilite) IN ('SCI','SAS','ASSOCIATION', 'SASU', 'HOLDING')  OR f.Civilite IS NULL)
                            AND (LOWER(TRIM(REPLACE(CONCAT(f.Civilite, ' ', f.Nom), '-', ' '))) COLLATE utf8mb4_general_ci = LOWER(TRIM(REPLACE(c.Nom, '-', ' '))) COLLATE utf8mb4_general_ci
                            OR LOWER(TRIM(REPLACE(f.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci  = LOWER(TRIM(REPLACE(c.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci  )
                        )
                    where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                    /*Le produit Theoreim est LOG IN*/
                    and f.nomproduit = c.produit
                    and bureau != 'FIPAGEST'
                    order by c.Nom asc;
            """
        
        # ----------- SMALT CAPITAL
        case 'tfournisseur_smaltcapital' :
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
                    join tfournisseur_smaltcapital f on (c.Produit like concat ('%', substring_index(f.NomProduit,' ',1), '%'))
                    where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                    and c.etablissementfournisseur = 'SMALT CAPITAL'
                    and bureau != 'FIPAGEST'
                    order by c.Nom asc;
            """
        
        # ----------- KEYS
        case 'tfournisseur_keys' :
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
                    join tfournisseur_keys f on (c.EtablissementFournisseur like concat ('%', substring_index(f.NomProduit,' ',1), '%'))
                    where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                    and c.etablissementfournisseur = 'KEYS AM'
                    and bureau != 'FIPAGEST'
                    order by c.Nom asc;
            """
        
        # ----------- EIFFEL
        case 'tfournisseur_eiffel' :
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
                    and c.etablissementfournisseur = 'EIFFEL INVESTMENT GROUP'
                    and bureau != 'FIPAGEST'
                    order by c.Nom asc;
            """
        
        # ----------- NORMA CAPITAL
        case 'tfournisseur_normacapital' :
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
                    from tfournisseur_normacapital f
                    join tfichier_clientastoria c on (
                            (LOWER(TRIM(REPLACE(CONCAT(f.Civilite, ' ', f.Nom), '-', ' '))) COLLATE utf8mb4_general_ci = LOWER(TRIM(REPLACE(c.Nom, '-', ' '))) COLLATE utf8mb4_general_ci
                            OR LOWER(TRIM(REPLACE(f.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci  = LOWER(TRIM(REPLACE(c.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci  )
                        )
                    where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                    and EtablissementFournisseur = 'NORMA CAPITAL'
                    and bureau != 'FIPAGEST'
                    order by c.Nom asc;
            """
        
        # ----------- ALPHEYS
        case 'tfournisseur_alpheys' :
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
                    and c.etablissementfournisseur = 'ALPHEYS'
                    and bureau != 'FIPAGEST'
                    and f.ID = %s
                    order by c.Nom asc;
            """
        
        # ----------- VATEL
        case 'tfournisseur_vatel' :
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
                    from tfournisseur_vatel f
                    join tfichier_clientastoria c on (
                            LOWER(TRIM(REPLACE(f.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci  = LOWER(TRIM(REPLACE(c.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci 
                            AND LOWER(TRIM(REPLACE(c.Prenom, '-', ' '))) COLLATE utf8mb4_unicode_ci like concat('%', LOWER(TRIM(REPLACE(f.Prenom, '-', ' '))) COLLATE utf8mb4_unicode_ci, '%') 
                        )
                    where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                    and c.EtablissementFournisseur = 'VATEL CAPITAL'
                    and f.NomProduit = c.Produit
                    order by c.Nom asc;
            """
        

        # ----------- SOFIDY
        case 'tfournisseur_sofidy' :
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
                    join tfournisseur_sofidy f on c.Intitule = f.NomProduit
                    where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                    and c.etablissementfournisseur = 'SOFIDY'
                    and c.bureau != 'FIPAGEST'
                    order by c.Nom asc;
            """
        

        # ----------- PAREF
        case 'tfournisseur_paref' :
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
                join tfournisseur_paref f on c.Intitule like concat('%', f.NomProduit, '%')
                where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
                and c.etablissementfournisseur = 'PAREF GESTION'
                and c.bureau != 'FIPAGEST'
                order by c.Nom asc;
            """
        


        # ----------- PRIMONIAL
        case 'tfournisseur_primonial' :
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
                and c.etablissementfournisseur = 'PRIMONIAL'
                and c.bureau != 'FIPAGEST'
                order by c.Nom asc;
            """
        


        # ----------- LA FRANCAISE
        case 'tfournisseur_lafrancaise' :
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
                    and c.etablissementfournisseur = 'LA FRANCAISE AM'
                    and c.Produit not like '%/%'
                    and c.bureau != 'FIPAGEST'
                    order by c.Nom asc;
            """



        case _ :
            raise ValueError(f"Table inconnue : {Table}")