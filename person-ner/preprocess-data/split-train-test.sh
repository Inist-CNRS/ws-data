#!/bin/bash

input_file="corpus_aij_wikiner_wp3.txt"
train_file="train_corpus_aij_wikiner_wp3.txt"
test_file="test_corpus_aij_wikiner_wp3.txt"

> "$train_file"
> "$test_file"

sentence=""
while IFS= read -r line
do
  # Si la ligne est vide (split des phrase), on décide si la phrase va dans le test ou le train
  if [[ -z "$line" ]]; then
    # Si la phrase est vide, on passe à la suivante
    if [ -n "$sentence" ]; then
      # On tire aléatoirement pour savoir si on ajoute la phrase dans le jeu de test ou de train
      if (( RANDOM % 5 == 0 )); then
        echo "$sentence" >> "$test_file"
      else
        echo "$sentence" >> "$train_file"
      fi
    fi
    sentence=""
  else
    sentence+="$line"$'\n'
  fi
done < "$input_file"

# Pour la dernière phrase
if [ -n "$sentence" ]; then
  if (( RANDOM % 5 == 0 )); then
    echo "$sentence" >> "$test_file"
  else
    echo "$sentence" >> "$train_file"
  fi
fi

echo "Séparation terminée : $train_file et $test_file"
