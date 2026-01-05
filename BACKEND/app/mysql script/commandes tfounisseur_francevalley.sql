SELECT * FROM fraisexpost.tfournisseur_francevalley;



/*les doublons qu'on fait match avec des noms de produits*/
SELECT f.ID AS IDFournisseur, 
       c.ID AS IDClient, 
       cp.ID AS IDClientProduit, 
       c.Nom, 
       c.Prenom, 
       c.Bureau, 
       c.Conseiller, 
       f.EstGenere, 
       f.NomProduit as FournisseurProduit,
       p.Produit as ClientProduit
FROM fraisexpost.tfournisseur_francevalley f
JOIN tclients c ON c.Nom = f.nom AND c.Prenom = f.Prenom
JOIN tclient_produits cp ON c.ID = cp.IDClient
JOIN tproduits p ON cp.IDProduit = p.ID
WHERE f.NomProduit = p.Produit 
or f.NomProduit = p.intitule 
AND f.ID IN (
    SELECT f.ID
    FROM fraisexpost.tfournisseur_francevalley f
    JOIN tclients c ON c.Nom = f.nom AND c.Prenom = f.Prenom
    JOIN tclient_produits cp ON c.ID = cp.IDClient
    JOIN tproduits p ON cp.IDProduit = p.ID
    WHERE f.NomProduit = p.Produit
	or f.NomProduit = p.intitule 
    GROUP BY f.ID
    HAVING COUNT(f.ID) > 1
)
ORDER BY f.ID;

/*uniquement ceux qui n'ont pas de doublon*/
SELECT f.ID AS IDFournisseur, 
       c.ID AS IDClient, 
       cp.ID AS IDClientProduit, 
       c.Nom, 
       c.Prenom, 
       c.Bureau, 
       c.Conseiller, 
       f.NomProduit as FournisseurProduit,
       p.Produit as ClientProduit
FROM fraisexpost.tfournisseur_francevalley f
JOIN tclients c ON c.Nom = f.nom AND c.Prenom = f.Prenom
JOIN tclient_produits cp ON c.ID = cp.IDClient
JOIN tproduits p ON cp.IDProduit = p.ID
WHERE p.EtablissementFournisseur = 'FRANCE VALLEY INVESTISSEMENTS'
AND f.ID IN (
    SELECT f.ID
    FROM fraisexpost.tfournisseur_francevalley f
    JOIN tclients c ON c.Nom = f.nom AND c.Prenom = f.Prenom
    JOIN tclient_produits cp ON c.ID = cp.IDClient
    JOIN tproduits p ON cp.IDProduit = p.ID
    WHERE p.EtablissementFournisseur = 'FRANCE VALLEY INVESTISSEMENTS'
    GROUP BY f.ID
    HAVING COUNT(f.ID) = 1
)
ORDER BY f.ID;


/*requete finale utilisée pour faire patch les produits du fournisseur et de la base client*/
select f.id, c.ID, cp.ID, p.ID, f.Nom, c.Nom, f.Prenom, c.Prenom, f.NomProduit as FournisseurProduit, p.Produit as ClientProduit
from tfournisseur_francevalley f 
join fraisexpost.tclients c on replace(f.Nom, '-', ' ') = replace(c.Nom, '-', ' ') and replace(f.Prenom, '-', ' ') = replace(c.Prenom, '-', ' ') 
join fraisexpost.tclient_produits cp on c.id = cp.idclient 
join fraisexpost.tproduits p on cp.IDProduit = p.id 
where p.EtablissementFournisseur = 'FRANCE VALLEY INVESTISSEMENTS'
and f.NomProduit = p.Produit
order by f.id asc;


/*trouver les personnes dans la table tfournisseur_francevalley qui ne correspondent à aucun client dans la table tclients*/
SELECT f.id, f.Nom, f.Prenom
FROM tfournisseur_francevalley f
LEFT JOIN tclients c ON f.Nom = c.Nom AND f.Prenom = c.Prenom
WHERE c.Nom IS NULL AND c.Prenom IS NULL
order by f.id asc;

