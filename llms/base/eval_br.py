"""
Model Evaluation and Results Processing Module

This module provides functionality for evaluating and analyzing AI model performance
on benchmark tasks. It handles result storage, processing, and metric calculations
for comparing different language models.

Key Features:
    - Result initialization and storage management
    - Response processing and validation
    - Performance metric calculations (accuracy, latency, efficiency)
    - Result aggregation and analysis
    - Error margin calculations
    - Cost-effectiveness analysis

The module supports both standard and chain-of-thought (CoT) evaluation approaches,
with built-in handling for various response formats and validation requirements.

Main Functions:
    - init_model_sheet: Creates template for storing evaluation results
    - save_results: Persists evaluation results to JSON files
    - load_results: Combines multiple result files for analysis
    - agg_results: Aggregates and calculates performance metrics
    - calculate_acc_cost_index: Computes efficiency metrics considering accuracy and cost

Note: This module expects results to be stored in a 'results' directory and
requires specific data structures for model responses and evaluation metrics.
"""

# pylint: disable=C0301  # line-too-long
# pylint: disable=E0401  # import-error

import sys
import json
import os.path
import pandas as pd
import utils  as UTILS

def init_model_sheet():
    """
    Initialize an empty data structure to store model evaluation results.
    
    Returns:
        dict: Template structure for storing model results and metadata
    """
    model_sheet = {
        "model_desc": "",
        "execution_hash": "",
        "parameters": {},
        "results": {
            "input_id": [],
            "gabarito": [],
            "respostas": [],
            "respostas_raw": [],
            "input_tokens": [],
            "output_tokens": [],
            "total_tokens": [],
            "latency": [],
        }
    }

    return model_sheet

def check_result_if_exists(hashx, prefix, model):
    """
    Check if results for a specific model execution already exist.
    
    Args:
        hashx (str): Execution hash identifier
        prefix (str): Prefix for the results file
        model (str): Name of the model being evaluated
    """
    if os.path.isfile(f"results/{hashx}_{prefix}_{model}.json"):
        print(f"Modelo {model} já foi executado. Saindo...")
        sys.exit(0)

def save_results(hashx, prefix, model, res):
    """
    Save model evaluation results to a JSON file and print accuracy summary.
    
    Args:
        hashx (str): Execution hash identifier
        prefix (str): Prefix for the results file
        model (str): Name of the model being evaluated
        res (dict): Results to be saved
    """
    # Save model results to JSON file
    with open(f"results/{hashx}_{prefix}_{model}.json", "w", encoding="utf-8") as f:
        json.dump(res, f)
    acertos = sum([1 if res["results"]["respostas"][i] == res["results"]["gabarito"][i] else 0 for i in range(len(res["results"]["respostas"]))])
    print(f"Quantidade de acertos para o modelo {model} foi {acertos} de {len(res["results"]["respostas"])}")

def post_process_response(res, expected_min, expected_max, tag = "resposta"):
    """
    Clean and format model responses to extract relevant answer content.
    
    Args:
        res (str): Raw response from the model
        expected_min (int): Minimum expected length of the response
        expected_max (int): Maximum expected length of the response
        tag (str): XML-style tag to extract content from (default: "resposta")
        
    Returns:
        str: Processed and cleaned response
    """
    # Process and clean model's response
    res = res.replace("\n","").strip()
    lenx = len(res)
    if lenx >= expected_min and lenx <= expected_max  + 2:
        return res.replace("<","").replace(">","")
    else:
        return res.partition(f"<{tag}>")[2].partition(f"</{tag}>")[0].replace("\n","").replace(" ","").strip()

def load_results():
    """
    Load and combine all JSON result files into a single DataFrame.
    
    Returns:
        pandas.DataFrame: Combined results from all evaluation runs
    """
    all_results = pd.DataFrame()
    json_files = [pos_json for pos_json in os.listdir('results') if pos_json.endswith('.json')]

    for jf in json_files:
        with open('results/' + jf, 'r', encoding='utf-8') as f:
            origin = json.load(f)
            temp = pd.DataFrame(origin["results"])

            temp['model_id'] = f"{origin["model_desc"]}"
            temp['model_name'] = f"{origin["model_desc"]} - {origin["execution_hash"][0:5]}"
            all_results = pd.concat([all_results, temp], axis=0)

    all_results["correct"] = all_results.apply(lambda row: row["gabarito"] == row["respostas"], axis=1)

    return all_results

def calculate_margin_of_error(df, to_print = False):
    """
    Calculate error margin for each model based on response length validation.
    
    Args:
        df (pandas.DataFrame): DataFrame containing model results
        to_print (bool): Whether to print the error margins
        
    Returns:
        dict: Error margins for each model
    """
    error_margin = {}

    for row in df.itertuples():
        if (len(row.respostas) != 6 and len(row.respostas) != 8) and (len(row.respostas_raw.replace(" ","")) != 6 and len(row.respostas_raw.replace(" ","")) != 8):
            error_margin[f"{row.model_name}"] = error_margin.get(f"{row.model_name}", 0) + 1

    size = len(df[df["model_name"] == df["model_name"].unique().tolist()[0]])
    error_margin = {k: round(100*v/size, 2) for k, v in error_margin.items()}

    if to_print:
        print(f"Margin of error = {error_margin}")

    return error_margin

def agg_results(idf, bmm, error_margin, normalize_latency = False):
    """
    Aggregate results and calculate performance metrics for each model.
    
    Args:
        idf (pandas.DataFrame): Input DataFrame with raw results
        bmm: Benchmark metrics
        error_margin (dict): Error margins for each model
        normalize_latency (bool): Whether to normalize latency calculations
        
    Returns:
        pandas.DataFrame: Aggregated results with performance metrics
    """
    results = {}
    models = idf["model_name"].unique().tolist()

    for m in models:
        tmp = idf[idf["model_name"] == m].reset_index(drop=True)

        if len(tmp) == 0:
            continue

        uses_cot = "cot" in m
        m0 = tmp["model_id"][0]
        m0 = m0.replace("_", ".").replace(".zero.shot.cot","").replace(".zero.shot","").replace(".manual","")

        c0 = bmm[bmm["Model Id"] == m0].reset_index(drop=True)
        c0i = float(c0["Preço Input 1000"][0])
        c0o = float(c0["Preço Output 1000"][0])

        respostas = tmp["respostas"]
        gabarito = tmp["gabarito"]
        model_name = tmp["model_name"][0]
        acertos = sum([1 if respostas[i] == gabarito[i] else 0 for i in range(len(respostas))])

        results[m] = {
            "model_id": f"{m0.replace("us_","").replace("us.","").replace("anthropic_","").replace("amazon_","").replace("meta_","").replace("_zero_shot","")}",
            "model_name": model_name.replace("us_","").replace("anthropic_","").replace("amazon_","").replace("meta_","").replace("_zero_shot",""),
            "accuracy": 100 * acertos/len(respostas),
            "cost": c0i*1000 + c0o*1000, # USD per million Tokens
            "avg_latency": sum(tmp['latency']) / len(tmp['latency']) if not normalize_latency or uses_cot else sum(tmp[tmp['output_tokens'] < 20]["latency"]) / len(tmp[tmp['output_tokens'] < 20]["latency"]),
            "error": error_margin[m] if m in error_margin else 0.0,
            "error_minus": 0.0
        }

    d = pd.DataFrame(results).T
    d['accuracy'] = pd.to_numeric(d['accuracy'], errors='coerce')
    d['cost'] = pd.to_numeric(d['cost'], errors='coerce')
    d['avg_latency'] = pd.to_numeric(d['avg_latency'], errors='coerce')
    d["category"] = d.index.to_series().apply(UTILS.parse_category)

    return d

def calculate_acc_cost_index(df):
    """
    Calculate and sort efficiency index based on accuracy and cost.
    
    Args:
        df (pandas.DataFrame): DataFrame with model results
        
    Returns:
        pandas.DataFrame: DataFrame sorted by efficiency index
    """
    df['efficiency_index'] = df['accuracy'].apply(lambda x: x**5)/(10 ** 9)
    df['efficiency_index'] = df['efficiency_index'] / df['cost']
    df.sort_values(by='efficiency_index', ascending=False, inplace=True)

    return df
