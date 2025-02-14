# pylint: disable=C0301
# pylint: disable=C0413  # wrong-import-position
# pylint: disable=E0401  # import-error
# pyright: reportMissingImports=false

import sys
import pandas as pd
from pathlib import Path

sibling_dir = Path(__file__).parent / "base"
sys.path.append(str(sibling_dir))

from executor import BenchExecutor

class OAB_Benchmark(BenchExecutor):
    def __init__(self):
        super().__init__()

    def get_data_from_source(self, ppath, lines = False):
        dataset = pd.read_parquet("hf://datasets/eduagarcia/oab_exams/data/train-00000-of-00001.parquet")

        if self.nsample < 1:
            return dataset.sample(frac=self.nsample, random_state=1)

        return dataset

    def pre_process(self, dataset):
        return dataset[dataset["exam_year"] == str(self.year)]

    def check_result_if_exists(self, prefix):
        super().check_result_if_exists(self.hash_id, prefix, self.model_desc)

    def execute_tests(self, dataset, prefix):
        super().execute_tests(dataset, prefix)

    def process_row(self, row, prefix):
        iu = None
        utterance = row["question"]
        alternativas = "\n".join([f"{row['choices']['label'][idx]}) {row['choices']['text'][idx]}" for idx in range(0, 4)])

        if "IU" in row and row['IU']:
            iu = row['description'][0]

        res, it, ot, tt, lt = self.call_bedrock(utterance, alternativas, iu)

        self.model_sheet["results"]["prova_id"].append(row["exam_id"])
        self.model_sheet["results"]["input_id"].append(row["id"])
        self.model_sheet["results"]["gabarito"].append(row["answerKey"])
        self.model_sheet["results"]["respostas"].append(self.post_process(res))
        self.model_sheet["results"]["respostas_raw"].append(res)
        self.model_sheet["results"]["input_tokens"].append(it)
        self.model_sheet["results"]["output_tokens"].append(ot)
        self.model_sheet["results"]["total_tokens"].append(tt)
        self.model_sheet["results"]["latency"].append(lt)

    def post_process(self, text):
        return super().post_process(text)

    def save_results(self, prefix):
        super().save_results(self.hash_id, prefix, self.model_desc, self.model_sheet)

if __name__ == "__main__":
    b_oab = OAB_Benchmark()
    print(f"Inciando a execução da análise da OAB. Modelo = {b_oab.model}, CoT = {b_oab.use_cot}, N_Sampler = {b_oab.nsample}. Outros argumentos = {b_oab.args}")

    b_oab.check_result_if_exists(f"oab_{b_oab.year}")
    oab_dataset = b_oab.get_data_from_source(f"hf://datasets/maritaca-ai/enem/{b_oab.year}.jsonl", True)
    oab_dataset = b_oab.pre_process(oab_dataset)

    b_oab.execute_tests(oab_dataset, f"oab_{b_oab.year}")

    b_oab.save_results(f"oab_{b_oab.year}")
    print("FIM.")
