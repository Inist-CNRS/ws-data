# Loterre-resolvers

Les données préparées dans ce répertoire servent pour le web service
<https://github.com/Inist-CNRS/web-services/tree/main/services/loterre-resolvers>.

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

Dans le `.env` mettre les trois lignes suivantes :

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

## Mettre à jour les fichiers

1. se mettre dans ce répertoire: `cd loterre-resolvers`
2. activer l'environnement virtuel: `source .venv/bin/activate`
3. lancer le script: `./bin/get-files.sh`
4. lancer la création des bases à mettre à jour: `dvc repro`
5. pousser les fichiers: `dvc push`

> [!NOTE]  
> Pour lancer la génération d'un vocabulaire en particulier (ex: `216`),
> utiliser `dvc repro tgz@216`.

> [!WARNING]
> Pour ajouter un nouveau vocabulaire (ex: `VOCA`), ne pas oublier le
> `dvc add data/VOCA.skos`.
