# Installer DVC

Pour installer DVC, il est conseillé de créer un environnement virtuel.

```bash
python3 -m venv .venv/
```

Pour activer :

```bash
source .venv/bin/activate
```

Les commandes pour installer dvc sont :

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

Pour envoyer un fichier de plus de 500M :

- Mettre le fichier dans un répertoire
- Découper le fichier avec `split -b 500m nom_du_fichier`
- Faire un `dvc add répertoire`
- `dvc push répertoire.dvc`
