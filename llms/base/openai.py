import os
import pandas as pd
from openai import OpenAI

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def get_openai_metadata():
    temp = {
        'Provedor': '',
        'Nome do Modelo': '',
        'Model Id': '',
        'Preço Input 1000': '',
        'Preço Output 1000': '',
        'Delay': '',
    }

    df = pd.DataFrame([temp])

    return df

def get_model_delay(model):
    _omm = get_openai_metadata()
    return _omm[_omm["Model Id"] == model].reset_index()["Delay"][0]

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
    message_list = [{"role": "user", "content": message}]
    if len(system_list) > 0:
        message_list = [{"role": "system", "content": system_list[0]["text"]}] + message_list

    if len(message) > 20000:
        print("Mensagem muito grande...")
        exit(0)

    response = client.chat.completions.create(
        model=modelid,
        messages=message_list,
        temperature=temp,
        max_tokens=mt,
    )

    # response.choices[0].message.content

    token_usage = response['usage']
    latency = response['metrics']['latencyMs']
    msg = response['output']['message']["content"][0]["text"] if len(response['output']['message']["content"]) > 0 else ""

    return msg, token_usage['inputTokens'], token_usage['outputTokens'], token_usage['totalTokens'], latency
