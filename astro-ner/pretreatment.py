import pickle
import os
import pandas as pd
import numpy as np
import random

if 0:
    # mettre à 0 quand annotation.pickle est créé
    abreviation = {
        "Planète": "PL",
        "Trou noirs, quasars et apparentés": "TNQ",
        "Satellite naturel": "SNAT",
        "Objets artificiels": "OA",
        "Système solaire": "SSO",
        "Étoiles binaires (et pulsars)": "EB",
        "Étoiles": "ET",
        "Nébuleuse et région apparentés": "NRA",
        "Constellations": "CST",
        "Galaxies et amas de galaxie": "GAL",
        "Astèroïdes": "AST",
        "Satue hypotétique": "ST",
        "amas stellaires": "AS",
        "supernovas": "SN",
        "exoplanètes": "XPL",
        "sursaut radio, source radio, autres sursauts": "SR",
    }

    # charger les données
    df = pd.read_excel("astro.xlsx")

    my_dict = {}
    for column in df.columns:
        elements = df[column].dropna()
        for element in elements:
            sub_elements = element.split(";")
            for sub_element in sub_elements:
                entitie = sub_element.strip()
                my_dict[entitie] = [column]
    my_dict_unique = {}
    for cle, value in my_dict.items():
        if cle not in my_dict_unique and cle != "":
            cle = cle.replace("\n ", "").replace(" \n", "")
            # cle_lower = cle.lower()
            my_dict_unique[cle] = value

    def wordTrans(words):
        # words = ast.literal_eval(words)
        L = []
        for word in words:
            save = word
            finalFile = []
            end = [".", ",", ";", ":", "»", ")", "’", "'"]
            start = ["«", "(", ".", "‘"]
            middle = [
                "l'",
                "d'",
                "j'",
                "L'",
                "D'",
                "J'",
                "l’",
                "d’",
                "j’",
                "L’",
                "D’",
                "J’",
            ]
            queue = []

            File = word.split()
            for Word in File:
                word = Word
                for execp in start:
                    if word.startswith(execp):
                        finalFile.append(word[0])
                        word = word[1:]
                for execp in middle:
                    if word.startswith(execp):
                        finalFile.append(word[:2])
                        word = word[2:]
                for execp in end:
                    if word.endswith(execp):
                        queue.insert(0, word[-1])
                        word = word[:-1]

                if word.endswith("’s"):
                    queue.insert(0, "s")
                    queue.insert(0, "’")
                    word = word[:-2]

                finalFile.append(word)
                for i in queue:
                    finalFile.append(i)
                queue = []

            if finalFile == ["a"]:
                print("word = ", save)

            L.append(" ".join(finalFile))
        return L

    def split_txt(txt):
        splt = []
        start = 0
        for i, letter in enumerate(txt):
            if letter == ".":
                if (
                    (
                        txt[i - 1].islower()
                        and txt[i - 2].islower()
                        and (txt[i - 2: i] not in ["Dr", "no"])
                    )
                    or (txt[i - 1] == ")")
                    or (
                        i + 1 < len(txt)
                        and not (txt[i - 1].isnumeric() and txt[i + 1].isnumeric())
                    )
                ):
                    sent = txt[start: i + 1]
                    start = i + 1
                    splt.append(sent)
        return splt

    dirname = []

    def listdirs(rootdir):
        if not os.path.exists(rootdir):
            print(f"Le répertoire '{rootdir}' n'existe pas.")
            return

        result = []

        for subdir in os.listdir(rootdir):
            subdir_path = os.path.join(rootdir, subdir)
            if os.path.isdir(subdir_path):
                for f in os.listdir(subdir_path):
                    f_path = os.path.join(subdir_path, f)
                    if (
                        os.path.isfile(f_path)
                        and f == "data-ocr"
                        or f.endswith(".txt")
                        or f.endswith(".ocr")
                    ):
                        try:
                            with open(f_path, "r") as file:
                                dirname.append(subdir)
                                content = file.read()
                                file = split_txt(content)
                                text = wordTrans(file)
                                result.append(text)
                        except Exception as e:
                            print(
                                f"Erreur lors de la lecture de {f_path}: {e}")
                        break
        return result

    rootdir = "data-istex"
    processed_texts = listdirs(rootdir)

    total_sent = []
    total_annot = []

    for index, text in enumerate(processed_texts):
        print(
            "text ",
            index + 1,
            " sur ",
            len(processed_texts),
            " nom du répertoire : ",
            dirname[index],
        )

        for elements in text:
            element = elements.split(" ")
            # element = [e.lower() for e in element_upper]
            annotation = ["O"] * len(element)
            for key, value in my_dict_unique.items():
                cle = wordTrans([key])[0].split()
                for i in range(len(element) - len(cle)):
                    if cle == element[i: i + len(cle)] and key != " ":
                        # print(value)
                        if value[0] in abreviation:
                            if len(cle) == 1:
                                annotation[i] = "S-" + abreviation[value[0]]
                            else:
                                annotation[i: i + len(cle)] = [
                                    "I-" + abreviation[value[0]]
                                ] * len(cle)
                                annotation[i + len(cle) - 1] = (
                                    "E-" + abreviation[value[0]]
                                )
                                annotation[i] = "B-" + abreviation[value[0]]
            total_sent.append(element)
            total_annot.append(annotation)
        # if index == 3 :
        #     break
    # print(total_annot)
    data = {"total_sent": total_sent, "total_annot": total_annot}

    with open("annotation.pickle", "wb") as handle:
        pickle.dump(data, handle, protocol=pickle.HIGHEST_PROTOCOL)
    exit()

with open("annotation.pickle", "rb") as handle:
    b = pickle.load(handle)

total_sent = b["total_sent"]
total_annot = b["total_annot"]

temp = list(zip(total_sent, total_annot))
random.shuffle(temp)
res1, res2 = zip(*temp)
# res1 and res2 come out as tuples, and so must be converted to lists.
total_sent, total_annot = list(res1), list(res2)


proba = [0.85, 0.03, 0.12]
file = np.random.choice([0, 1, 2], 1, p=proba)
fTrain = open("train_data/train.txt", "w", encoding="utf-8")
fTest = open("train_data/test.txt", "w", encoding="utf-8")
fDev = open("train_data/dev.txt", "w", encoding="utf-8")
count: int = 0
annote: bool = False
max_word_train = 400000
word_annotated = 0
percent_annot = 0.9
for i, sent in enumerate(total_sent):
    for j, _ in enumerate(sent):
        if total_annot[i][j] != "O":
            annote = True
            word_annotated += len(sent)
            break
        if word_annotated > max_word_train * percent_annot and not annote:
            annote = True
    if annote:
        for k, word in enumerate(sent):
            if file == 0:
                fTrain.write(word + " " + total_annot[i][k] + "\n")
            elif file == 1:
                fTest.write(word + " " + total_annot[i][k] + "\n")
            else:
                fDev.write(word + " " + total_annot[i][k] + "\n")
            count += 1

        if file == 0:
            fTrain.write("\n")
            if count > max_word_train:
                break
        elif file == 1:
            fTest.write("\n")
        else:
            fDev.write("\n")
        annote = False
    file = np.random.choice([0, 1, 2], 1, p=proba)  # train-test-dev
