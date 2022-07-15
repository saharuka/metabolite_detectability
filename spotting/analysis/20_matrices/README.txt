Analysis of 20 matrices project
In/out folders are on group drive (only a few files are on Gitlab)

1) Stitch low mass range and high mass range datasets. Upload them to METASPACE with only custom DB, adducts and neutral losses of interest.

Use notebook: stitch_and_upload_datasets.ipynb
In/out directory: ROOT_DIR/1_stitch_and_upload_datasets

2) Align spot grid with the datasets

Use notebook: ../grid_calibration_tool/Calibration tool.ipynb
In/out directory: 2_grid_calibration 

3)  Train and evaluate ML image classification models based on a set of input labelled images.

Use notebook: train_model.ipynb
In/out directory: 3_model_evaluation

4) Apply trained model to all ion images on METASPACE, and curate predicitons

Use notebook: apply_trained_model
In/out directory: 4_model_application

5) Analyse data.  This includes files with ion metrics/predictions, compound classification and compound metadata

In/out directory: 5_data_analysis

6) Make variuos plots

In/out directory: 6_plots