#!/usr/bin/env bun

import { parseArgs } from 'util';
import path from 'path';
import { XMLParser } from 'fast-xml-parser';
import { depleteString } from '../src/strings';

async function getRNSR(path: string) {
    const RNSRXML = await Bun.file(path).text();
    const parser = new XMLParser({
        ignoreAttributes: true,
        ignoreDeclaration: true,
        processEntities: false,
        trimValues: true,
    });
    const RNSR = parser.parse(RNSRXML);
    return RNSR;
}

const simplifyEtabAssoc = (etabAssoc: {
    etab: { sigle: any; libelle: any };
    label: any;
    numero: any;
}) => {
    const simplifiedEtab = {
        sigle: etabAssoc.etab.sigle,
        libelle: etabAssoc.etab.libelle,
        sigleAppauvri: depleteString(etabAssoc.etab.sigle),
        libelleAppauvri: depleteString(etabAssoc.etab.libelle),
    };
    const simplifiedEtabAssoc = {
        etab: simplifiedEtab,
        label: etabAssoc.label,
        labelAppauvri: depleteString(etabAssoc.label),
        numero: etabAssoc.numero,
    };
    return simplifiedEtabAssoc;
};

const isTutelle = (etabAssoc: { natTutEtab: string }) =>
    etabAssoc.natTutEtab === 'TUTE';

const simplifyStructure = (structure: {
    etabAssoc: any[];
    num_nat_struct: any;
    intitule: any;
    sigle: any;
    ville_postale: any;
    code_postal: any;
    annee_creation: any;
    an_fermeture: number;
}) => {
    if (!structure.etabAssoc) return structure;
    let simplifiedEtabAssoc;
    if (Array.isArray(structure.etabAssoc)) {
        simplifiedEtabAssoc = structure.etabAssoc
            .filter(isTutelle)
            .map(simplifyEtabAssoc);
    } else {
        simplifiedEtabAssoc = [simplifyEtabAssoc(structure.etabAssoc)];
    }
    const simplifiedStructure = {
        num_nat_struct: structure.num_nat_struct,
        intitule: structure.intitule,
        sigle: structure.sigle,
        ville_postale: structure.ville_postale,
        code_postal: structure.code_postal,
        etabAssoc: simplifiedEtabAssoc,
        intituleAppauvri: depleteString(structure.intitule),
        sigleAppauvri: depleteString(structure.sigle),
        ville_postale_appauvrie: depleteString(structure.ville_postale),
        annee_creation: structure.annee_creation,
        an_fermeture: Number(structure.an_fermeture),
    };
    return simplifiedStructure;
};

const {
    values: { file },
} = parseArgs({
    args: Bun.argv,
    options: {
        file: {
            type: 'string',
            short: 'f',
            name: 'file',
        },
    },
    strict: true,
    allowPositionals: true,
});

if (!file) {
    console.error('No file specified, use -f <path>');
    process.exit(1);
}

getRNSR(file)
    .then((rnsr) => {
        const simplifiedStructures =
            rnsr.structures.structure.map(simplifyStructure);
        const simplifiedRnsr = {
            structures: { structure: simplifiedStructures },
        };
        return simplifiedRnsr;
    })
    .then((simplifiedRnsr) =>
        Bun.write(
            path.join(__dirname, '../data/RNSR.json'),
            JSON.stringify(simplifiedRnsr),
        ),
    )
    .then(() => {
        console.log('data/RNSR.json updated');
    });
