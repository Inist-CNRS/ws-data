# first-name

Les données préparées dans ce répertoire servent pour le web service <https://github.com/Inist-CNRS/web-services/tree/main/services/authors-tools>.

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
pip install -r requirements.txt
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

## Générer le pickle

```bash
python preprocessing.py
```
