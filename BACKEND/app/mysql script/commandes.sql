SELECT * FROM fraisexpost.tclients where Nom = 'PERROZET';

SELECT * from fraisexpost.tproduits;

SELECT * FROM fraisexpost.Tclient_produits;




/*Theoreim*/
select * from fraisexpost.tproduits p 
join fraisexpost.tclient_produits cp on p.ID = cp.IDProduit
join fraisexpost.tclients c on c.ID = cp.IDClient
where p.produit = 'Log in'
and cp.dateouverture < '2025-01-01'
order by c.Nom;



/*fiches générées*/
SELECT * FROM fraisexpost.tclients c
JOIN fraisexpost.tclient_produits cp on c.ID = cp.IDClient
JOIN fraisexpost.tproduits p on cp.IDProduit = p.ID
JOIN fraisexpost.tfournisseur_perial f on cp.NumeroCompte = f.NumeroCompte
WHERE f.EstGenere = true
ORDER BY c.Nom;        


SELECT * FROM fraisexpost.tfournisseur_francevalley f
join fraisexpost.tclients c on f.Nom = c.Nom and f.Prenom = c.Prenom 
and f.EstGenere = true
ORDER BY f.Nom;      


/*REQUETE A UTILISEE*/
select  c.ID as IDClient, p.ID as IDProduit, cp.ID as IDClientProduit, fv.ID as IDFournisseur, 
        c.Nom as ClientNom, c.Prenom as ClientPrenom, cp.NumeroCompte as ClientNumCompte, p.EtablissementFournisseur as FournisseurNom,
        fv.NomProduit FournisseurProduit, cp.Compte_au_31_12_2024 as ClientCompte_31_12 
from tclients c, tclient_produits cp, tproduits p,  tfournisseur_francevalley fv
where c.ID = cp.IDClient
and cp.IDProduit = p.ID
and p.EtablissementFournisseur = 'FRANCE VALLEY INVESTISSEMENTS'
and c.Nom = fv.Nom
and c.Prenom = fv.Prenom
and fv.NomProduit = p.Produit
and fv.EstGenere = True
order by c.Nom;


/*------------------------------ PERIAL ----------------------------------*/

/*permet de faire matcher les numéros de compte dans la table fournisseur PERIAL et ceux contenus dans la table tClientProduit*/
SELECT distinct cp.NumeroCompte, f.Nom, f.Prenom, f.ID as PerialID, c.ID AS ClientID, cp.ID as ClientProduitID
FROM fraisexpost.tfournisseur_perial f
JOIN fraisexpost.tclient_produits cp ON cp.NumeroCompte = f.NumeroCompte
JOIN fraisexpost.tproduits p ON cp.IDProduit = p.ID
JOIN fraisexpost.tclients c ON cp.IDClient = c.ID
WHERE p.EtablissementFournisseur LIKE '%perial%';


/*permet de trouver les éléments qui n'ont pas matcher*/
SELECT DISTINCT f.NumeroCompte, f.Nom, f.Prenom, f.ID AS PerialID
FROM fraisexpost.tfournisseur_perial f
LEFT JOIN fraisexpost.tclient_produits cp ON cp.NumeroCompte = f.NumeroCompte
LEFT JOIN fraisexpost.tproduits p ON cp.IDProduit = p.ID AND p.EtablissementFournisseur LIKE '%perial%'
LEFT JOIN fraisexpost.tclients c ON cp.IDClient = c.ID
WHERE cp.ID IS NULL;

Select f.TypeFrais1_eu, f.TypeFrais1_p, f.TypeFrais2_eu, f.TypeFrais2_p, f.TypeFrais3_eu, f.TypeFrais3_p from tfournisseur_perial f
join tclient_produits cp on f.NumeroCompte = cp.NumeroCompte
join tclients c on cp.IDClient = c.ID
where f.NumeroCompte = '378009';

Select cp.NumeroCompte as Client_NumCompte, c.Nom as ClientNom, c.Prenom as ClientPrenom, cp.Compte_au_01_01_2024, cp.Compte_au_31_12_2024, p.Produit as Produit, p.Intitule,
f.NumeroCompte as Fournisseur_NumCompte, f.Nom as FournisseurNom, f.Prenom as FournisseurPrenom, f.NomProduit as FournisseurProduit
from tfournisseur_perial f
join tclient_produits cp on f.NumeroCompte = cp.NumeroCompte
join tproduits p on p.ID = cp.IDProduit
join tclients c on cp.IDClient = c.ID;

/*requete pour trouver les doubles lignes dans le fichier EMT Perial quand il n'y a qu'une seule ligne dans le fichier client*/
SELECT *
FROM tfournisseur_perial f
JOIN tclient_produits cp ON cp.NumeroCompte = f.NumeroCompte
WHERE f.NumeroCompte IN (
    SELECT NumeroCompte
    FROM tfournisseur_perial
    GROUP BY NumeroCompte
    HAVING COUNT(*) >= 2
);