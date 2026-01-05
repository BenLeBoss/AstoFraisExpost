select * from fraisexpost.tfichier_clientAstoria where nom = 'FAIVRE'; 


/*ASTORIA FINANCE*/
SELECT * FROM fraisexpost.tfournisseur_perial;
SELECT * FROM fraisexpost.tfournisseur_francevalley;
SELECT * FROM fraisexpost.tfournisseur_atlandvoisin;
SELECT * FROM fraisexpost.tfournisseur_corum;
SELECT * FROM fraisexpost.tfournisseur_urbanpremium;
SELECT * FROM fraisexpost.tfournisseur_theoreim;
SELECT * FROM fraisexpost.tfournisseur_smaltcapital;
SELECT * FROM fraisexpost.tfournisseur_keys;
SELECT * FROM fraisexpost.tfournisseur_eiffel;
SELECT * FROM fraisexpost.tfournisseur_normacapital;
SELECT * FROM fraisexpost.tfournisseur_lafrancaise;
SELECT * FROM fraisexpost.tfournisseur_123im;
SELECT * FROM fraisexpost.tfournisseur_alpheys;
SELECT * FROM fraisexpost.tfournisseur_vatel;

                    
/*INSINIA*/
select * from fraisexpost.tfichier_clientinsinia_watson;
select * from fraisexpost.tfournisseur_insinia_watsonall;
select * from fraisexpost.tfichier_clientastoria where bureau = 'FIPAGEST';

    
select * from fraisexpost.tfichier_clientAstoria where Compte_au_31_12_2024 = 0 and Dateouverture < '2025-01-01';
select EtablissementFournisseur, count(*) from tfichier_clientAstoria group by EtablissementFournisseur order by EtablissementFournisseur asc;


/*Fiches générées*/
select  c.ID as IDClient, c.Nom as ClientNom, c.Prenom as ClientPrenom, c.NumeroCompte as ClientNumCompte, c.EtablissementFournisseur as FournisseurNom,
		c.Produit FournisseurProduit, c.Compte_au_31_12_2024 as ClientCompte_31_12 
from tfichier_clientastoria c
where c.EstGenere = True
order by c.Nom;


/*Nouvelle requête PERIAL*/
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
	f.NomProduit as FournisseurNomProduit
from tfournisseur_perial f
join tfichier_clientastoria c on c.NumeroCompte = f.NumeroCompte
where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
and bureau != 'FIPAGEST'
order by c.Description asc;


/*Nouvelle requete FRANCEVALLEY*/
select c.ID as IDClient, 
	c.Nom as ClientNom, 
	c.Prenom as ClientPrenom, 
    c.Region as ClientRegion,
	c.Bureau as ClientBureau, 
	c.Conseiller as ClientConseiller, 
	c.EtablissementFournisseur as ProduitEtablissementFournisseur, 
	c.TypeProduit as ProduitTypeProduit,
	c.Intitule as ProduitIntitule, 
	c.NumeroCompte as ClientProduitNumeroCompte, 
	DATE_FORMAT(c.DateOuverture, '%d/%m/%Y') as ClientProduitDateOuverture, 
	replace(format(c.Compte_au_01_01_2024,2), ',', ' ') as ClientProduitCompte_01_01, 
	replace(format(c.Compte_au_31_12_2024,2), ',', ' ') as ClientProduitCompte_31_12, 
	f.EstGenere as FournisseurEstGenere, 
	c.EstGenere as ClientEstGenere, 
	f.ID as IDFournisseur, 
	c.Produit as ProduitProduit, 
	f.NomProduit as FournisseurNomProduit
from tfournisseur_francevalley f 
join fraisexpost.tfichier_clientastoria c on 
	LOWER(TRIM(REPLACE(f.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci = LOWER(TRIM(REPLACE(c.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci
    AND LOWER(TRIM(REPLACE(f.Prenom, '-', ' '))) COLLATE utf8mb4_unicode_ci = LOWER(TRIM(REPLACE(c.Prenom, '-', ' '))) COLLATE utf8mb4_unicode_ci
where c.EtablissementFournisseur = 'FRANCE VALLEY INVESTISSEMENTS'
and SUBSTRING_INDEX(c.Produit, ' ', -1) = SUBSTRING_INDEX(f.NomProduit, ' ', -1)
and (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
order by f.id asc;


/*Nouvelle requete ATLAND VOISIN*/
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
	c.IDClient as IDClient,
	c.ClientNom as ClientNom,
	c.ClientPrenom as ClientPrenom,
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



/*Nouvelle requete CORUM*/
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
	f.NomProduit as FournisseurNomProduit
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
and
	CASE
      WHEN f.NomProduit LIKE '%XL%' 
				THEN c.Produit = 'SCPI (CORUM XL)' or c.Produit = 'SCPI (CORUM)'
      WHEN f.NomProduit LIKE '%EU%' 
				THEN c.Produit = 'SCPI EURION'
      WHEN f.NomProduit LIKE '%CC%' 
				THEN c.Produit = 'SCPI CORUM ORIGIN' or c.Produit = 'SCPI (CORUM ORIGIN)' or c.Produit = 'SCPI (CORUM)'
      end
order by f.ID;



/*Nouvelle requête Urban Premium*/
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
order by c.Nom asc;


/*Nouvelle requête Theoreim*/
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
order by c.Nom asc;


/*Smalt Capital*/
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
order by c.Nom asc;


/*Keys*/
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
order by c.Nom asc;



/*Eiffel*/
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
join tfournisseur_Eiffel f on c.Produit = f.NomProduit
where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
and c.etablissementfournisseur = 'EIFFEL INVESTMENT GROUP'
order by c.Nom asc;


/*Nouvelle requête Norma*/
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
order by c.Nom asc;



/*Alpheys*/
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
order by c.Nom asc;



/*123Im*/
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
join tfournisseur_123im f on c.Produit = f.NomProduit
where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
and c.etablissementfournisseur = '123 INVESTMENT MANAGERS'
order by c.Nom asc;


/*Vatel*/
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

SELECT *
FROM tfournisseur_vatel f
WHERE NOT EXISTS (
    SELECT 1
    FROM tfichier_clientastoria c
    WHERE 
        LOWER(TRIM(REPLACE(f.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci = LOWER(TRIM(REPLACE(c.Nom, '-', ' '))) COLLATE utf8mb4_unicode_ci
        AND LOWER(TRIM(REPLACE(c.Prenom, '-', ' '))) COLLATE utf8mb4_unicode_ci LIKE CONCAT('%', LOWER(TRIM(REPLACE(f.Prenom, '-', ' '))) COLLATE utf8mb4_unicode_ci, '%')
        AND (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
        AND c.EtablissementFournisseur = 'VATEL CAPITAL'
        AND f.NomProduit = c.Produit
)
ORDER BY f.Nom ASC;


