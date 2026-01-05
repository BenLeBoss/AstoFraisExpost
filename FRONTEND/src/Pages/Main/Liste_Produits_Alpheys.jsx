
/* Cette function sert à remplir la liste des produits des pages Alpheys pour les groupes Astoria et Insinia */
function Liste_Produits_Alpheys(Groupe){
   
    return loadProduits(Groupe);

}export default Liste_Produits_Alpheys;


const loadProduits = async(Groupe) => {
    let ListeProduits = [];

    try{
        const res = await fetch('/api/REST/liste/produitsAlpheys', {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json'
            },
            body : JSON.stringify({ 
                    groupe : Groupe
                })
        });
        const data = await res.json();
        
        if (res.ok) {
            ListeProduits = data.produits_liste;
            console.log("Liste des produits : " + data.produits_liste);
        }
        else {
            const status = res.status;
            const message = data.message || 'Erreur serveur';
            throw new Error(`Code ${status} : ${message}`);
        }
    } catch(err){
        console.error('Erreur coté frontend :', err.message);
        //alert(`Erreur : ${err.message}`);
    }

    return ListeProduits;
}