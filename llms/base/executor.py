# pylint: disable=C0301

from abc import ABC, abstractmethod
import time
import hashlib
import pandas as pd
from tqdm import tqdm

import utils as UTILS
import bedrock as BROCK
import eval_br as EVALRES

class BenchExecutor(ABC):
    @abstractmethod
    def __init__(self):
        super().__init__()
        _model, _use_cot, _nsample, _config_file, _args = UTILS.argument_parser()

        self.model = _model
        self.use_cot = _use_cot
        self.nsample = _nsample
        self.config_file = _config_file
        self.args = _args
        self.year = _args["year"] if "year" in _args else ""
        self.hash_id = hashlib.md5(f"{self.model}_{self.use_cot}_{self.nsample}_{self.config_file}_{self.args}".encode("utf-8")).hexdigest()

        _model_id, _model_desc = BROCK.parse_model_name(self.model, self.use_cot)

        self.model_id = _model_id
        self.model_desc = _model_desc

        self.model_sheet = EVALRES.init_model_sheet()
        self.model_sheet["model_desc"] = self.model_desc
        self.model_sheet["execution_hash"] = self.hash_id
        self.model_sheet["parameters"] = self.args
        self.model_sheet["results"]["prova_id"] = [] # CUSTOM

        self.sleeptime = BROCK.get_model_delay(self.model_id)
        self.configs = UTILS.load_yaml(self.config_file)
        self._system_list = BROCK.set_system_prompt(self.configs['system_prompts'])

    @abstractmethod
    def get_data_from_source(self, path, sample_size = 1.0, p_lines = False):
        dataset = pd.read_json(path, lines = p_lines)

        if sample_size < 1:
            return dataset.sample(frac=sample_size, random_state=1)
        return dataset

    @abstractmethod
    def pre_process(self, text):
        pass

    @abstractmethod
    def check_result_if_exists(self, hash_id, prefix, model):
        EVALRES.check_result_if_exists(hash_id, prefix, model)

    @abstractmethod
    def execute_tests(self, dataset, prefix):
        with tqdm(total=len(dataset), desc=f"Model = {self.model_desc}") as pbar:
            for ix, linha in dataset.iterrows():
                while True:
                    time.sleep(self.sleeptime)
                    try:
                        self.process_row(linha, prefix)
                    except Exception as e:
                        print(f"Sleep = {self.sleeptime}.\nException = {e}")
                        self.sleeptime = self.sleeptime + 1
                        continue
                    break
                pbar.update(1)

    def call_bedrock(self, utterance, alternativas, iu = None):
        prompt = BROCK.set_prompt(
            self.configs["prompt_template"],
            utterance,
            self.configs["zero_shot_footer"],
            self.configs["chain_of_thought_footer"],
            self.use_cot,
            alternativas
        )

        if iu:
            prompt = prompt.replace('[[placeholder]]', iu)

        # Get model's response and metrics
        return BROCK.call_model(self.model_id, prompt, self._system_list, 0.0, self.configs['max_tokens'])

    @abstractmethod
    def process_row(self, row, prefix):
        pass

    @abstractmethod
    def post_process(self, text):
        return EVALRES.post_process_response(text, self.configs["min"], self.configs["max"]) if len(text) > 0 else ""

    @abstractmethod
    def save_results(self, hash_id, prefix, model, sheet):
        EVALRES.save_results(hash_id, prefix, model, sheet)
