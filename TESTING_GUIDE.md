# Guide de Test — Comparaison d'APIs

Ce guide vous montre comment lancer chaque serveur et vérifier que les 4 différentes APIs (SOAP, REST, GraphQL, gRPC) fonctionnent correctement sur votre machine.

## Étape 1 : Installer ce qu'il faut

Ouvrez un terminal dans le dossier du projet (`projet-API/`) et tapez ces commandes pour installer les bibliothèques Python nécessaires :

```bash
pip install -r procurement/requirements.txt
pip install -r marketplace/requirements.txt
pip install -r dashboard/requirements.txt
pip install -r logistics/requirements.txt
```

Ensuite, exécutez cette commande (à faire une seule fois) pour préparer les fichiers gRPC :
```bash
python -m grpc_tools.protoc -Ilogistics/contracts --python_out=logistics/mock-server --grpc_python_out=logistics/mock-server logistics/contracts/warehouse.proto
```

---

## Étape 2 : Lancer les 4 serveurs

Ouvrez **4 nouveaux terminaux** (un pour chaque API) et tapez une commande par terminal :

**Terminal 1 — SOAP (port 8001) :**
```bash
python procurement/mock-server/server.py
```

**Terminal 2 — REST (port 8002) :**
```bash
python marketplace/mock-server/server.py
```

**Terminal 3 — GraphQL (port 8003) :**
```bash
python dashboard/mock-server/server.py
```

**Terminal 4 — gRPC (port 50051) :**
```bash
python logistics/mock-server/server.py
```

---

## Étape 3 : Tester que ça marche (Démonstration en direct)

Maintenant, ouvrez un **5ème terminal**. C'est ici que vous allez envoyer des requêtes pour tester chaque API, comme si vous étiez le client.

### 1. Tester SOAP (Commander auprès d'une usine)
On envoie un fichier XML (le format lourd mais très strict) pour passer une commande.
```bash
curl -s -X POST http://localhost:8001 -H "Content-Type: text/xml" -d @procurement/mock-server/test_request.xml
```
*Résultat attendu : Une réponse en XML qui confirme la commande (`<status>ACCEPTED</status>`).*

### 2. Tester REST (Gérer le stock des boutiques)
On utilise les méthodes classiques du web. D'abord, on demande de voir tout le stock (GET).
```bash
curl -s http://localhost:8002/inventory | python -m json.tool
```
Ensuite, on modifie la quantité d'un produit spécifique (PATCH).
```bash
curl -s -X PATCH http://localhost:8002/inventory/SKU001 -H "Content-Type: application/json" -d '{"quantity": 75}' | python -m json.tool
```
*Résultat attendu : Des réponses en JSON simples à lire avec les bonnes quantités de stock.*

### 3. Tester GraphQL (Le tableau de bord du gérant)
Au lieu de faire plusieurs requêtes, on demande exactement ce qu'on veut (id du magasin, l'inventaire, et les commandes) en une seule fois.
```bash
curl -s -X POST http://localhost:8003/graphql -H "Content-Type: application/json" -d '{"query":"{ stores { id name inventory { sku quantity } orders { status } } }"}' | python -m json.tool
```
*Résultat attendu : Une seule réponse JSON qui regroupe toutes les informations demandées.*

### 4. Tester gRPC (La Télémétrie des Robots)
Ici on utilise un petit script Python pour simuler une communication ultra-rapide en continu avec un robot d'entrepôt.
```bash
python logistics/mock-server/client.py
```
*Résultat attendu : Vous allez voir s'afficher en direct les mouvements et les actions du robot (MOVE, PICK, CHARGE).*

---

## Dépannage rapide

| Problème | Solution |
|---|---|
| `Connection refused` | Vérifiez que le serveur correspondant tourne bien dans son propre terminal. |
| Le port est déjà utilisé | Fermez le terminal qui l'utilise, ou redémarrez votre terminal/ordinateur si le processus est bloqué. |
| Erreur gRPC introuvable | Refaites la longue commande `grpc_tools.protoc` de l'Étape 1. |
