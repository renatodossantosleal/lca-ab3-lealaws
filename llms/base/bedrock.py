# pylint: disable=C0301

import boto3
import pandas as pd

# Initialize Bedrock client for AWS region us-east-1
client = boto3.client("bedrock-runtime", region_name="us-east-1")

def get_bedrock_metadata():
    return pd.read_csv("./_metadados/bedrock_models.csv", sep=";")

def get_model_delay(model):
    _bmm = get_bedrock_metadata()
    return _bmm[_bmm["Model Id"] == model].reset_index()["Delay"][0]

def set_system_prompt(text = ""):
    if text == "":
        return []
    text = text.replace("\n", " ")
    return [{ "text": text}]

def parse_model_name(model, use_cot = False):
    model_id = model
    model_desc = model.replace(".","_")
    model_desc = model_desc + "_zero_shot" if use_cot is None or use_cot is False else model_desc + "_zero_shot_cot"

    return model_id, model_desc

def set_prompt(template, utter, footer_zs, footer_cot = "", use_cot = False, alternatives = ""):
    if "{footer}" in template:
        footer = footer_zs if use_cot is None or use_cot is False else footer_cot
        template = template.replace("{footer}", footer)
    elif len(footer_zs) > 0 or len(footer_cot) > 0:
        footer = footer_zs if use_cot is None or use_cot is False else footer_cot
        template = template + "\n" + footer
    if "{utterance}" in template:
        template = template.replace("{utterance}", utter)
    if "{alternatives}" in template:
        template = template.replace("{alternatives}", alternatives)

    return template

def call_model(modelid, message, system_list = [], temp = 0.0, mt = 22):
    message_list = [{"role": "user", "content": [{"text": message}]}]
    inference_config = {"temperature": temp,  "maxTokens": mt,}

    if len(message) > 20000:
        print("Mensagem muito grande...")
        exit(0)

    response = client.converse(
        modelId=modelid,
        messages=message_list,
        system=system_list,
        inferenceConfig=inference_config,
    )

    token_usage = response['usage']
    latency = response['metrics']['latencyMs']
    msg = response['output']['message']["content"][0]["text"] if len(response['output']['message']["content"]) > 0 else ""

    return msg, token_usage['inputTokens'], token_usage['outputTokens'], token_usage['totalTokens'], latency
