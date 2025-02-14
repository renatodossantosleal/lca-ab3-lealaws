# pylint: disable=C0301
# pylint: disable=C0413  # wrong-import-position
# pylint: disable=E0401  # import-error
# pyright: reportMissingImports=false

import sys
from pathlib import Path

sibling_dir = Path(__file__).parent / "base"
sys.path.append(str(sibling_dir))

from executor import BenchExecutor

class ENEM_Benchmark(BenchExecutor):
    def __init__(self):
        super().__init__()

    def get_data_from_source(self, ppath, lines = False):
        return super().get_data_from_source(ppath, self.nsample, lines)

    def pre_process(self, dataset):
        return dataset[dataset["label"] != 'Anulado']

    def check_result_if_exists(self, prefix):
        super().check_result_if_exists(self.hash_id, prefix, self.model_desc)

    def execute_tests(self, dataset, prefix):
        super().execute_tests(dataset, prefix)

    def process_row(self, row, prefix):
        iu = None
        utterance = row["question"]
        choices = {0: "A", 1: "B", 2: "C", 3: "D", 4: "E"}

        alternativas = "\n".join([f"{choices[idx]}) {list(row["alternatives"])[idx]}" for idx in range(0, 5)])

        if row['IU']:
            iu = row['description'][0]

        res, it, ot, tt, lt = self.call_bedrock(utterance, alternativas, iu)

        self.model_sheet["results"]["prova_id"].append(row["exam"])
        self.model_sheet["results"]["input_id"].append(row["id"])
        self.model_sheet["results"]["gabarito"].append(row["label"])
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
    b_enem = ENEM_Benchmark()
    print(f"Inciando a execução da análise do ENEM. Modelo = {b_enem.model}, CoT = {b_enem.use_cot}, N_Sampler = {b_enem.nsample}. Outros argumentos = {b_enem.args}")

    b_enem.check_result_if_exists(f"enem_{b_enem.year}")
    enem_dataset = b_enem.get_data_from_source(f"hf://datasets/maritaca-ai/enem/{b_enem.year}.jsonl", True)
    enem_dataset = b_enem.pre_process(enem_dataset)

    b_enem.execute_tests(enem_dataset, f"enem_{b_enem.year}")

    b_enem.save_results(f"enem_{b_enem.year}")
    print("FIM.")
