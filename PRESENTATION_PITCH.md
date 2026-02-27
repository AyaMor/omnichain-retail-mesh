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

## Slide 8 : 4. Analyse - SOAP
**Durée estimée : 1:00**

**[Mohamed] :** "Entrons dans le détail. Pour le domaine 1, l'approvisionnement B2B, nous devions nous interfacer avec des ERP historiques. SOAP s'est imposé naturellement."

**[Mohamed] :** "Malgré sa verbosité liée au XML, l'usage d'un fichier WSDL et d'un schéma XSD nous permet une validation 'Fail-fast'. Si le partenaire envoie une entité métier non conforme au contrat strict, le flux est rejeté avant même d'atteindre le code logique. C'est robuste et éprouvé."

---

## Slide 9 : 4. Analyse - REST
**Durée estimée : 1:00**

**[Aya] :** "Pour le domaine 2, la synchronisation avec des boutiques tierces, le critère numéro un était l'accessibilité. Nous avons choisi l'architecture REST."

**[Aya] :** "Basé sur les standards du Web, HTTP et JSON, REST permet à n'importe quel partenaire de s'intégrer facilement. Nous avons particulièrement travaillé sur la sémantique HTTP, en utilisant par exemple la notion de SKU (Stock Keeping Unit) dans l'URL et le verbe HTTP `PATCH` pour mettre à jour efficacement et de manière asynchrone le différentiel d'un inventaire."

---

## Slide 10 : 4. Analyse - GraphQL
**Durée estimée : 1:30**

**[Mohamed] :** "Le domaine 3 devait alimenter un tableau de bord directionnel agrégeant de nombreuses entités (Magasins, Commandes, Employés). Les approches CRUD traditionnelles comme REST allaient générer de la latence via le fameux problème des 'N+1 requêtes'."

**[Mohamed] :** "GraphQL résout élégamment ce problème. En une seule trame POST, le frontend requise exactement l'arbre de graphe de données dont il a besoin, résolvant le sur-fetching de données, au prix d'une implémentation serveur plus complexe."

---

## Slide 11 : 4. Analyse - gRPC
**Durée estimée : 1:30**

**[Aya] :** "Enfin, le domaine 4 concerne la robotique d'entrepôt, avec des contraintes de haute fréquence et de faible bande passante. Nous avons retenu gRPC."

**[Aya] :** "Là où le JSON texte est lourd à parser, l'encodage binaire des Protocol Buffers de gRPC divise drastiquement le poids réseau. Surtout, grâce à HTTP/2, gRPC ouvre un canal de Streaming Bidirectionnel persistant, évitant le lag du TCP handshake à chaque trame, ce qui est indispensable pour de la télémétrie temps réel."

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
