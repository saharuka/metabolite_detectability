AP-MALDI matrix comparison project

1) Stitch low mass range and high mass range datasets. Upload them to METASPACE with only custom DB, adducts and neutral losses of interest.

Use notebook: stitch_and_upload_datasets.ipynb
In/out directory: 1_stitch_and_upload_datasets

2) Align spot grid with the datasets

Use notebook: ../grid_calibration_tool/grid_calibration_tool.ipynb
In/out directory: 2_grid_calibration 

3)  Train and evaluate ML image classification model based on a set of input labelled images.

Use notebook: train_classifier.ipynb
In/out directory: 3_train_classifier

4) Apply trained model to all ion images on METASPACE, and curate predicitons

Use notebook: apply_classifier.ipynb
In/out directory: 4_apply_classifier

5) Store data for analysis  This includes files with ion metrics/predictions, compound classification and compound metadata

In/out directory: 5_data

6) Perform analysis and make figures

In/out directory: 6_figures