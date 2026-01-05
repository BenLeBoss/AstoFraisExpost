SELECT * FROM fraisexpost.tfournisseur_perial;
SELECT * FROM fraisexpost.tfournisseur_francevalley;
SELECT * FROM fraisexpost.tfournisseur_atlandvoisin;
SELECT * FROM fraisexpost.tfournisseur_corum;






/*ATLAND VOISIN*/
WITH FournisseurData AS (
  SELECT
    f.ID AS IDFournisseur,
    f.Civilite as FournisseurCivilite, 
    f.Nom AS FournisseurNom,
    f.Prenom AS FournisseurPrenom,
    f.NumeroCompte as FournisseurNumeroCompte,
    f.NomProduit as FournisseurNomProduit,
    f.EstGenere as FournisseurEstGenere,
    ROW_NUMBER() OVER (PARTITION BY f.Nom, f.Prenom, f.NomProduit ORDER BY f.ID) AS rn
  FROM tfournisseur_atlandvoisin f
),
ClientData AS (
  SELECT
    c.ID AS IDClient,
    cp.ID AS IDClientProduit,
    p.ID AS IDProduit,
    c.Nom AS ClientNom,
    c.Prenom AS ClientPrenom,
    c.Bureau as ClientBureau, 
    c.Conseiller as ClientConseiller,
    DATE_FORMAT(cp.DateOuverture, '%d/%m/%Y') as ClientProduitDateOuverture,
    replace(format(cp.Compte_au_01_01_2024,2), ',', ' ') as ClientProduitCompte_01_01, 
    replace(format(cp.Compte_au_31_12_2024,2), ',', ' ') as ClientProduitCompte_31_12,
    p.EtablissementFournisseur as ProduitEtablissementFournisseur, 
    p.TypeProduit as ProduitTypeProduit, 
    p.Produit as ProduitProduit,
    p.Intitule as ProduitIntitule,
    ROW_NUMBER() OVER (PARTITION BY c.Nom, c.Prenom, p.Intitule ORDER BY cp.ID) AS rn
  FROM fraisexpost.tclients c
  JOIN fraisexpost.tclient_produits cp ON c.ID = cp.IDClient
  JOIN fraisexpost.tproduits p ON cp.IDProduit = p.ID
  WHERE p.EtablissementFournisseur = 'ALPHEYS'
  AND cp.dateouverture < '2025-01-01'
)
SELECT 
	f.IDFournisseur as IDFournisseur,
	f.FournisseurCivilite as FournisseurCivilite, 
	f.FournisseurNom as FournisseurNom,
	f.FournisseurPrenom as FournisseurPrenom,
    f.FournisseurNumeroCompte as FournisseurNumeroCompte,
	f.FournisseurNomProduit as FournisseurNomProduit,
	f.FournisseurEstGenere as FournisseurEstGenere,
	c.IDClient as IDClient,
	c.IDClientProduit as IDClientProduit,
	c.IDProduit as IDProduit,
	c.ClientNom as ClientNom,
	c.ClientPrenom as ClientPrenom,
	c.ClientBureau as ClientBureau, 
	c.ClientConseiller as ClientConseiller,
	c.ClientProduitDateOuverture as ClientProduitDateOuverture,
	c.ClientProduitCompte_01_01 as ClientProduitCompte_01_01, 
	c.ClientProduitCompte_31_12 as ClientProduitCompte_31_12,
	c.ProduitEtablissementFournisseur as ProduitEtablissementFournisseur, 
	c.ProduitTypeProduit as ProduitTypeProduit, 
	c.ProduitProduit as ProduitProduit,
	c.ProduitIntitule as ProduitIntitule
FROM FournisseurData f
JOIN ClientData c ON (
  (
    (UPPER(f.FournisseurCivilite) IN ('MONSIEUR', 'MADAME', 'MONSIEUR ET MADAME', 'MR', 'MME') OR f.FournisseurCivilite IS NULL)
    AND LOWER(TRIM(REPLACE(f.FournisseurNom, '-', ' '))) COLLATE utf8mb4_general_ci = LOWER(TRIM(REPLACE(c.ClientNom, '-', ' '))) COLLATE utf8mb4_general_ci
    AND LOWER(TRIM(REPLACE(f.FournisseurPrenom, '-', ' '))) COLLATE utf8mb4_general_ci = LOWER(TRIM(REPLACE(c.ClientPrenom, '-', ' '))) COLLATE utf8mb4_general_ci
  )
  OR
  (
    UPPER(f.FournisseurCivilite) IN ('SCI','SAS','ASSOCIATION', 'SASU')
    AND (
      LOWER(TRIM(REPLACE(CONCAT(f.FournisseurCivilite, ' ', f.FournisseurNom), '-', ' '))) COLLATE utf8mb4_general_ci = LOWER(TRIM(REPLACE(c.ClientNom, '-', ' '))) COLLATE utf8mb4_general_ci
      OR LOWER(TRIM(REPLACE(f.FournisseurNom, '-', ' '))) COLLATE utf8mb4_general_ci = LOWER(TRIM(REPLACE(c.ClientNom, '-', ' '))) COLLATE utf8mb4_general_ci
    )
  )
)
WHERE LOWER(TRIM(c.ProduitIntitule)) like concat ('%', LOWER(TRIM(f.FournisseurNomProduit)), '%')
AND f.rn = c.rn
ORDER BY f.FournisseurNom ASC;






/*FRANCE VALLEY*/
WITH FournisseurData AS (
  SELECT
    f.ID AS IDFournisseur,
    f.Civilite as FournisseurCivilite, 
    f.Nom AS FournisseurNom,
    f.Prenom AS FournisseurPrenom,
    f.NumeroCompte as FournisseurNumeroCompte,
    f.NomProduit as FournisseurNomProduit,
    f.EstGenere as FournisseurEstGenere,
    ROW_NUMBER() OVER (PARTITION BY f.Nom, f.Prenom, f.NomProduit ORDER BY f.ID) AS rn
  FROM tfournisseur_francevalley f
),
ClientData AS (
  SELECT
    c.ID AS IDClient,
    cp.ID AS IDClientProduit,
    p.ID AS IDProduit,
    c.Nom AS ClientNom,
    c.Prenom AS ClientPrenom,
    c.Bureau as ClientBureau, 
    c.Conseiller as ClientConseiller,
    DATE_FORMAT(cp.DateOuverture, '%d/%m/%Y') as ClientProduitDateOuverture,
    replace(format(cp.Compte_au_01_01_2024,2), ',', ' ') as ClientProduitCompte_01_01, 
    replace(format(cp.Compte_au_31_12_2024,2), ',', ' ') as ClientProduitCompte_31_12,
    p.EtablissementFournisseur as ProduitEtablissementFournisseur, 
    p.TypeProduit as ProduitTypeProduit, 
    p.Produit as ProduitProduit,
    p.Intitule as ProduitIntitule,
    ROW_NUMBER() OVER (PARTITION BY c.Nom, c.Prenom, p.Produit ORDER BY cp.ID) AS rn
  FROM fraisexpost.tclients c
  JOIN fraisexpost.tclient_produits cp ON c.ID = cp.IDClient
  JOIN fraisexpost.tproduits p ON cp.IDProduit = p.ID
  WHERE p.EtablissementFournisseur = 'FRANCE VALLEY INVESTISSEMENTS'
  AND cp.dateouverture < '2025-01-01'
)
SELECT 
  f.IDFournisseur as IDFournisseur,
	f.FournisseurCivilite as FournisseurCivilite, 
	f.FournisseurNom as FournisseurNom,
	f.FournisseurPrenom as FournisseurPrenom,
    f.FournisseurNumeroCompte as FournisseurNumeroCompte,
	f.FournisseurNomProduit as FournisseurNomProduit,
	f.FournisseurEstGenere as FournisseurEstGenere,
	c.IDClient as IDClient,
	c.IDClientProduit as IDClientProduit,
	c.IDProduit as IDProduit,
	c.ClientNom as ClientNom,
	c.ClientPrenom as ClientPrenom,
	c.ClientBureau as ClientBureau, 
	c.ClientConseiller as ClientConseiller,
	c.ClientProduitDateOuverture as ClientProduitDateOuverture,
	c.ClientProduitCompte_01_01 as ClientProduitCompte_01_01, 
	c.ClientProduitCompte_31_12 as ClientProduitCompte_31_12,
	c.ProduitEtablissementFournisseur as ProduitEtablissementFournisseur, 
	c.ProduitTypeProduit as ProduitTypeProduit, 
	c.ProduitProduit as ProduitProduit,
	c.ProduitIntitule as ProduitIntitule
FROM FournisseurData f
JOIN ClientData c ON (
  (
    (UPPER(f.FournisseurCivilite) IN ('MONSIEUR', 'MADAME', 'MONSIEUR ET MADAME', 'MR', 'MME') OR f.FournisseurCivilite IS NULL)
    AND LOWER(TRIM(REPLACE(f.FournisseurNom, '-', ' '))) COLLATE utf8mb4_general_ci = LOWER(TRIM(REPLACE(c.ClientNom, '-', ' '))) COLLATE utf8mb4_general_ci
    AND LOWER(TRIM(REPLACE(f.FournisseurPrenom, '-', ' '))) COLLATE utf8mb4_general_ci = LOWER(TRIM(REPLACE(c.ClientPrenom, '-', ' '))) COLLATE utf8mb4_general_ci
  )
  OR
  (
    UPPER(f.FournisseurCivilite) IN ('SCI','SAS','ASSOCIATION', 'SASU')
    AND (
      LOWER(TRIM(REPLACE(CONCAT(f.FournisseurCivilite, ' ', f.FournisseurNom), '-', ' '))) COLLATE utf8mb4_general_ci = LOWER(TRIM(REPLACE(c.ClientNom, '-', ' '))) COLLATE utf8mb4_general_ci
      OR LOWER(TRIM(REPLACE(f.FournisseurNom, '-', ' '))) COLLATE utf8mb4_general_ci = LOWER(TRIM(REPLACE(c.ClientNom, '-', ' '))) COLLATE utf8mb4_general_ci
    )
  )
)
WHERE LOWER(TRIM(c.ProduitProduit)) like concat ('%', LOWER(TRIM(f.FournisseurNomProduit)), '%')
  AND f.rn = c.rn
ORDER BY f.FournisseurNom ASC;



/*PERIAL*/
select c.ID as IDClient, 
c.Nom as ClientNom, 
c.Prenom as ClientPrenom, 
c.Bureau as ClientBureau, 
c.Conseiller as ClientConseiller, 
p.ID as IDProduit, 
p.EtablissementFournisseur as ProduitEtablissementFournisseur, 
p.TypeProduit as ProduitTypeProduit,
p.Produit as ProduitProduit, 
p.Intitule as ProduitIntitule, 
cp.ID as IDClientProduit, 
cp.NumeroCompte as FournisseurNumeroCompte, 
DATE_FORMAT(cp.DateOuverture, '%d/%m/%Y') as ClientProduitDateOuverture, 
replace(format(cp.Compte_au_01_01_2024,2), ',', ' ') as ClientProduitCompte_01_01, 
replace(format(cp.Compte_au_31_12_2024,2), ',', ' ') as ClientProduitCompte_31_12, 
f.EstGenere as FournisseurEstGenere, 
f.ID as IDFournisseur, 
f.NomProduit as FournisseurNomProduit
from tfournisseur_perial f
join tclient_produits cp on cp.NumeroCompte = f.NumeroCompte
join tproduits p on cp.IDProduit = p.id
join tclients c on cp.IDClient = c.id
order by c.Description asc;


/*----------------------------------------------------------------------------------------*/

/*CORUM*/

SELECT Produit, count(*) FROM fraisexpost.tproduits p
where p.EtablissementFournisseur = 'CORUM L''EPARGNE'
group by Produit;


/*----------------------------------------*/
WITH FournisseurData AS (
  SELECT
    f.ID AS IDFournisseur,
    f.Civilite as FournisseurCivilite, 
    f.Nom AS FournisseurNom,
    f.Prenom AS FournisseurPrenom,
    f.NumeroCompte as FournisseurNumeroCompte,
    f.NomProduit as FournisseurNomProduit,
    f.EstGenere as FournisseurEstGenere,
    ROW_NUMBER() OVER (PARTITION BY f.Nom, f.Prenom, f.NomProduit ORDER BY f.ID) AS rn
  FROM tfournisseur_corum f
),
ClientData AS (
  SELECT
    c.ID AS IDClient,
    cp.ID AS IDClientProduit,
    p.ID AS IDProduit,
    c.Nom AS ClientNom,
    c.Prenom AS ClientPrenom,
    c.Bureau as ClientBureau, 
    c.Conseiller as ClientConseiller,
    DATE_FORMAT(cp.DateOuverture, '%d/%m/%Y') as ClientProduitDateOuverture,
    replace(format(cp.Compte_au_01_01_2024,2), ',', ' ') as ClientProduitCompte_01_01, 
    replace(format(cp.Compte_au_31_12_2024,2), ',', ' ') as ClientProduitCompte_31_12,
    p.EtablissementFournisseur as ProduitEtablissementFournisseur, 
    p.TypeProduit as ProduitTypeProduit, 
    p.Produit as ProduitProduit,
    p.Intitule as ProduitIntitule,
    ROW_NUMBER() OVER (PARTITION BY c.Nom, c.Prenom, p.Produit ORDER BY cp.ID) AS rn
  FROM fraisexpost.tclients c
  JOIN fraisexpost.tclient_produits cp ON c.ID = cp.IDClient
  JOIN fraisexpost.tproduits p ON cp.IDProduit = p.ID
  WHERE p.EtablissementFournisseur = 'CORUM L''EPARGNE'
  AND cp.dateouverture < '2025-01-01'
)
SELECT 
  f.IDFournisseur as IDFournisseur,
	f.FournisseurCivilite as FournisseurCivilite, 
	f.FournisseurNom as FournisseurNom,
	f.FournisseurPrenom as FournisseurPrenom,
    f.FournisseurNumeroCompte as FournisseurNumeroCompte,
	f.FournisseurNomProduit as FournisseurNomProduit,
	f.FournisseurEstGenere as FournisseurEstGenere,
	c.IDClient as IDClient,
	c.IDClientProduit as IDClientProduit,
	c.IDProduit as IDProduit,
	c.ClientNom as ClientNom,
	c.ClientPrenom as ClientPrenom,
	c.ClientBureau as ClientBureau, 
	c.ClientConseiller as ClientConseiller,
	c.ClientProduitDateOuverture as ClientProduitDateOuverture,
	c.ClientProduitCompte_01_01 as ClientProduitCompte_01_01, 
	c.ClientProduitCompte_31_12 as ClientProduitCompte_31_12,
	c.ProduitEtablissementFournisseur as ProduitEtablissementFournisseur, 
	c.ProduitTypeProduit as ProduitTypeProduit, 
	c.ProduitProduit as ProduitProduit,
	c.ProduitIntitule as ProduitIntitule
FROM FournisseurData f
JOIN ClientData c ON (
    (UPPER(f.FournisseurCivilite) IN ('MONSIEUR', 'MADAME', 'MONSIEUR ET MADAME', 'MR', 'MME') OR f.FournisseurCivilite IS NULL)
    AND LOWER(TRIM(REPLACE(f.FournisseurNom, '-', ' '))) COLLATE utf8mb4_general_ci = LOWER(TRIM(REPLACE(c.ClientNom, '-', ' '))) COLLATE utf8mb4_general_ci
    AND LOWER(TRIM(REPLACE(f.FournisseurPrenom, '-', ' '))) COLLATE utf8mb4_general_ci = LOWER(TRIM(REPLACE(c.ClientPrenom, '-', ' '))) COLLATE utf8mb4_general_ci
	AND f.rn = c.rn)
ORDER BY f.FournisseurNom ASC;






WITH FournisseurData AS (
  SELECT
    f.ID AS IDFournisseur,
    f.Nom AS FournisseurNom,
    f.Prenom AS FournisseurPrenom,
    f.NomProduit AS FournisseurNomProduit,
    CASE
      WHEN f.NomProduit LIKE '%XL%' THEN 'SCPI (CORUM XL)'
      WHEN f.NomProduit LIKE '%EU%' THEN 'SCPI EURION'
      WHEN f.NomProduit LIKE '%CC%' THEN 'SCPI (CORUM)'
      ELSE f.NomProduit
    END AS ProduitMatch,
    ROW_NUMBER() OVER (
      PARTITION BY f.Nom, f.Prenom,
        CASE
          WHEN f.NomProduit LIKE '%XL%' THEN 'SCPI (CORUM XL)'
          WHEN f.NomProduit LIKE '%EU%' THEN 'SCPI EURION'
          WHEN f.NomProduit LIKE '%CC%' THEN 'SCPI (CORUM)'
          ELSE f.NomProduit
        END
      ORDER BY f.ID
    ) AS rn
  FROM tfournisseur_corum f
),
ClientData AS (
  SELECT
    c.ID AS IDClient,
    c.Nom AS ClientNom,
    c.Prenom AS ClientPrenom,
    p.Produit AS ProduitProduit,
    ROW_NUMBER() OVER (
      PARTITION BY c.Nom, c.Prenom, p.Produit
      ORDER BY c.ID
    ) AS rn
  FROM fraisexpost.tclients c
  JOIN fraisexpost.tclient_produits cp ON c.ID = cp.IDClient
  JOIN fraisexpost.tproduits p ON cp.IDProduit = p.ID
  WHERE p.EtablissementFournisseur = 'CORUM L''EPARGNE'
)
SELECT f.IDFournisseur, f.FournisseurNom, f.FournisseurPrenom, f.FournisseurNomProduit,
       f.ProduitMatch, f.rn
FROM FournisseurData f
LEFT JOIN ClientData c
  ON LOWER(f.FournisseurNom) = LOWER(c.ClientNom)
  AND LOWER(f.FournisseurPrenom) = LOWER(c.ClientPrenom)
  AND LOWER(f.ProduitMatch) = LOWER(c.ProduitProduit)
  AND f.rn = c.rn
WHERE c.IDClient IS NULL;




WITH FournisseurData AS (
                    SELECT
                        f.ID AS IDFournisseur,
                        f.Civilite as FournisseurCivilite, 
                        f.Nom AS FournisseurNom,
                        f.Prenom AS FournisseurPrenom,
                        f.NumeroCompte as FournisseurNumeroCompte,
                        f.NomProduit as FournisseurNomProduit,
                        f.EstGenere as FournisseurEstGenere,
                        ROW_NUMBER() OVER (PARTITION BY f.Nom, f.Prenom, f.NomProduit ORDER BY f.ID) AS rn
                    FROM tfournisseur_atlandvoisin f
                    ),
                    ClientData AS (
                    SELECT
                        c.ID AS IDClient,
                        c.Nom AS ClientNom,
                        c.Prenom AS ClientPrenom,
                        c.NumeroCompte as ClientProduitNumeroCompte,
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
                        c.IDClient as IDClient,
                        c.ClientNom as ClientNom,
                        c.ClientPrenom as ClientPrenom,
                        c.ClientProduitNumeroCompte as ClientProduitNumeroCompte,
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
                    ORDER BY f.FournisseurNom ASC;
