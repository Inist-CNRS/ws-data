#!/bin/bash

input_file="corpus_aij_wikiner_wp3.txt"
train_file="train_corpus_aij_wikiner_wp3.txt"
test_file="test_corpus_aij_wikiner_wp3.txt"

> "$train_file"
> "$test_file"

sentence=""
while IFS= read -r line
do
  # Si la ligne est vide (fin de phrase), on décide si la phrase va dans le test ou le train
  if [[ -z "$line" ]]; then
    # Si la phrase est vide, on passe à la suivante
    if [ -n "$sentence" ]; then
      # Décision aléatoire pour tester si on ajoute la phrase dans test.txt ou train.txt
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

# Ne pas oublier de traiter la dernière phrase
if [ -n "$sentence" ]; then
  if (( RANDOM % 5 == 0 )); then
    echo "$sentence" >> "$test_file"
  else
    echo "$sentence" >> "$train_file"
  fi
fi

echo "Séparation terminée : $train_file et $test_file"
