# Les Graphiques de la Présentation

Tous les graphiques sont enregistrés sous forme d'images PNG dans le dossier `diagrams/` pour être facilement ajoutés à vos diapositives.

## 1. L'Architecture Globale (Vue d'ensemble)

C'est l'image parfaite pour commencer et montrer comment le système fonctionne dans son ensemble.

![Architecture Globale](/Users/ayamorsli/projet-API/diagrams/01_master_architecture.png)

## 2. SOAP — Les Commandes B2B

![Flux SOAP](/Users/ayamorsli/projet-API/diagrams/02_soap_sequence.png)

**Pourquoi utiliser SOAP ici ?**
- **C'est le standard de l'industrie :** Les grandes usines utilisent déjà des vieux systèmes (comme SAP) qui parlent SOAP.
- **C'est très strict :** Impossible de s'y tromper grâce au fichier WSDL qui vérifie chaque champ de la commande.
- **C'est très sécurisé :** Chaque message est chiffré.

*En résumé : On sacrifie la vitesse et la simplicité pour avoir une garantie à 100% que la commande est valide. Parfait pour de grosses transactions financières avec des partenaires !*

## 3. REST — La Gestion des Boutiques

![Flux REST](/Users/ayamorsli/projet-API/diagrams/03_rest_sequence.png)

**Pourquoi utiliser REST ici ?**
- **C'est très simple :** N'importe quel développeur sait s'en servir. Pas besoin de générer du code pour intégrer l'API.
- **C'est rapide :** On utilise le fonctionnement standard d'Internet (les requêtes HTTP GET ou PATCH).

*En résumé : Idéal pour que des développeurs tiers puissent gérer l'inventaire de leur boutique facilement et avec les outils standards.*

## 4. GraphQL — Le Tableau de Bord

![Flux GraphQL](/Users/ayamorsli/projet-API/diagrams/04_graphql_sequence.png)

**Pourquoi utiliser GraphQL ici ?**
- **Tout en un :** Au lieu de faire 3 requêtes (pour voir les magasins, puis le stock, puis les commandes), on demande tout en une seule fois.
- **À la carte :** L'application web demande exactement ce dont elle a besoin, ni plus ni moins. Pas de données inutiles téléchargées.

*En résumé : GraphQL agit comme un "chef d'orchestre". L'application cliente ne fait qu'une requête à GraphQL, et c'est lui qui va chercher les infos dans les autres APIs.*

## 5. gRPC — Les Robots de l'Entrepôt

![Flux gRPC](/Users/ayamorsli/projet-API/diagrams/05_grpc_sequence.png)

**Pourquoi utiliser gRPC ici ?**
- **Ultra léger :** Il envoie des données sous forme binaire (des 0 et des 1) plutôt que du texte très lourd. Un message fait 40 octets au lieu de 250 octets en JSON.
- **En continu :** Le robot et le serveur restent connectés. Ils peuvent s'envoyer des informations dans les deux sens sans interruption (streaming).

*En résumé : Indispensable quand on a 100 robots qui envoient 10 messages par seconde. Avec une API classique, le réseau de l'entrepôt serait saturé.*

## 6. Arbre de Décision (Pourquoi avoir choisi ces 4 APIs)

![Arbre de décision](/Users/ayamorsli/projet-API/diagrams/06_decision_tree.png)

**Note pour la présentation :** *"Par défaut, on utilise REST car c'est le plus simple. Mais dès qu'on a un besoin très particulier (sécurité extrême, données complexes, vitesse temps-réel), on choisit l'outil fait pour ça."*

## 7. Comparaison du poids des messages

![Comparaison XML / JSON / Protobuf](/Users/ayamorsli/projet-API/diagrams/08_payload_comparison.png)

**Note pour la présentation :** *"Pour envoyer la même information, regarder comment la taille change. SOAP est lourd, REST est au milieu, et gRPC (Protobuf) bat tous les records de légèreté."*

## 8. Le Motif "Aggregator" (Comment GraphQL rassemble tout)

![L'Aggregator](/Users/ayamorsli/projet-API/diagrams/07_aggregator_pattern.png)

**Note pour la présentation :** *"Pour le développeur du site web (frontend), le fait d'avoir 3 APIs différentes derrière est invisible. Il ne parle qu'à GraphQL qui s'occupe de tout rassembler."*

---

## 9. Amélioration de l'Architecture : L'API Gateway

Si on vous demande **"Pourquoi avoir utilisé 4 ports différents au lieu d'un seul ?"**, voici la réponse parfaite pour la fin de la présentation :

Dans ce projet pédagogique, nous avons laissé chaque module tourner sur son propre "port" réseau (8001, 8002, etc.). Cela nous permet de bien séparer et comprendre les technologies. L'architecture est dite en **Microservices**.

Cependant, en production dans le monde réel, on ajouterait une brique supplémentaire devant tout cela : **une Passerelle d'API (API Gateway)**.

- Le Gateway écoute sur **un seul port unifié** (ex: le port sécurisé 443 pour HTTPS).
- Lorsqu'un client frappe à la porte unifiée, c'est le Gateway qui joue le rôle de routeur intelligent. 
- S'il demande l'adresse `/procurement`, le Gateway transfère sous le capot le trafic vers notre serveur SOAP sur le port 8001. 

Ainsi, le client ne voit qu'une seule adresse globale, et nous pouvons garder nos systèmes (gRPC, REST, SOAP) parfaitement séparés et indépendants en arrière-plan sans perturber le réseau de l'entreprise.
