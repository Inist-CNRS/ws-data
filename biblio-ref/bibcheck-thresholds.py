#!/usr/bin/env python3

import bibref.bibref_functions as bf
import json
import sklearn.metrics as skl
import matplotlib.pyplot as plt
import numpy as np
import sys
from sklearn.metrics import classification_report
import pandas as pd

i=0
found_references_threshold = []
false_found_references_threshold = []

# error_found = ["Granum, P. E., and Braid-Parker, T. (2000). \u201cBacillus species,\u201d in The microbiological safety and quality of food. 2. Editors B. Lund, T. Braid-Parker, and W. Gould (Gaithersburg, MD, USA: Aspen Publishers), 1029\u20131039.", "Jouison, P. (1986/1995). \u00c9crits sur la Langue des Signes Fran\u00e7aise. Edition prepared by B. Garcia. Paris: L\u2019Harmattan.", "Lyons, J. (1977). Semantics. Volume II. Cambridge, MA: Cambridge University Press.", "Casey, E. S. (2007). The world at a glance. Bloomington: University of Indiana Press.", "Agriculture Census 2015\u201316 (2019). Phase I: All India Report on Number and Area of Operational Holdings. New Delhi: Agriculture Census Division, Department of Agriculture, Co-Operation & Farmers Welfare, Ministry of Agriculture & Farmers Welfare, Government of India.", "Bhargava, A., Boudot, C., Butler, A., Chom,\u00e9, G., Gupta, K., Singh, R., et al. (2017). Conservation Agriculture: Documenting Adoption Across the Gangetic Plains of India. Chennai: IFMR LEAD and CGIAR Independent Science and Partnership Council.", "GoI (2020). Agricultural Statistics at a Glance - 2019. New Delhi: Ministry of Agriculture and Farmers Welfare, Government of India.", "CEVA (2019). R\u00e9glementation algues alimentaires. Pleubian, France: Centre d'\u00c9tude et de Valorisation des Algues.", "Brown, T., Mann, B., Ryder, N., Subbiah, M., Kaplan, J. D., Dhariwal, P., et al. (2020). \u201cLanguage models are few-shot learners,\u201d in Advances in Neural Information Processing Systems (Curran Associates, Inc.), 1877\u20131901.", "Li, R., Kahou, S., Schulz, H., Michalski, V., Charlin, L., and Pal, C. (2018). \u201cTowards deep conversational recommendations,\u201d in Proceedings of the 32nd International Conference on Neural Information Processing Systems, NIPS'18 (Red Hook, NY, USA: Curran Associates Inc.), 9748\u20139758.", "Lundberg, S. M., and Lee, S.-I. (2017). \u201cA unified approach to interpreting model predictions,\u201d in Proceedings of the 31st International Conference on Neural Information Processing Systems, NIPS'17 (Red Hook, NY, USA: Curran Associates Inc.), 4768\u20134777.", "Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., Sutskever, I., et al. (2019). Language models are unsupervised multitask learners. OpenAI blog 1:9.", "Raffel, C., Shazeer, N., Roberts, A., Lee, K., Narang, S., Matena, M., et al. (2020). Exploring the limits of transfer learning with a unified text-to-text transformer. J. Mach. Learn. Res. 21, 140, 5485\u2013140, 5551.", "FAO (2016). Save and Grow in Practice: Maize, Rice and Wheat. Rome: Food and Agriculture Organization of the United Nations (FAO)."]

# for line in sys.stdin:
#     i+=1
#     try:
#         data = json.loads(line)
#     except:
#         sys.stderr.write(str(i))
#         exit()
#     ref_biblio = data["id"]
    
#     if data["expected_result"] == "found":
#         if ref_biblio in error_found:
#             false_found_references_threshold.append(bf.get_thresholds(ref_biblio))
#         else:
#             found_references_threshold.append(bf.get_thresholds(ref_biblio))
    
# print(json.dumps(found_references_threshold))
# print(json.dumps(false_found_references_threshold))

# false_found_references_threshold = [0.59, ... ]
# # found_references_threshold= [1.0, ... ]

colors = ["blue", "lime"]
plt.hist([found_references_threshold, false_found_references_threshold], color=colors, stacked= True)
plt.title("Repartition des seuils de similarités des titres sur les références labellisées found")
plt.xlabel("seuil, en vert les erreurs de prédictions et en bleu les bonnes prédictions", fontweight='bold')
plt.ylabel("occurence", fontweight='bold')
plt.savefig("repartition-seuil-titre.png")
plt.close()
