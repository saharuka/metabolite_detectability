Analysis of 20 matrices project
In/out folders are on group drive (only a few files are on Gitlab)

1) Stitch low mass range and high mass range datasets. Upload them to METASPACE with only custom DB, adducts and neutral losses of interest.

Use notebook: stitch_and_upload_datasets
In/out directory: ROOT_DIR/1_stitch_and_upload_datasets

2) Align spot grid with the datasets

Use notebook: Calibration tool
In/out directory: 2_grid_calibration 

3) (Optional) Use grid information to calculate per-spot metrics for every dataset and every ion image

Use notebook: extract_metrics
In/out directory: 3_metric_extraction 

4) Train and evaluate ML image classification models based on a set of input labelled images. Choose a suitable model and apply it to all ion images on METASPACE

Use notebook: train_model
In/out directory: 4_model_evaluation

5) Analyse data.  This includes files with ion metrics/predictions, compound classification and compound metadata. Make plots

In/out directory: 5_dataframes

6) Make variuos plots

In/out directory: 6_plots