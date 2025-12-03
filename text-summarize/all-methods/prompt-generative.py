import torch
import json
import requests
import pandas as pd
from tqdm import tqdm


# Phi3 model
from transformers import AutoTokenizer, AutoModelForCausalLM
tokenizer = AutoTokenizer.from_pretrained("microsoft/Phi-3-mini-4k-instruct", trust_remote_code=True)
model = AutoModelForCausalLM.from_pretrained("microsoft/Phi-3-mini-4k-instruct", trust_remote_code=True).to("cuda")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# Une méthode de prompt-engineering pour comparer
def get_template(txt_from_pdf):
    template = f"""
Here is a scientific article from a pdf:
<text>
{txt_from_pdf}
</text>
Generate an abstract of this document as a scientific.
<answer>
<abstract>The abstract of the scientific article.<abstract>
</answer>
End here with then endoftext token.

Here is your structured answer:
<answer>
"""
    return template


def generation(prompt, **gen_parameters):
    """Generate text from a prompt and print it."""
    model_inp = tokenizer(prompt, return_tensors="pt").to("cuda")
    # the generate() method is a succession of forward (auto-regressive) 
    out = model.generate(input_ids=model_inp["input_ids"], eos_token_id=tokenizer.eos_token_id, **gen_parameters)

    return tokenizer.decode(out[0]).replace(prompt, "")


def extract_structured_metadata(text):
    try:
        answer = generation(text, do_sample=False, max_new_tokens=500).split("</answer>")[0]
    except Exception as e:
        print(str(e))
        answer = ""

    res = {
        "abstract": ""
        }
    for elt in res:
        try:
            res[elt] = answer.split(f"<{elt}>")[1].split(f"</{elt}>")[0]
        except Exception as e:
            print(str(e))
            res[elt] = ""
    return res


def complete_metadata(text, res, max_try=3):
    to_complete = []
    for elt in res:
        if res[elt] == "":
            to_complete.append(elt)
    i = 0
    while i < max_try and to_complete != []:
        i += 1
        res2 = extract_structured_metadata(text)

        for elt in to_complete:
            if res2[elt] != "":
                res[elt] = res2[elt]
                to_complete.remove(elt)

    return res


with open("./data-scisumm/corpus-scisumm.json", "r") as f:
    data = json.load(f)

y_true = []
y_pred = []
for i in tqdm(range(len(data)), desc="Traitement", unit="itération"):
    y_true.append(data[i]["abstract"])
    full_text = data[i]["full_text"]

    try:
        if len(full_text) > 10000:
            full_text = full_text[:10000]
        template = get_template(full_text)
        res = extract_structured_metadata(template)
        res = complete_metadata(template, res, max_try=3)

        y_pred.append(res["abstract"])
    except Exception as e:
        print(e)
        y_pred.append("")


with open("res_file_prompt.json", "w") as f:
    json.dump({"y_true": y_true, "y_pred": y_pred}, f)
