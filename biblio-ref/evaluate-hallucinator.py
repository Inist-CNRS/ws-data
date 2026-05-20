import json
from collections import defaultdict
from hallucinator import Reference, Validator, ValidatorConfig, PdfExtractor

ext = PdfExtractor()

# ATTENTION : vérifier les labels d'hallucinator
# https://github.com/gianlucasb/hallucinator/blob/main/hallucinator-rs/PYTHON_BINDINGS.md
def load_corpus(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return [json.loads(line) for line in f]


def create_reference(entry):
    return ext.parse_reference(entry["id"])


def evaluate_entry(entry, validator):
    ref = create_reference(entry)
    results = validator.check([ref])
    result = results[0]

    # Déterminer la classe prédite
    if result.retraction_info and result.retraction_info.is_retracted:
        predicted = "retracted"
    elif result.status == "verified":
        predicted = "found"
    elif result.status in ["no_match", "timeout", "rate_limited", "error", "skipped"]:
        predicted = "not_found"
    else:
        predicted = "to_be_verified"

    return {
        "id": entry["id"],
        "expected": entry["expected_result"],
        "predicted": predicted,
        "match": predicted == entry["expected_result"]
    }


def compute_accuracy(results):
    classes = ["retracted", "to_be_verified", "found"]
    accuracy = {}
    counts = defaultdict(int)
    correct = defaultdict(int)

    for r in results:
        expected = r["expected"]
        counts[expected] += 1
        if r["match"]:
            correct[expected] += 1

    for cls in classes:
        accuracy[cls] = correct[cls] / counts[cls] if counts[cls] > 0 else 0

    return accuracy, counts


def generate_report(results, accuracy, counts, output_dir="evaluation_output"):
    import os
    os.makedirs(output_dir, exist_ok=True)

    with open(f"{output_dir}/results.jsonl", "w", encoding="utf-8") as f:
        for r in results:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    with open(f"{output_dir}/accuracy.json", "w", encoding="utf-8") as f:
        json.dump({
            "accuracy": accuracy,
            "counts": dict(counts),
            "total_entries": len(results),
            "total_matches": sum(1 for r in results if r["match"])
        }, f, indent=2, ensure_ascii=False)

    print(f"Rapport généré dans {output_dir}/")


def evaluate_corpus(corpus_path, output_dir="evaluation_output"):
    # Config
    config = ValidatorConfig()
    config.disabled_dbs = []  # Désactive les DBs inutiles si besoin
    config.num_workers = 8    # Parallélisation
    config.cache_path = "hallucinator_cache.db"  # Cache
    validator = Validator(config)

    corpus = load_corpus(corpus_path)
    results = []

    # Évaluer chaque entrée
    for i, entry in enumerate(corpus):
        try:
            eval_result = evaluate_entry(entry, validator)
            results.append(eval_result)
            if (i + 1) % 10 == 0:
                print(f"Progress: {i + 1}/{len(corpus)}")
        except Exception as e:
            print(f"Erreur pour {entry['id'][:50]}: {e}")
            results.append({
                "id": entry["id"],
                "expected": entry["expected_result"],
                "predicted": "error",
                "match": False
            })

    # Calculer l'accuracy par classe
    accuracy, counts = compute_accuracy(results)

    generate_report(results, accuracy, counts, output_dir)

    # On affiche un résumé
    print("\n--- Accuracy par classe ---")
    for cls, acc in accuracy.items():
        print(f"{cls}: {acc:.2%} ({counts[cls]} entrées)")


if __name__ == "__main__":
    evaluate_corpus("corpus_eval_bibcheck_v4.jsonl")