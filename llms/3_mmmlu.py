# pylint: disable=C0301
# pylint: disable=C0413  # wrong-import-position
# pylint: disable=E0401  # import-error
# pyright: reportMissingImports=false

import sys
import hashlib
import pandas as pd
from pathlib import Path

sibling_dir = Path(__file__).parent / "base"
sys.path.append(str(sibling_dir))

from datasets import load_dataset
from executor import BenchExecutor

class ENEM_Benchmark(BenchExecutor):
    def __init__(self):
        super().__init__()

    def get_data_from_source(self, ppath, lines = False):
        df  = load_dataset(ppath, "PT_BR", split="test")
        df = pd.DataFrame(df)
        df = df.sample(frac=0.01, random_state=1)
        return df

    def pre_process(self, dataset):
        dataset.drop(columns=["Unnamed: 0"], inplace=True)
        dataset.reset_index(drop=True, inplace=True)

        dataset['hash'] = dataset["Question"].apply(lambda x: hashlib.md5(x.encode("utf-8")).hexdigest())
        dataset['alternativas'] = dataset.apply(lambda row: "\n".join([f"A) {row['A']}", f"B) {row['B']}", f"C) {row['C']}", f"D) {row['D']}"]), axis=1)

        if self.nsample < 1.0:
            dataset = dataset.sample(frac=self.nsample, random_state=1)
        return dataset

    def check_result_if_exists(self, prefix):
        super().check_result_if_exists(self.hash_id, prefix, self.model_desc)

    def execute_tests(self, dataset, prefix):
        super().execute_tests(dataset, prefix)

    def process_row(self, row, prefix):
        iu = None
        utterance = row["Question"]
        alternativas = row["alternativas"]

        if "IU" in row and row['IU']:
            iu = row['description'][0]

        res, it, ot, tt, lt = self.call_bedrock(utterance, alternativas, iu)

        self.model_sheet["results"]["prova_id"].append(prefix)
        self.model_sheet["results"]["input_id"].append(row["hash"])
        self.model_sheet["results"]["gabarito"].append(row["Answer"])
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
    b_mmmlu = ENEM_Benchmark()
    print(f"Inciando a execução da análise do MMMLU. Modelo = {b_mmmlu.model}, CoT = {b_mmmlu.use_cot}, N_Sampler = {b_mmmlu.nsample}. Outros argumentos = {b_mmmlu.args}")

    b_mmmlu.check_result_if_exists("mmmlu")
    mmmlu_dataset = b_mmmlu.get_data_from_source("openai/MMMLU", False)
    mmmlu_dataset = b_mmmlu.pre_process(mmmlu_dataset)

    b_mmmlu.execute_tests(mmmlu_dataset, "mmmlu")

    b_mmmlu.save_results("mmmlu")
    print("FIM.")
