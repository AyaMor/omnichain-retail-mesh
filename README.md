# RetailSync — Comparaison d'APIs : SOAP, REST, GraphQL et gRPC

Ce projet est une première application qui compare 4 types d'APIs différents : SOAP, REST, GraphQL et gRPC. 
L'objectif n'est pas de dire qu'une technologie est meilleure qu'une autre, mais de montrer que **chaque API a son utilité selon les besoins spécifiques**. Nous prenons l'exemple d'un système de gestion de magasin (Retail).

## Vue d'ensemble de l'architecture

```text
+---------------+--------------+---------------+----------------------+
|  SOAP / XML   |  REST / JSON |  GraphQL      |  gRPC / Protobuf     |
|  Port 8001    |  Port 8002   |  Port 8003    |  Port 50051          |
+---------------+--------------+---------------+----------------------+
|  procurement/ |  marketplace/|  dashboard/   |  logistics/          |
|               |              |               |                      |
|  Commandes    |  Gestion     |  Tableau de   |  Télémétrie des      |
|  B2B avec     |  des stocks  |  bord complet |  robots d'entrepôt   |
|  les usines   |  (Boutiques) |  (Gérants)    |  (Temps réel)        |
+---------------+--------------+---------------+----------------------+
```

## Structure du Projet

Le projet est divisé en 4 modules simples :

- **`procurement/` (SOAP)** : Sert à envoyer des commandes aux usines. Idéal pour les systèmes d'entreprise classiques qui ont besoin d'une structure très stricte (fichier WSDL).
- **`marketplace/` (REST)** : Sert à gérer les stocks des boutiques. C'est l'API la plus standard, facile à utiliser par tout type de développeur avec des requêtes simples (GET, PATCH).
- **`dashboard/` (GraphQL)** : Sert pour l'affichage du tableau de bord d'un gérant. Pratique car il permet de demander toutes les informations (stocks, commandes) en une seule fois, au lieu de faire plusieurs requêtes.
- **`logistics/` (gRPC)** : Sert pour les communications avec les robots. Très rapide et utilise très peu de bande passante, idéal pour envoyer les positions des robots en continu.

## Pourquoi utiliser chaque API ? (Le bon outil au bon moment)

1. **SOAP** : Très strict et sécurisé. Parfait pour les contrats entre entreprises (comme une commande d'achat), où la moindre erreur de format n'est pas permise.
2. **REST** : Simple, universel et facile à comprendre. Parfait pour que nos partenaires puissent mettre à jour leurs stocks rapidement.
3. **GraphQL** : Flexible pour le client. Parfait pour une interface web (tableau de bord) qui a besoin d'afficher des données variées sans ralentir l'application.
4. **gRPC** : Très performant et compact. Parfait pour des machines (comme nos robots d'entrepôt) qui communiquent entre elles 10 fois par seconde.

## Démarrage Rapide

### Prérequis
- Python 3.10+
- pip (le gestionnaire de paquets de Python)

### Comment lancer les serveurs

Ouvrez un terminal différent pour chaque serveur pour les laisser tourner :

```bash
# 1. SOAP (port 8001)
pip install -r procurement/requirements.txt
python procurement/mock-server/server.py

# 2. REST (port 8002)
pip install -r marketplace/requirements.txt
python marketplace/mock-server/server.py

# 3. GraphQL (port 8003)
pip install -r dashboard/requirements.txt
python dashboard/mock-server/server.py

# 4. gRPC (port 50051)
pip install -r logistics/requirements.txt
# (Besoin de générer les fichiers python depuis le proto la première fois)
python -m grpc_tools.protoc -Ilogistics/contracts --python_out=logistics/mock-server --grpc_python_out=logistics/mock-server logistics/contracts/warehouse.proto

python logistics/mock-server/server.py
```

### Comment tester rapidement

Ouvrez un dernier terminal pour faire ces requêtes de test :

```bash
# Tester SOAP (envoi d'une commande en XML)
curl -X POST http://localhost:8001 -H "Content-Type: text/xml" -d @procurement/mock-server/test_request.xml

# Tester REST (voir les stocks actuels)
curl http://localhost:8002/inventory

# Tester GraphQL (récupérer les infos des magasins en une fois)
curl -X POST http://localhost:8003/graphql -H "Content-Type: application/json" -d '{"query":"{ stores { id name inventory { sku name quantity } orders { id status } } }"}'

# Tester gRPC (voir les communications du robot)
python logistics/mock-server/client.py
```

Vous retrouverez tous les tests complets (y compris via Postman) dans le fichier `TESTING_GUIDE.md`.


## Démonstration en Direct (Live Demo)

Si vous présentez ce projet, un guide détaillé étape par étape (optimisé pour Postman) est disponible ici pour vous aider à montrer la puissance des APIs sans taper de code devant le public : **[Guide de Démonstration (LIVE_DEMO_GUIDE.md)](LIVE_DEMO_GUIDE.md)**
