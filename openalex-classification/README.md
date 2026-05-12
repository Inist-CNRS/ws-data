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

- Mettre le fichier dans un répertoire nommé `répertoire`
- Découper le fichier avec `split -b 500m nom_du_fichier`
- Faire un `dvc add répertoire`
- `dvc push répertoire.dvc`

## Classification

### Niveau 1 — Domaine (domains)

Le modèle `model_parent.bin` prédit l'un des domaines suivants :

| Étiquette | Description |
|---|---|
| `physical_sciences` | Sciences physiques |
| `social_sciences` | Sciences sociales |
| `health_sciences` | Sciences de la santé |
| `life_sciences` | Sciences du vivant |

### Niveau 2 — Sous-domaine (fields)

Selon le domaine prédit, un second modèle spécialisé affine la classification :

| Domaine | Modèle utilisé | Fields possibles |
|---|---|---|
| `health_sciences` | `model_healthsciences.bin` | `dentistry`, `health_professions`, `medicine`, `nursing`, `veterinary` |
| `life_sciences` | `model_lifesciences.bin` | `agricultural_and_biological_sciences`, `biochemistry_genetics_and_molecular_biology`, `immunology_and_microbiology`, `neuroscience`, `pharmacology_toxicology_and_pharmaceutics` |
| `physical_sciences` | `model_physicalsciences.bin` | `chemical_engineering`, `chemistry`, `computer_science`, `earth_and_planetary_sciences`, `energy`, `engineering`, `environmental_science`, `materials_science`, `mathematics`, `physics_and_astronomy` |
| `social_sciences` | `model_socialsciences.bin` | `arts_and_humanities`, `business_management_and_accounting`, `decision_sciences`, `economics_econometrics_and_finance`, `psychology` |

---