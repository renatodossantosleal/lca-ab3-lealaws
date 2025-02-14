# pylint: disable=C0301
"""
This module provides utility functions for the benchmark system.
It includes functions for parsing command line arguments, loading YAML files,
and parsing provider names from strings.
"""

import argparse
import yaml

def argument_parser():
    """
    Parse and process command line arguments for the benchmark system.
    
    Returns:
        tuple: Contains the following elements:
            - model (str): Name of the model to be evaluated
            - use_cot (bool): Whether to use Chain of Thought reasoning
            - nsample (float): Number of samples to process
            - config_file (str): Path to configuration file
            - args (dict): All parsed command line arguments
    """

    ap = argparse.ArgumentParser()
    ap.add_argument("-m", "--model",        required=True,  help="Modelo a ser avaliado")
    ap.add_argument("-c", "--cot",          required=False, help="Utiliza CoT (chain of thought)")
    ap.add_argument("-n", "--nsample",      required=False, help="Número de amostras")
    ap.add_argument("-y", "--year",         required=False, help="Ano da prova")
    ap.add_argument("-f", "--config-file",  required=False, help="Arquivo de Configuração", default="configs.yaml")
    ap.add_argument("-r", "--router",       required=False, help="Arquivo de Configurações do Roteador")
    args = vars(ap.parse_args())

    model  = args["model"]
    use_cot = True if args["cot"] is not None and args["cot"].lower() == "true" else False
    nsample = float(args["nsample"]) if args["nsample"] is not None else 1.0
    config_file = args["config_file"]

    return model, use_cot, nsample, config_file, args

def load_yaml(file_path):
    """
    Load and parse a YAML configuration file.
    
    Args:
        file_path (str): Path to the YAML file to be loaded
        
    Returns:
        dict: Parsed YAML data
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
    return data

def parse_provider(model_name):
    """
    Determine the AI provider based on the model name.
    
    Args:
        model_name (str): Name of the model
        
    Returns:
        str: Name of the provider (amazon, anthropic, meta, openai, or maritaca ai)
    """
    if "nova" in model_name.lower():
        return "amazon"
    elif "haiku" in model_name.lower() or "sonnet" in model_name.lower():
        return "anthropic"
    elif "llama" in model_name.lower():
        return "meta"
    elif "gpt" in model_name.lower():
        return "openai"
    else:
        return "maritaca ai"
