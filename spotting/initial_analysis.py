# Main script to apply spot mask generated Jupyter notebooks to images from metaspace
# and calculate various metrics

from analysistools.metaspace import get_results


ds_name = '2020-03-12_Lipid_Array_1_DAN_POS_100x220_200umSS_33at'
fdr = 0.5
databases = ['SwissLipids-2018-02-02']
results = get_results(
    dataset=ds_name,
    fdr=fdr,
    databases=databases
)

