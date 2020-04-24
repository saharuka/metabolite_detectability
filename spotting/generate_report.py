# To install dependencies: pip install metaspace2020 scikit-learn scikit-image seaborn matplotlib pandas numpy openpyxl
from getpass import getpass
import json
from metaspace.sm_annotation_utils import SMInstance
import numpy as np
import pandas as pd
import re#gex

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
result_sum = pd.DataFrame(index=annotations.formula + annotations.adduct, columns=mask_names)
result_mean = pd.DataFrame(index=annotations.formula + annotations.adduct, columns=mask_names)
result_std = pd.DataFrame(index=annotations.formula + annotations.adduct, columns=mask_names)
result_occ = pd.DataFrame(index=annotations.formula + annotations.adduct, columns=mask_names)

for val, col in enumerate(mask_names):
    spot_inds = np.flatnonzero(grid_mask == val)
    for img, ann in annotations_key.iteritems():
        pixels_from_spot = images_flat[img, spot_inds]
        result_sum.loc[ann, col] = np.sum(pixels_from_spot)
        result_mean.loc[ann, col] = np.average(pixels_from_spot)
        result_std.loc[ann, col] = np.std(pixels_from_spot)
        result_occ.loc[ann, col] = (np.count_nonzero(pixels_from_spot) / pixels_from_spot.size) * 100

targets = pd.read_csv('Molecules.csv', sep=',', header=None)  # Generated from plate randomizer

#Define report structure
report = pd.DataFrame(index=[targets[0], targets[2], targets[1]], columns=["Sum","Mean","Standard Deviation","%occupancy"])
report["Sum"] = report["Mean"] = report["Standard Deviation"] = report["%occupancy"] = 0
report.index.names = ["Well", "Formula", "Molecule"]

#Calulate...
for ann in annotations.formula + annotations.adduct:  #...for each annotation
    for idx, well in enumerate(targets[0]): #...for each target molecule
        if (re.split("(\+|\-)", ann)[0]) == targets[2][idx]: #...if annotation is an adduct of target
            if (report.iloc[idx][1] < result_sum.loc[ann, well]): #...if the sum intensity is the highest so far for this well
                report.iloc[idx] = [result_sum.loc[ann, well],result_mean.loc[ann, well],result_std.loc[ann, well],result_occ.loc[ann, well]]  #...report results for this well

#Output a bunch of excel reports
report.to_excel(f'{dataset_id}_{fdr}_{database}_report.xlsx')
result_sum.to_excel(f'{dataset_id}_{fdr}_{database}_sum.xlsx')
result_mean.to_excel(f'{dataset_id}_{fdr}_{database}_mean.xlsx')
result_std.to_excel(f'{dataset_id}_{fdr}_{database}_std.xlsx')
result_occ.to_excel(f'{dataset_id}_{fdr}_{database}_occ.xlsx')