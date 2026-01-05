/*INSINIA*/
select * from fraisexpost.tfichier_clientinsinia_watson;
select * from fraisexpost.tfournisseur_insinia_watsonall;
select * from fraisexpost.tfichier_clientastoria where bureau = 'FIPAGEST';

select EtablissementFournisseur, count(*) from fraisexpost.tfichier_clientastoria where bureau = 'FIPAGEST' group by EtablissementFournisseur order by EtablissementFournisseur;




/*WATSON*/
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
and c.etablissementfournisseur = 'KEYS AM'
order by c.Nom asc;



/*-----FIPAGEST------*/
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
and c.Bureau = 'FIPAGEST'
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
join tfournisseur_eiffel f on c.Produit = f.NomProduit
where (c.dateouverture IS NULL OR c.dateouverture < '2025-01-01')
and c.etablissementfournisseur = 'EIFFEL INVESTMENT GROUP'
and c.Bureau = 'FIPAGEST'
order by c.Nom asc;


/*Corum*/
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
and c.Bureau = 'FIPAGEST'
order by f.ID;
