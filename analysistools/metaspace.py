# access metaspace remotely
from metaspace import sm_annotation_utils as smau
import pandas as pd


def login_metaspace(email, password):
    """
    Log in to https://metaspace2020.eu/
    :param email: (str)
    :param password: (str)
    """
    sm = smau.SMInstance()
    sm.login(email, password)
    return sm


def filter_by_list(results, my_list):
    """
    Filter annotations by presence in a list of formulas, e.g. a list of Kegg annotations
    :param results: (DataFrame) output of get_results function
    :param my_list: (list) list of chemical formulas
    :return: (DataFrame) subset input data frame that satisfies filtering
    """

    by_list = results[results.formula.isin(my_list)]
    return by_list


def get_results(dataset, fdr, databases='all', merge_adducts=False, by_list=None):
    """
    Get results for a specific dataset from https://metaspace2020.eu/
    :param dataset: (str) dataset name
    :param fdr: (float) false discovery rate (0.05, 0.1, 0.2 or 0.5)
    :param databases: (list) names of databases to pull results from, default value all
    :param merge_adducts: (bool) if True, merge adducts into one entry
    :param by_list: (list) if provided, discard entries for formulas not in the list. Skips filtering by default
    :return: (DataFrame) summary with one entry per ion or formula
    """
    sm = login_metaspace()
    d = sm.dataset(dataset)
    df = pd.DataFrame()
    if databases == 'all': databases = d.databases
    for j, db in enumerate(databases):
        result = d.results(database=db, fdr=fdr, coloc_with=None)
        df = pd.concat([df, result.reset_index()])

        if merge_adducts:
            grouped = df.groupby('formula')  # this gets rid of both inter-database and adduct duplicates

            results = grouped.agg({  # I keep only selected columns
                'mz': 'first',
                'msm': max,
                'fdr': min,
                # 'intensity': max,  # this is the highest intensity value in first isotope image
                'moleculeIds': sum,
                'moleculeNames': sum})
            results['moleculeIds'] = results['moleculeIds'].apply(lambda x: list(set(x)))
            results['moleculeNames'] = results['moleculeNames'].apply(lambda x: list(set(x)))
            results.reset_index(inplace=True)

        elif not merge_adducts:
            grouped = df.groupby('ion')  # this gets rid of inter-database duplicates, but keeps adducts separate
            results = grouped.agg({
                'formula': 'first',
                'adduct': 'first',
                'mz': 'first',
                'msm': max,
                'fdr': min,
                'moleculeIds': sum,
                'moleculeNames': sum})
            results['moleculeIds'] = results['moleculeIds'].apply(lambda x: list(set(x)))
            results['moleculeNames'] = results['moleculeNames'].apply(lambda x: list(set(x)))
            results.reset_index(inplace=True)

        # Optional filtration by formula list
        if by_list is not None:
            results = filter_by_list(results, by_list)
    return results