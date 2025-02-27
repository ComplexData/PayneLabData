#   Copyright 2019 Samuel Payne sam_payne@byu.edu
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#       http://www.apache.org/licenses/LICENSE-2.0
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

import os
import webbrowser
import textwrap
import pandas as pd
from .dataframe import DataFrameLoader
from .queries import Queries

def warning():
    print("\n","******PLEASE READ******")
    warning = "WARNING: This data is under a publication embargo until further notice. The embargo allows exploring and utilizing the data, but the data may not be in a publication until further notice."
    wrapped_list = textwrap.wrap(warning)
    for line in wrapped_list:
        print(line)

"""
Creates dictionary for linking Patient_Id with individual sample number (i.e. C3L-00006 with S001)
"""
def create_patient_ids(clinical):
    c = clinical[["Proteomics_Participant_ID"]][0:100] #S101 through S140 have no patient id
    s = c.index
    dictPrepDf = c.set_index('Proteomics_Participant_ID')
    dictPrepDf['idx'] = s
    patient_ids = dictPrepDf.to_dict()['idx']
    return patient_ids
def link_patient_ids(patient_ids, somatic):
    s = []
    for x in somatic["Patient_Id"]:
        if x in patient_ids.keys():
            s.append(patient_ids[x])
        else:
            s.append("NA")
    somatic["Clinical_Patient_Key"] = s
    return somatic
"""
Executes on import CPTAC statement. Selects files from docs folder in CPTAC package
utilizing DataFrameLoader from dataframe.py. Prints update as files are loaded into
dataframes.
"""
print("Loading Burkholderia data:")

dir_path = os.path.dirname(os.path.realpath(__file__))
data_directory = dir_path + os.sep + "data" + os.sep

print("Loading Dictionary...")
dict = {}
file = open(data_directory + "definitions.txt", "r")

for line in file:
    line = line.strip()
    line = line.split("\t")
    dict[line[0]] = line[1]
file.close()

print("Loading Burkholderia data...")
raw_data = DataFrameLoader(data_directory + "Bthai_Norm_Ref_Names.xlsx").createDataFrame()
no_glucose = [raw_data.iloc[:,5:9],
                    raw_data.iloc[:,9:13],
                    raw_data.iloc[:,13:17],
                    raw_data.iloc[:,17:21],
                    raw_data.iloc[:,21:25]]

#bthai_no_glucose_means = bthai_no_glucose[0].mean(axis=1).merge(
#                            [bthai_no_glucose[1].mean(axis=1),
#                            bthai_no_glucose[2].mean(axis=1),
#                            bthai_no_glucose[3].mean(axis=1)])
glucose = [raw_data.iloc[:,25:29],
                    raw_data.iloc[:,29:33],
                    raw_data.iloc[:,33:37],
                    raw_data.iloc[:,37:41],
                    raw_data.iloc[:,41:45]]

#metaData = MetaData(clinical)
#molecularData = MolecularData(proteomics, transcriptome, cna, phosphoproteomics)
warning()
def list():
    """
    Parameters
    None

    Prints list of loaded data frames and dimensions

    Returns
    None
    """
    print("Below are the available data frames contained in this package:")
    data = [bthai_raw, bthai_no_glucose, bthai_glucose]
    for dataframe in data:
        print("\t", dataframe.name)
        print("\t", "\t", "Dimensions:", dataframe.shape)
    print("To access the data, use a get function with the data frame name, i.e. CTPAC.get_proteomics()")
def define(term):
    """
    Parameters
    term: string of term to be defined

    Returns
    String definition of provided term
    """
    if term in dict:
        print(dict[term])
    else:
        print(term, "not found in dictionary. Alternatively, CPTAC.define() can be used to perform a web search of the term provided.")
def search(term):
    """
    Parameters
    term: string of term to be searched

    Performs online search of provided term

    Returns
    None
    """
    url = "https://www.google.com/search?q=" + term
    print("Searching for", term, "in web browser...")
    webbrowser.open(url)
def get_clinical():
    """
    Parameters
    None

    Returns
    Clincal dataframe
    """
    return clinical
def get_proteomics():
    """
    Parameters
    None

    Returns
    proteomics dataframe
    """
    return proteomics
def get_transcriptomics(circular = False, miRNA = False):
    """
    Parameters
    circular: boolean indicating whether to return circular RNA data
    miRNA: boolean indicating whether to return miRNA data

    Returns
    Transcriptomics dataframe
    """
    if circular:
        return transcriptomics_circular
    if miRNA:
        return miRNA
    return transcriptomics
def get_CNA():
    """
    Parameters
    None

    Returns
    CNA dataframe
    """
    return cna
def get_phosphoproteomics(gene_level = False):
    """
    Parameters
    gene_level: boolean indicating whether to return gene level phosphoproteomics (returns site level if false)

    Returns
    Phosphoproteomics dataframe
    """
    if gene_level:
        return phosphoproteomics_gene
    return phosphoproteomics
def get_phosphosites(gene):
    """Returns dataframe with all phosphosites of specified gene name"""
    return Utilities().get_phosphosites(phosphoproteomics, gene)
def get_somatic(binary=False, unparsed=False):
    """
    Parameters
    binary: boolean indicating whether to retrieve the somatic mutations binary data
    unparsed: boolean indicating whether to retrieve unparsed somatic mutations maf data

    Default behavior is to return parsed somatic mutations maf data

    Returns
    Somatic mutations dataframe corresponding with parameters provided
    """
    if binary:
        return somatic_binary
    if unparsed:
        return somatic_unparsed
    return somatic_maf
def get_clinical_cols():
    """
    Parameters
    None

    Returns
    List of clincal dataframe columns, aka data types (i.e. BMI, Diabetes)
    """
    return clinical.columns
def get_proteomics_cols():
    """
    Parameters
    None

    Returns
    List of columns of proteomics dataframe
    """
    return proteomics.columns
def get_transcriptomics_cols():
    """
    Parameters
    None

    Returns
    List of columns of transcriptomics dataframe
    """
    return transcriptomics.columns
def get_cohort_clinical(columns):
    """
    Parameters
    columns: single column name or array of column names to select for in the clinical dataframe

    Returns
    Dataframe of specified columns (or Series if one column) of clinical data
    """
    return clinical[columns]
def get_proteomics_quant(colon_ids):
    """
    Parameters
    colon_ids: string or list of string ids (i.e. S001, S068) to be selected from proteomics dataframe

    Returns
    Dataframe of specified rows (or Series if one row) of proteomics data
    """
    return proteomics.loc[colon_ids]
def get_cohort_proteomics(columns):
    """
    Parameters
    columns: single column name or array of column names to select for in the proteomics dataframe

    Returns
    Dataframe of specified columns (or Series if one column) of proteomics data
    """
    return proteomics[columns]
def get_cohort_transcriptomics(columns):
    """
    Parameters
    columns: single column name or array of column names to select for in the transcriptomics dataframe

    Returns
    Dataframe of specified columns (or Series if one column) of transcriptomics data
    """
    return transcriptomics[columns]
def get_cohort_cna(columns):
    """
    Parameters
    columns: single column name or array of column names to select for in the CNA dataframe

    Returns
    Dataframe of specified columns (or Series if one column) of CNA data
    """
    return cna[columns]
def get_cohort_phosphoproteomics(columns):
    """
    Parameters
    columns: single column name or array of column names to select for in the phosphoproteomics dataframe

    Returns
    Dataframe of specified columns (or Series if one column) of phosphoproteomics data
    """
    return phosphoproteomics[columns]
def get_patient_mutations(patient_id):
    """
    Parameters
    patient_id: Patient ID (i.e. C3L-00006, S018, etc.) to select from somatic mutation data

    Returns
    Dataframe containing data for provided patient ID
    """
    if len(patient_id) == 4: #S***
        return somatic_maf[somatic_maf["Patient_Id"] == patient_id]
    elif len(patient_id) > 0: #C3L-*****
        return somatic_maf[somatic_maf["Clinical_Patient_Key"] == patient_id]
    else:
        print("ERROR:", patient_id, "not a valid patient_id.")
def get_tumor_ids(tumor_type, query_type, value): #TODO: implement
    #"""
    #Parameters
    #tumor_type is the tumor type, e.g. colon
    #query_type is the type of tumor query, e.g. by SNP, mutated gene, outlier
    #value corresponds with the query type, e.g. TP53 for mutated gene or EGFR for outlier

    #Returns

    #"""
    dataframe = None #TODO what should the dataframe be?
    return Queries(dataframe).query(tumor_type, query_type, value)
def get_gene_mapping():
    #TODO implement
    return Utilities().get_gene_mapping()
def convert(snp_or_sap):
    #TODO implement
    return Utilities().convert(snp_or_sap)
def get_means(dataframe_list):
    means_df = pd.DataFrame()
    means_df['Protein'] = dataframe_list[0].index
    column_names = ['Protein']
    i = 1
    for dataframe in dataframe_list:
        means_df = pd.concat([means_df, dataframe.mean(axis=1)], axis=1, sort=True)
        column_names.append('mean' + str(i))
        i = i + 1
    means_df.columns = column_names
    means_df.drop_na(inplace=True)
    return means_df
    
def melt_time_points(dataframe):
    return pd.melt(dataframe, id_vars=['Protein'], value_vars=['mean1','mean2','mean3','mean4','mean5'], var_name='time_point')
    
def help():
    """
    Parameters
    None

    Opens github help page

    Returns
    None
    """
    print("Opening help.txt in web browser...")
    webbrowser.open("https://github.com/PayneLab/CPTAC/blob/master/doc/help.txt")
def embargo():
    """
    Parameters
    None

    Opens CPTAC embargo details in web browser

    Returns
    None
    """
    print("Opening embargo details in web browser...")
    webbrowser.open("https://proteomics.cancer.gov/data-portal/about/data-use-agreement")
def start():
    #Might remove this function
    print("Welcome to our burkholderia data. Enter CPTAC.help() to open our Github help page.")
def version():
    version = {}
    with open(dir_path + '/version.py') as fp:
    	exec(fp.read(), version)
    return(version['__version__'])
