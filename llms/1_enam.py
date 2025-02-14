# pylint: disable=C0301
# pylint: disable=C0413  # wrong-import-position
# pylint: disable=E0401  # import-error
# pyright: reportMissingImports=false

import sys
from pathlib import Path

sibling_dir = Path(__file__).parent / "base"
sys.path.append(str(sibling_dir))

from executor import BenchExecutor

class ENAM_Benchmark(BenchExecutor):
    def __init__(self):
        super().__init__()

    def get_data_from_source(self, ppath, lines = False):
        return super().get_data_from_source(ppath, self.nsample, lines)

    def pre_process(self, text):
        pass

    def check_result_if_exists(self, prefix):
        super().check_result_if_exists(self.hash_id, prefix, self.model_desc)

    def execute_tests(self, dataset, prefix):
        super().execute_tests(dataset, prefix)

    def process_row(self, row, prefix):
        utterance = row["enunciado"]
        alternativas = "\n".join(row["alternativas"])

        res, it, ot, tt, lt = self.call_bedrock(utterance, alternativas)

        self.model_sheet["results"]["prova_id"].append(prefix)
        self.model_sheet["results"]["input_id"].append(row["questao_id"])
        self.model_sheet["results"]["gabarito"].append(row["gabarito"])
        self.model_sheet["results"]["respostas"].append(self.post_process(res))
        self.model_sheet["results"]["respostas_raw"].append(res)
        self.model_sheet["results"]["input_tokens"].append(it)
        self.model_sheet["results"]["output_tokens"].append(ot)
        self.model_sheet["results"]["total_tokens"].append(tt)
        self.model_sheet["results"]["latency"].append(lt)

    def post_process(self, text):
        text = super().post_process(text)
        if len(text) == 3:
            return text.replace("(","").replace(")","")
        return text

    def save_results(self, prefix):
        super().save_results(self.hash_id, prefix, self.model_desc, self.model_sheet)

if __name__ == "__main__":
    b_enam = ENAM_Benchmark()
    print(f"Inciando a execução da análise do ENAM. Modelo = {b_enam.model}, CoT = {b_enam.use_cot}, N_Sampler = {b_enam.nsample}. Outros argumentos = {b_enam.args}")

    b_enam.check_result_if_exists("enam_2024")
    enam_dataset = b_enam.get_data_from_source("./0_ground_truth/enam_2024.json")

    b_enam.execute_tests(enam_dataset, "enam_2024")

    b_enam.save_results("enam_2024")
    print("FIM.")
