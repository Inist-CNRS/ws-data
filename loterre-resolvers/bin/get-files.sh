#!/usr/bin/env bash

set -euo pipefail

printf "Downloading files...\n\n"

printf "216\n"
curl --progress-bar -o ./data/216.skos http://mapping-tables.daf.intra.inist.fr/216.skos

printf "2XK - loterre-structures-recherche\n"
curl --progress-bar -o ./data/2XK.skos http://mapping-tables.daf.intra.inist.fr/loterre-structures-recherche.xml

printf "3JP\n"
curl --progress-bar -o ./data/3JP.skos http://mapping-tables.daf.intra.inist.fr/3JP.skos

printf "73G\n"
curl --progress-bar -o ./data/73G.skos http://mapping-tables.daf.intra.inist.fr/73G.skos

printf "9SD - loterre-pays\n"
curl --progress-bar -o ./data/9SD.skos http://mapping-tables.daf.intra.inist.fr/loterre-pays.xml

printf "BVM\n"
curl --progress-bar -o ./data/BVM.skos http://mapping-tables.daf.intra.inist.fr/BVM.skos

printf "D63 - loterre-communes\n"
curl --progress-bar -o ./data/D63.skos http://mapping-tables.daf.intra.inist.fr/loterre-communes.xml

printf "JVR - loterre-mesh\n"
curl --progress-bar -o ./data/JVR.skos http://mapping-tables.daf.intra.inist.fr/loterre-mesh.xml

printf "MDL\n"
curl --progress-bar -o ./data/MDL.skos http://mapping-tables.daf.intra.inist.fr/MDL.skos

printf "N9J\n"
curl --progress-bar -o ./data/N9J.skos http://mapping-tables.daf.intra.inist.fr/N9J.skos

printf "P21\n"
curl --progress-bar -o ./data/P21.skos http://mapping-tables.daf.intra.inist.fr/P21.skos

printf "P66\n"
curl --progress-bar -o ./data/P66.skos http://mapping-tables.daf.intra.inist.fr/P66.skos

printf "QX8\n"
curl --progress-bar -o ./data/QX8.skos http://mapping-tables.daf.intra.inist.fr/QX8.skos
