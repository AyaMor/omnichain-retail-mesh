# Présentation "Architectures Logicielles" : Pitch à Deux Voix

Ce document propose une répartition équilibrée de la prise de parole pour la soutenance finale. Le temps estimé est d'environ 15 minutes, à adapter selon votre rythme.

**Intervenants :**
*   **Aya** (Aya Morsli)
*   **Mohamed** (Mohamed Chtouqui)

---

## Slide 1 : Page de Garde (Titre)
**Durée estimée : 0:30**

**[Aya] :** "Bonjour à toutes et à tous. Nous sommes Aya Morsli et Mohamed Chtouqui, étudiants en filière VAP DSI, et nous sommes ravis de vous présenter aujourd'hui l'aboutissement de notre projet d'architecture logicielle, encadré par le Professeur Walid Gaaloul."

**[Mohamed] :** "Notre travail porte sur une étude comparative d'architectures API appliquées à un cas d'usage réel. Pendant ce semestre, nous avons modélisé, implémenté et comparé quatre technologies majeures : SOAP, REST, GraphQL et gRPC."

---

## Slide 2 : Plan de la présentation
**Durée estimée : 0:30**

**[Aya] :** "Pour structurer notre propos, nous allons procéder en cinq temps. Tout d'abord, nous vous présenterons directement la synthèse de notre étude via un tableau comparatif. Ensuite, nous poserons le contexte métier de notre cas d'étude."

**[Mohamed] :** "Nous justifierons par la suite nos choix architecturaux avant de plonger dans l'analyse technique détaillée de chaque protocole. Enfin, nous conclurons sur l'intégration logicielle et les perspectives d'amélioration, ce qui nous amènera à la démonstration technique."

---

## Slide 3 : 1. Synthèse Comparative Principale
**Durée estimée : 1:30**

**[Aya] :** "Voici d'emblée la conclusion macroscopique de notre étude. Ce tableau met en exergue qu'il n'existe pas de 'Silver Bullet', c'est-à-dire de solution universelle. Chaque technologie brille par un cas d'usage bien précis."

**[Mohamed] :** "En effet. Comme on peut le voir, un protocole historique comme SOAP apporte une garantie contractuelle totale, parfaite pour du B2B strict. REST s'impose par son écosystème natif web et sa flexibilité. GraphQL révolutionne la consommation de la donnée côté Frontend, tandis que gRPC se concentre sur la performance pure en binaire pour le dialogue inter-systèmes."

---

## Slide 4 : 2. Contexte Fonctionnel
**Durée estimée : 1:30**

**[Aya] :** "Pour appliquer et tester ces technologies de manière empirique, nous avons imaginé 'RetailSync', le système d'information d'une entreprise opérant dans le commerce de détail (Retail). Plutôt que de coder des services abstraits, nous avons modélisé quatre domaines métiers bien distincts."

**[Mohamed] :** "Le SI devait gérer : 1. L'approvisionnement auprès de fournisseurs industriels. 2. La synchronisation des stocks avec des boutiques partenaires. 3. Le pilotage via un tableau de bord directionnel. Et 4. La remontée de données issues de robots logistiques en entrepôt."

---

## Slide 5 : Démarche d'Ingénierie "Contract-First"
**Durée estimée : 1:00**

**[Aya] :** "Avant d'écrire la moindre ligne de code métier, nous avons appliqué une démarche stricte de type 'Contract-First'. Pour chaque module, le contrat d'interface a été pensé, écrit et validé en premier."

**[Mohamed] :** "Que ce soit un WSDL pour SOAP, un OpenAPI pour REST, un schéma pour GraphQL ou un fichier `proto` pour gRPC, cette approche a permis de garantir la fiabilité du typage et de découpler le design de l'implémentation. Le code des serveurs a d'ailleurs été généré ou contraint par ces contrats."

---

## Slide 6 : 3. Choix Architectural (Justification Microservices)
**Durée estimée : 1:30**

**[Aya] :** "Face à la diversité de ces quatre métiers et de leurs contraintes, développer une application monolithique aurait été une erreur conceptuelle et technologique."

**[Mohamed] :** "Nous avons donc opté pour une approche par microservices. Cela s'imposait techniquement car faire cohabiter du gRPC en HTTP/2 binaire avec du SOAP XML sur un même serveur applicatif est un anti-pattern. Cette isolation par port et par processus garantit la haute disponibilité : si la base de télémétrie robotique surcharge gRPC, la création des bons de commande SOAP n'en sera pas affectée."

---

## Slide 7 : Cartographie Logique du Système
**Durée estimée : 0:30**

**[Aya] :** "Voici donc la cartographie logique de notre système. Chaque base de données, chaque serveur métier est indépendant, et expose son propre point d'entrée réseau selon le protocole le plus adapté à sa fonction."

---

## Slide 8 : 4. Analyse - SOAP (La rigueur des Contrats)
**Durée estimée : 1:15**

**[Mohamed] :** "Entrons dans le détail technique. Commençons par définir rigoureusement **SOAP (Simple Object Access Protocol)**. Il s'agit d'un protocole d'échange d'informations structurées, strictement basé sur le langage XML. Contrairement à une simple architecture, SOAP impose une enveloppe standardisée (Header/Body) et repose sur un contrat de service formel, le WSDL, qui dicte contractuellement chaque opération, type et paramètre disponible."

**[Mohamed] :** "Pour notre domaine 1, l'approvisionnement B2B avec des usines, nous devions nous interfacer avec des ERP historiques. SOAP s'est imposé naturellement par sa rigueur. Tout part du contrat WSDL. Plutôt que de coder manuellement la logique réseau, nous l'utilisons pour générer ce qu'on appelle un **Stub** (une souche). Ce Stub agit comme un proxy local : le développeur appelle une simple fonction Python, et le Stub se charge en coulisses de sérialiser l'objet en une enveloppe XML parfaitement conforme au schéma XSD, puis de l'envoyer sur le réseau. Cela garantit une validation 'Fail-fast' et masque la complexité de l'échange XML."

---

## Slide 9 : 4. Analyse - REST (L'Universalité et ses limites)
**Durée estimée : 1:15**

**[Aya] :** "Passons à **REST (Representational State Transfer)**. Plus qu'un protocole, REST est un style architectural défini par Roy Fielding. Il repose sur l'exposition de ressources identifiables par des URI, manipulées exclusivement de manière 'stateless' via la sémantique standard des verbes HTTP (GET, POST, PUT, PATCH, DELETE). Le format d'échange est libre, mais le JSON est devenu le standard de fait."

**[Aya] :** "Pour le domaine 2, la synchronisation des stocks avec les boutiques, le critère numéro un était l'accessibilité universelle. Nous avons logiquement choisi REST. REST brille par son utilisation sémantique de HTTP, comme le verbe `PATCH` pour mettre à jour efficacement une quantité. De plus, il profite nativement du cache HTTP sur les requêtes `GET`. Cependant, cette approche montre ses limites face à des interfaces complexes. Le client subit souvent le problème de l'**Over-fetching** (télécharger un objet JSON entier alors qu'on ne veut qu'un seul champ) et le problème des **N+1 requêtes** (multiplier les appels HTTP séquentiels pour récupérer des données liées)."

---

## Slide 10 : 4. Analyse - GraphQL (L'Orchestration BFF)
**Durée estimée : 1:30**

**[Mohamed] :** "Technologie plus récente, **GraphQL** est un langage de requête open source créé par Facebook. Contrairement à REST qui expose de multiples URIs fixes, GraphQL expose un 'Endpoint' unique. Il offre au client la possibilité de définir de manière déclarative et fortement typée la struture exacte des données dont il a besoin, déplaçant ainsi la logique de composition du client vers le serveur."

**[Mohamed] :** "Le domaine 3, notre tableau de bord directionnel, adressait justement le problème de sur-multiplication des requêtes REST. En une seule trame POST, le frontend demande exactement l'arbre de graphe de données dont il a besoin, résolvant purement le sur-fetching. Plus important encore, dans notre projet, le serveur GraphQL agit comme un véritable orchestrateur (pattern BFF - Backend For Frontend). Derrière chaque champ du schéma se cache une fonction appelée **Resolver**. Lorsqu'on interroge un magasin, nos Resolvers Python font le 'Fan-Out' : ils traduisent la requête, interrogent simultanément l'API REST pour le stock, le serveur SOAP pour les commandes, et gRPC pour les robots, puis agglomèrent ces formats hétérogènes (JSON, XML, Binaire) en une unique réponse JSON unifiée."

---

## Slide 11 : 4. Analyse - gRPC (La Performance Temps-Réel)
**Durée estimée : 1:30**

**[Aya] :** "Terminons avec **gRPC (gRPC Remote Procedure Calls)**, un framework open source initialement développé par Google. Sa définition rigoureuse repose sur deux piliers : l'utilisation d'HTTP/2 comme protocole de transport sous-jacent, et l'utilisation des Protocol Buffers (Protobuf) comme langage de description d'interface (IDL) et format d'échange binaire fortement typé."

**[Aya] :** "Le domaine 4 concerne la robotique d'entrepôt, avec des contraintes de haute fréquence. C'est là que gRPC révèle sa puissance. Contrairement à JSON et XML, l'encodage binaire compilé de Protobuf est ultra-compressé. Au-delà de la taille, le véritable atout de gRPC est son exploitation d'HTTP/2 qui permet le **Streaming Bidirectionnel**. Le robot ouvre un seul canal persistant avec le serveur central. Plutôt que de multiplier les coûteuses requêtes HTTP (le traditionnel Tour par Tour), le serveur peut 'pousser' des mises à jour de coordonnées en rafale sur le flux existant, annulant la latence de l'établissement de connexion TCP et rendant le véritable temps-réel possible."

---

## Slide 12 : Transition Validation Pratique
**Durée estimée : 0:45**

**[Mohamed] :** "La théorie et l'architecture logicielle étant fixées, la question est : comment valider ce modèle en conditions réelles ?"

**[Mohamed] :** "Nous allons maintenant passer à la démonstration. L'objectif est de solliciter la flotte de serveurs que nous avons développés. Nous enverrons de vraies commandes via l'enveloppe XML SOAP, récupérerons des stocks REST, agrégerons des graphes via GraphQL, et ouvrirons un flux de télémétrie streaming avec gRPC."

---

## Slide 13 : Conclusion & API Gateway
**Durée estimée : 1:00**

*(Note : Présentez cette slide APRÈS la démo en live finale pour clôturer le passage)*

**[Aya] :** "Pour conclure cette soutenance, bien que notre architecture de démonstration expose 4 points d'accès distincts à visée pédagogique, cela créerait ce qu'on appelle un couplage fort en production."

**[Aya] :** "En environnement d'entreprise réel, l'évolution naturelle de ce système serait l'implémentation d'une API Gateway. Composant central, la Gateway masquerait la complexité protocolaire via une façade REST/GraphQL unifiée tout en centralisant l'authentification et le rate-limiting. L'hétérogénéité technologique devient alors totalement invisible pour le client, tout en gardant l'agilité des microservices en backend."

**[Mohamed] :** "Nous vous remercions pour votre attention et sommes maintenant à l'écoute de vos questions, remarques, ou éclaircissements sur l'implémentation technique."

---

*Fin du Pitch.*
