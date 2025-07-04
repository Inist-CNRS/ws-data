#!/usr/bin/env bash

set -euo pipefail

get_url() {
    vocab="$1"
    value="${2:-SKOS}"
    LODEX_URL="https://data.istex.fr/api/run/all-documents/?\$query\[uri\]=uid:/${vocab}-${value}"
    HEADER="X-Lodex-Tenant: terminologies-liens"
    BASE_URL=$(curl -H "$HEADER" "$LODEX_URL" | jq -r '.data[0].kTJq // empty')
    if [[ -z "$BASE_URL" ]]; then
        echo "Error: .data[0].kTJq not found in JSON response for vocab '$vocab'." >&2
        exit 1
    fi
    URL="${BASE_URL}/download/${vocab}.xml"
    echo "$URL"
}

printf "Downloading files...\n\n"

printf "216\n"
curl --progress-bar -o ./data/216.skos http://mapping-tables.daf.intra.inist.fr/216.skos

printf "2XK - loterre-structures-recherche\n"
curl --progress-bar -o ./data/2XK.skos http://mapping-tables.daf.intra.inist.fr/loterre-structures-recherche.xml

printf "3JP\n"
curl --progress-bar -o ./data/3JP.skos "$(get_url 3JP)"

printf "73G\n"
curl --progress-bar -o ./data/73G.skos "$(get_url 73G)"

printf "9SD - loterre-pays\n"
curl --progress-bar -o ./data/9SD.skos "$(get_url 9SD)"

printf "BVM\n"
curl --progress-bar -o ./data/BVM.skos http://mapping-tables.daf.intra.inist.fr/BVM.skos

printf "D63 - loterre-communes\n"
curl --progress-bar -o ./data/D63.skos "$(get_url D63)"

printf "JVR - loterre-mesh\n"
curl --progress-bar -o ./data/JVR.skos http://mapping-tables.daf.intra.inist.fr/loterre-mesh.xml

printf "MDL\n"
curl --progress-bar -o ./data/MDL.skos "$(get_url MDL)"

printf "N9J\n"
curl --progress-bar -o ./data/N9J.skos http://mapping-tables.daf.intra.inist.fr/N9J.skos

printf "P21\n"
curl --progress-bar -o ./data/P21.skos "$(get_url P21)"

printf "P66\n"
curl --progress-bar -o ./data/P66.skos "$(get_url P66)"

printf "QX8\n"
curl --progress-bar -o ./data/QX8.skos http://mapping-tables.daf.intra.inist.fr/QX8.skos
