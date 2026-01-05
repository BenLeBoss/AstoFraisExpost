POUR RÉCUPÉRER LES DONNÉES DES FICHIERS EXCEL XLSX :
    -tous les fichiers nécessaires à cette partie du projet sont dans le dossier app/routes/getter_setter_data
    -ces fichiers servent à récupérer les infos disponibles dans les fichiers excel dispo dans app.medias.excel
    -et ajouter la data dans des tables de données

    -> Pour exécuter les codes, il faut se placer dans le dossier BACKEND et exécuter : 
                python -m app.routes.getter_setter_data.main

    1.Executer d'abord les codes pour récupérer les Clients, puis les produits, et enfin les produits par clients 
        ->(getter_Clients_data, getter_Produits_data, getter_ClientProduits_data)

    2.Vérifier qu'aucun doublon de produits ou de clients ne s'insère en table, pour cela une fonction nettoyer_champs() a été 
implémentée (app > routes > getter_setter_data > getter_data_from_xlsx > getter_Produits_data.py ou getter_ClientProduits_data.py)
et deux requètes sql ont été écrites pour la vérification (app > mysql script > commandes.sql)