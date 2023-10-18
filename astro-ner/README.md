# Installer DVC

Pour installer DVC, il est conseillé de créer un environnement virtuel. Les commandes sont :

```bash
pip install wheel # pré-requis nécessaire
pip install dvc[webdav]
```

## Configurer le remote DVC

Dans le .env mettre les trois lignes suivantes :

```bash
export WEBDAV_URL=webdav://????????
export WEBDAV_LOGIN=????
export WEBDAV_PASSWORD=?????
```

Pour prendre en compte ces trois lignes : `source .env`.

Pour déclarer un remote DVC : `dvc remote add -d origin $WEBDAV_URL`
