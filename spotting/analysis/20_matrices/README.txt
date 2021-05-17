Analysis of 20 matrices project
In/out folders are on group drive (only a few files are on Gitlab)

1) Stitch low mass range and high mass range datasets. Upload them to staging.metaspace with only custom DB, adducts and neutral losses of interest.

Use notebook: stitch_and_upload_datasets
In/out directory: ROOT_DIR/1_stitch_and_upload_datasets

2) Align spot grid with the datasets

Use notebook: Calibration tool
In/out directory: 2_grid_calibration 

3) Use grid information to calculate per-spot metrics for every dataset and every ion image

Use notebook: extract_metrics
In/out directory: 3_metric_extraction 

4) Use obtained metrics to calculate some ratios (this required no image data)

Use notebook: extend_metrics
In/out directory: 4_metric_extension

5) Use a labelled set to classify all wells as filled or empty. Based on this, classify images as good or bad quality.

Use notebook: classify_wells_and_images
In/out directory: 5_well_classification