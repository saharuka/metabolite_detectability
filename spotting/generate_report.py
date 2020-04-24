
# To install dependencies: pip install metaspace2020 scikit-learn scikit-image seaborn matplotlib pandas numpy openpyxl
from getpass import getpass
import json
from metaspace.sm_annotation_utils import SMInstance
import numpy as np
import pandas as pd

#Load METASPACE Data
sm = SMInstance()
sm.login(email='luca.rappez@embl.de', password='Zeppar12')
dataset_id = '2020-03-12_17h55m21s'
fdr = 0.5
database = 'SwissLipids-2018-02-02'
annotations = sm.get_annotations(fdr, database, {'ids': dataset_id})

#Load pre-generated grid mask (Jupyter Notebook)
grid_mask = np.load(f'{dataset_id}_grid_mask.npy')
positions, grid_coords, n_rows, n_cols, spot_h, spot_w, mask_names = json.load(open(f'{dataset_id}_grid_params.json'))

annotations = sm.get_annotations(fdr, database, {'ids': dataset_id})

images = sm.dataset(id=dataset_id).all_annotation_images(fdr, database, True, True)
images = dict(((img.formula, img.adduct), img[0]) for img in images)
h, w = next(iter(images.values())).shape
images_flat = np.array(list(images.values())).reshape(len(images), -1)

annotations_key = annotations.formula + annotations.adduct
result = pd.DataFrame(index=annotations.formula + annotations.adduct, columns=mask_names)

for val, col in enumerate(mask_names):
    spot_inds = np.flatnonzero(grid_mask == val)
    for img, ann in annotations_key.iteritems():
        pixels_from_spot = images_flat[img, spot_inds]
        result.loc[ann, col] = np.sum(pixels_from_spot)

    # It's nice to have the complete output, but let's compile a quick report

import re#gex

targets = pd.read_csv('Molecules.csv', sep=',', header=None)  # Generated from plate randomizer

report = pd.DataFrame(index=[targets[0], targets[2], targets[1]], columns=["Sum"])
report["Sum"] = 0
report.index.names = ["Well", "Formula", "Molecule"]

for ann in annotations.formula + annotations.adduct:
    for idx, well in enumerate(targets[0]):
        if (re.split("(\+|\-)", ann)[0]) == targets[2][idx]:
            report.iloc[idx] += result.loc[ann, well]

report