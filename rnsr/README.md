# RNSR

Les données préparées dans ce répertoire servent pour le web service
<https://github.com/Inist-CNRS/web-services/tree/main/services/affiliations-tools>,
la route
[v1/rnsr](https://github.com/Inist-CNRS/web-services/tree/main/services/affiliations-tools/v1/rnsr).

## Installer DVC

Pour installer DVC, il est conseillé de créer un environnement virtuel `.venv` :

```bash
python3 -m venv .venv/
```

Pour activer :

```bash
source .venv/bin/activate
```

Les commandes pour installer DVC sont :

```bash
pip install "dvc[webdav]==3.42.0"
```

## Configurer le remote DVC

Dans le .env mettre les trois lignes suivantes :

```bash
export WEBDAV_URL=webdav://????????
export WEBDAV_LOGIN=????
export WEBDAV_PASSWORD=?????
```

Pour configurer le remote DVC :

```bash
source .env
dvc init --subdir
dvc remote add --local -d origin $WEBDAV_URL
dvc remote modify --local origin user $WEBDAV_LOGIN
dvc remote modify --local origin password $WEBDAV_PASSWORD
dvc config core.autostage true
```

## Installer les paquets

```bash
bun install
```

> **Remarque:** [bun](https://bun.sh/) doit être installé.

## Lancer le programme

```bash
bin/prepareRnsrJson.ts -f data/RNSR-2023.xml
```

Le résultat sera dans `data/RNSR.json`.

## Trouver une structure à partir du RNSR

```bash
$ fx < data/RNSR.json '.structures.structure.find(x => x.num_nat_struct ==="198822446E")'
{
  "num_nat_struct": "198822446E",
  "intitule": "Institut de l'information scientifique et technique",
  "sigle": "INIST",
  "ville_postale": "VANDOEUVRE LES NANCY CEDEX",
  "code_postal": 54519,
  "etabAssoc": [
    {
      "etab": {
        "sigle": "CNRS",
        "libelle": "Centre national de la recherche scientifique",
        "sigleAppauvri": "cnrs",
        "libelleAppauvri": "centre national de la recherche scientifique"
      },
      "label": "UAR",
      "labelAppauvri": "uar",
      "numero": 76
    }
  ],
  "intituleAppauvri": "institut de l information scientifique et technique",
  "sigleAppauvri": "inist",
  "ville_postale_appauvrie": "vandoeuvre les nancy cedex",
  "annee_creation": 1988,
  "an_fermeture": 0
}
```

> **Remarque:** `fx` doit être installé. Ça peut être via npm: `npm i -g fx`
