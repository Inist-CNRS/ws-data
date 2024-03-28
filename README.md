# ws-data

Dépôt de préparation des données pour les [services
web](https://github.com/Inist-CNRS/web-services).

Ces données peuvent être des tables de correspondance, des ressources
linguistiques, des modèles...

Nous les stockons via [DVC](https://dvc.org), pour pouvoir les réutiliser dans
d'autres projets (typiquement les services web).

Nous déposons ici les traitements préparatoires, afin de pouvoir les exposer et
les reproduire.

Chaque répertoire représente une expérience, un service web, auquel sont dédiés
les programmes et les données produites/traitées.

```mermaid
flowchart LR
    A(ws-data) -- push --> B[(DVC)]
    B -- pull --> C(web-services)
    click B href "https://dvc.org" _blank
    click C href "https://github.com/Inist-CNRS/web-services" _blank
```

```mermaid
mindmap
 root((ws-data))
    Projects
        astro-ner
        RNSR
    DVC
        web-services
            ws-astro-ner
            affiliations-tools
                RNSR
```

Chaque répertoire doit contenir un fichier de configuration déclarant les
dépendances utilisées.  
Pour python, c'est un fichier `requirements.txt` (éventuellement obtenu en
utilisant la commande `pip freeze`).  
Pour node, c'est un `package.json`.
