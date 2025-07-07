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

printf "1WB -Transferts de chaleur\n"
curl --progress-bar -o ./data/1WB.skos "$(get_url 1WB)"

printf "216 - Sciences de l'éducation\n"
curl --progress-bar -o ./data/216.skos http://mapping-tables.daf.intra.inist.fr/216.skos

printf "26L - Sciences de la terre\n"
curl --progress-bar -o ./data/26L.skos "$(get_url 26L)"

print "27X - Art et Archéologie\n"
curl --progress-bar -o ./data/27X.skos "$(get_url 27X)"

# printf "2CX - Santé Psy\n"
# curl --progress-bar -o ./data/2CX.skos "$(get_url 2CX)"

# printf "2QZ - Mécanique des fluides\n"
# curl --progress-bar -o ./data/2QZ.skos "$(get_url 2QZ)"

printf "2XK - loterre-structures-recherche\n"
curl --progress-bar -o ./data/2XK.skos http://mapping-tables.daf.intra.inist.fr/loterre-structures-recherche.xml

# printf "37T - Chimie\n"
# curl --progress-bar -o ./data/37T.skos "$(get_url 37T)"

printf "3JP - Sciences sociales\n"
curl --progress-bar -o ./data/3JP.skos "$(get_url 3JP)"

printf "3WV - Écotoxicologie\n"
curl --progress-bar -o ./data/3WV.skos "$(get_url 3WV)"

printf "4V5 - Histoire et sciences des religions\n"
curl --progress-bar -o ./data/4V5.skos "$(get_url 4V5)"

printf "73G - Philosophie\n"
curl --progress-bar -o ./data/73G.skos "$(get_url 73G)"

printf "8HQ - Tableau périodique des éléments\n"
curl --progress-bar -o ./data/8HQ.skos "$(get_url 8HQ)"

printf "8LP - Vocabulaire du traitement automatique des langues\n"
curl --progress-bar -o ./data/8LP.skos "$(get_url 8LP)"

printf "905 - Préhistoire et Protohistoire\n"
curl --progress-bar -o ./data/905.skos "$(get_url 905)"

printf "9SD - Pays et subdivisions\n"
curl --progress-bar -o ./data/9SD.skos http://mapping-tables.daf.intra.inist.fr/loterre-pays.xml

# printf "ADM - Sciences administratives\n"
# curl --progress-bar -o ./data/ADM.skos "$(get_url ADM)"

# printf "ASYSEL - Agriculture et systèmes d'élevage\n"
# curl --progress-bar -o ./data/ASYSEL.skos "$(get_url ASYSEL)"

# printf "BJW - Électrotechnique - Électroénergétique\n"
# curl --progress-bar -o ./data/BJW.skos "$(get_url BJW)"

# printf "BL8 - Nutrition artificielle\n"
# curl --progress-bar -o ./data/BL8.skos "$(get_url BL8)"

printf "BLH - Biodiversité\n"
curl --progress-bar -o ./data/BLH.skos "$(get_url BLH)"

printf "BRMH - Biotechnologies de la reproduction\n"
curl --progress-bar -o ./data/BRMH.skos "$(get_url BRMH)"

printf "BVM - NETSCITY\n"
curl --progress-bar -o ./data/BVM.skos http://mapping-tables.daf.intra.inist.fr/BVM.skos

printf "C0X - Covid-19\n"
curl --progress-bar -o ./data/C0X.skos "$(get_url C0X)"

# printf "CHC - Changement climatique\n"
# curl --progress-bar -o ./data/CHC.skos "$(get_url CHC)"

printf "CUEX - La cuisson-extrusion\n"
curl --progress-bar -o ./data/CUEX.skos "$(get_url CUEX)"

printf "D63 - Communes de France\n"
curl --progress-bar -o ./data/D63.skos "$(get_url D63)"

printf "DOM - Domaines scientifiques\n"
curl --progress-bar -o ./data/DOM.skos "$(get_url DOM)"

printf "EMTD - Écologie microbienne du tube digestif\n"
curl --progress-bar -o ./data/EMTD.skos "$(get_url EMTD)"

printf "ERC - Classification de l'ERC\n"
curl --progress-bar -o ./data/ERC.skos "$(get_url ERC)"

printf "FMC - Optique\n"
curl --progress-bar -o ./data/FMC.skos "$(get_url FMC)"

printf "G9G - Taxonomie des poissons\n"
curl --progress-bar -o ./data/G9G.skos "$(get_url G9G)"

printf "GGMGG - Génétique moléculaire\n"
curl --progress-bar -o ./data/GGMGG.skos "$(get_url GGMGG)"

printf "GT - Vocabulaire thématique de géographie\n"
curl --progress-bar -o ./data/GT.skos "$(get_url GT)"

printf "IDIA - L'ionisation dans l'industrie agro-alimentaire\n"
curl --progress-bar -o ./data/IDIA.skos "$(get_url IDIA)"

# printf "INS - Santé à l'INSB\n"
# curl --progress-bar -o ./data/INS.skos "$(get_url INS)"

printf "JVR - loterre-mesh\n"
curl --progress-bar -o ./data/JVR.skos http://mapping-tables.daf.intra.inist.fr/loterre-mesh.xml

# printf "KFP - CHEBI\n"
# curl --progress-bar -o ./data/KFP.skos "$(get_url KFP)"

printf "KG7 - Géographie de l'Amérique du Nord\n"
curl --progress-bar -o ./data/KG7.skos "$(get_url KG7)"

printf "KW5 - Ethnologie\n"
curl --progress-bar -o ./data/KW5.skos "$(get_url KW5)"

printf "LTK - ThesoTM\n"
curl --progress-bar -o ./data/LTK.skos "$(get_url LTK)"

printf "MDL - Astronomie\n"
curl --progress-bar -o ./data/MDL.skos "$(get_url MDL)"

printf "N9J - Sciences sociales SAGE\n"
curl --progress-bar -o ./data/N9J.skos http://mapping-tables.daf.intra.inist.fr/N9J.skos

printf "NHT - Physique de l'état condensé\n"
curl --progress-bar -o ./data/NHT.skos "$(get_url NHT)"

printf "PAN - Panification au levain naturel\n"
curl --progress-bar -o ./data/PAN.skos "$(get_url PAN)"

print "PSR - Mathématiques\n"
curl --progress-bar -o ./data/PSR.skos "$(get_url PSR)"

printf "P21 - Littérature\n"
curl --progress-bar -o ./data/P21.skos "$(get_url P21)"

printf "P66 - Mémoire\n"
curl --progress-bar -o ./data/P66.skos "$(get_url P66)"

# printf "PLP - Pédologie\n"
# curl --progress-bar -o ./data/PLP.skos "$(get_url PLP)"

# printf "Q1W - Agroalimentaire\n"
# curl --progress-bar -o ./data/Q1W.skos "$(get_url Q1W)"

# printf "QJP - Sciences de l'ingénieur\n"
# curl --progress-bar -o ./data/QJP.skos "$(get_url QJP)"

printf "QX8 - Paléoclimatologie\n"
curl --progress-bar -o ./data/QX8.skos http://mapping-tables.daf.intra.inist.fr/QX8.skos

printf "RDR - Électronique\n"
curl --progress-bar -o ./data/RDR.skos "$(get_url RDR)"

printf "RVQ - Composés inorganiques\n"
curl --progress-bar -o ./data/RVQ.skos "$(get_url RVQ)"

# printf "SCO - Sections du Comité National de la recherche scientifique\n"
# curl --progress-bar -o ./data/SCO.skos "$(get_url SCO)"

# printf "SEN - Santé et environnement\n"
# curl --progress-bar -o ./data/SEN.skos "$(get_url SEN)"

printf "SN8 - Théorie et traitement du signal\n"
curl --progress-bar -o ./data/SN8.skos "$(get_url SN8)"

# printf "TECSEM - Technologie des semences\n"
# curl --progress-bar -o ./data/TECSEM.skos "$(get_url TECSEM)"

printf "th63 - Nomenclature zoologique\n"
curl --progress-bar -o ./data/th63.skos "$(get_url th63)"

# printf "Theremy - Taxonomie et thésaurus pour la méthodologie de recherche en santé\n"
# curl --progress-bar -o ./data/Theremy.skos "$(get_url Theremy)"

printf "TSM - Techniques de séparation par membranes\n"
curl --progress-bar -o ./data/TSM.skos "$(get_url TSM)"

printf "TSO - Science ouverte\n"
curl --progress-bar -o ./data/TSO.skos "$(get_url TSO)"

printf "TSP - Santé publique\n"
curl --progress-bar -o ./data/TSP.skos "$(get_url TSP)"

printf "VH8 - Pathologies humaines\n"
curl --progress-bar -o ./data/VH8.skos "$(get_url VH8)"

printf "VPAC - Vocabulaire des la Politique Agricole Commune\n"
curl --progress-bar -o ./data/VPAC.skos "$(get_url VPAC)"

printf "W7B - Transfusion sanguine\n"
curl --progress-bar -o ./data/W7B.skos "$(get_url W7B)"

# Absent du lodex: https://data.istex.fr/instance/terminologies-liens
# printf "X64 - Linguistique\n"
# curl --progress-bar -o ./data/X64.skos "$(get_url X64)"

printf "XD4 - Histoire des sciences et techniques\n"
curl --progress-bar -o ./data/XD4.skos "$(get_url XD4)"
