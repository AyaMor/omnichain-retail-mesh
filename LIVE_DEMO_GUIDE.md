# Guide de Démonstration en Direct (Live Demo) avec Postman

Ce guide est fait pour vous accompagner pas à pas pendant votre présentation de 18 minutes. L'objectif est de montrer l'utilité des 4 APIs sans stress et sans taper de code en direct.

---

##  Étape 1 : La Préparation (Avant votre passage)

Il faut préparer votre environnement **avant** de prendre la parole pour ne pas perdre de temps.

1. **Lancez les 4 serveurs en arrière-plan**
   Ouvrez 4 terminaux séparés et lancez vos serveurs comme expliqué dans le `TESTING_GUIDE.md` :
   - Terminal 1 : `python procurement/mock-server/server.py`
   - Terminal 2 : `python marketplace/mock-server/server.py`
   - Terminal 3 : `python dashboard/mock-server/server.py`
   - Terminal 4 : `python logistics/mock-server/server.py`

2. **Préparez Postman**
   - Ouvrez le logiciel **Postman**.
   - En haut à gauche, cliquez sur le bouton **Import**.
   - Importez la collection : sélectionnez le fichier `postman/RetailSync_Collection.json`.
   - Importez l'environnement : recliquez sur **Import** et sélectionnez `postman/RetailSync_Environment.json`.
   - **TRÈS IMPORTANT :** En haut à droite de Postman, il y a un menu déroulant pour choisir l'environnement. Sélectionnez **RetailSync - Local**. (Si vous oubliez ça, rien ne marchera !).

3. **Préparez votre Terminal pour gRPC**
   Gardez un 5ème terminal ouvert, prêt à taper : `python logistics/mock-server/client.py` (ne faites pas Entrée tout de suite).

---

## Étape 2 : L'Exécution (Pendant la présentation)

Gérez votre temps : la démo doit durer **3 minutes maximum**. Ne montrez qu'une seule requête par technologie. 

Voici le script (ce que vous faites + ce que vous dites) :

### 1. Démontrer SOAP (La Rigueur B2B)
- **Action :** Dans Postman, ouvrez le dossier `Module 3 : SOAP...` et cliquez sur la requête `SubmitOrder`.
- **Ce que vous montrez :** Allez dans l'onglet **Body**. Montrez à l'audience la taille et la complexité de l'enveloppe XML.
- **Ce que vous dites :** *"Voici comment nous envoyons une commande à l'usine. C'est très verbeux (XML), mais c'est voulu : le contrat WSDL garantit qu'aucune erreur de format n'est possible."*
- **Action :** Cliquez sur le bouton bleu **Send**.
- **Ce que vous montrez :** La réponse apparaît en bas. Montrez le `<status>ACCEPTED</status>`.

### 2. Démontrer REST (La Simplicité pour les Boutiques)
- **Action :** Ouvrez le dossier `Module 1 : REST...` et cliquez sur `GET - Voir tout l'inventaire`.
- **Ce que vous montrez :** Montrez l'URL de la requête, qui est très courte et lisible (`/inventory`).
- **Ce que vous dites :** *"À l'inverse, voici l'API pour que nos boutiques partenaires consultent le stock. Une simple requête GET standard. N'importe quel développeur web sait l'utiliser en 5 minutes."*
- **Action :** Cliquez sur **Send**.
- **Ce que vous montrez :** La réponse JSON en bas, très claire avec les quantités.

### 3. Démontrer GraphQL (Le Chef d'Orchestre)
- **Action :** Ouvrez le dossier `Module 2 : GraphQL...` et cliquez sur `Requête - Magasins, Stock et Commandes`.
- **Ce que vous montrez :** Allez dans l'onglet **Body**. Montrez que vous avez tapé exactement les champs que vous voulez : `stores > id, name` puis `inventory` puis `orders`.
- **Ce que vous dites :** *"Maintenant le tableau de bord du gérant. Au lieu de faire 3 requêtes REST séparées (magasin, stock, commandes), on demande exactement ce qu'on veut à GraphQL en une seule fois. Il s'occupe de rassembler les infos."*
- **Action :** Cliquez sur **Send**.
- **Ce que vous montrez :** La réponse JSON en bas qui contient bien `inventory` et `orders` imbriqués.

### 4. Démontrer gRPC (La Vitesse Temps-Réel)
*Note : Postman gère gRPC, mais pour un effet "Waouh" devant un jury, le terminal est plus impressionnant visuellement pour afficher du streaming en temps réel.*
- **Action :** Réduisez Postman et ouvrez votre **5ème terminal** préparé.
- **Ce que vous dites :** *"Enfin, pour communiquer avec nos 100 robots dans l'entrepôt, SOAP ou REST satureraient le réseau. On utilise gRPC pour envoyer des messages binaires ultra-légers en continu."*
- **Action :** Appuyez sur **Entrée** pour lancer `python logistics/mock-server/client.py`.
- **Ce que vous montrez :** Laissez le texte défiler sur le terminal noir. On voit le robot exécuter *MOVE*, *PICK*, *CHARGE* et envoyer ses coordonnées (X, Y, Z) en temps réel.

---

## En cas de problème pendant la présentation (Plan B)

Si *quoi que ce soit* se passe mal (un serveur qui plante, un clic au mauvais endroit, internet coupé...) :
1. **Ne paniquez pas** et n'essayez pas de déboguer devant le jury. 
2. Dites simplement : *"C'est le risque du direct, mais heureusement nous avons préparé les diagrammes de séquence dans les diapositives précédentes qui montrent exactement ce comportement."*
3. Passez directement à la diapositive suivante. Les démonstrations live valent cher, mais l'aisance avec laquelle vous gérez les imprévus technique l'est tout autant !
