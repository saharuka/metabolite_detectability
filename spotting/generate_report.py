# To install dependencies: pip install metaspace2020 scikit-learn scikit-image seaborn matplotlib pandas numpy openpyxl
from getpass import getpass
import json
from metaspace.sm_annotation_utils import SMInstance
import numpy as np
import pandas as pd
import re#gex
import tkinter as tk
from tkinter import filedialog
from definitions import ROOT_DIR

#Load METASPACE Data
sm = SMInstance()
sm.login(email='luca.rappez@embl.de', password='Zeppar12')
dataset_id = '2020-03-12_17h55m21s'
fdr = 0.5
database = 'SwissLipids-2018-02-02'
annotations = sm.get_annotations(fdr, database, {'ids': dataset_id})

#Load pre-generated grid mask (Jupyter Notebook)
grid_mask = np.load(f'{ROOT_DIR}\\data\\grid_masks\\{dataset_id}.npy')
mask_names = json.load(open(f'{ROOT_DIR}\\data\\grid_masks\\{dataset_id}_mask_names.json'))

#Store all annotation images
images = sm.dataset(id=dataset_id).all_annotation_images(fdr, database, True, True)
images = dict(((img.formula, img.adduct), img[0]) for img in images)
h, w = next(iter(images.values())).shape
images_flat = np.array(list(images.values())).reshape(len(images), -1)

#Create result matrix structure
annotations_key = annotations.formula + annotations.adduct
result_sum = pd.DataFrame(index=annotations.formula + annotations.adduct, columns=mask_names)
result_mean = pd.DataFrame(index=annotations.formula + annotations.adduct, columns=mask_names)
result_std = pd.DataFrame(index=annotations.formula + annotations.adduct, columns=mask_names)
result_occ = pd.DataFrame(index=annotations.formula + annotations.adduct, columns=mask_names)

for val, col in enumerate(mask_names): #For each well
    spot_inds = np.flatnonzero(grid_mask == val)   #Find all the pixel co-ordinates that are part of the well
    for img, ann in annotations_key.iteritems():    #For each image
        pixels_from_spot = images_flat[img, spot_inds]  #Load all the pixels in the well
        #Update all result matrices
        result_sum.loc[ann, col] = np.sum(pixels_from_spot) #Sum abundance in well
        result_mean.loc[ann, col] = np.average(pixels_from_spot)  #Average abundance in well
        result_std.loc[ann, col] = np.std(pixels_from_spot) #Standard deviation
        result_occ.loc[ann, col] = (np.count_nonzero(pixels_from_spot) / pixels_from_spot.size) * 100 # % of pixels that have non-zero values

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

#Ask user for output folder
print('Analysis complete, select output folder')
root = tk.Tk()
root.withdraw()
outdir = filedialog.askdirectory()

#Output a bunch of excel reports
report.to_excel(f'{outdir}/{dataset_id}_{fdr}_{database}_report.xlsx')
result_sum.to_excel(f'{outdir}/{dataset_id}_{fdr}_{database}_sum.xlsx')
result_mean.to_excel(f'{outdir}/{dataset_id}_{fdr}_{database}_mean.xlsx')
result_std.to_excel(f'{outdir}/{dataset_id}_{fdr}_{database}_std.xlsx')
result_occ.to_excel(f'{outdir}/{dataset_id}_{fdr}_{database}_occ.xlsx')

print('All done, have a wonderful day!')