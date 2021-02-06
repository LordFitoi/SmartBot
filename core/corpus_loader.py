import os, json


class CorpusLoader:
    def get_files_path(self, corpus_name="") -> list:
        corpus_files_path = []
        structure_files_path = []

        corpus_path = os.path.join(self.main_path, f"assets/corpus/{corpus_name}")
        for root_path, dict_path, file_list in os.walk(corpus_path):
            for file_name in file_list:
                file_path = os.path.join(root_path, file_name)

                if ".txt" in file_name:
                    corpus_files_path.append(file_path)

                elif ".json" in file_name:
                    structure_files_path.append([file_path, file_name[:-5]])

        return corpus_files_path, structure_files_path

    def load_corpus(self, corpus_name: str):
        corpus_files_path, structure_files_path = self.get_files_path(corpus_name)

        corpus_samples = []
        for file_path in corpus_files_path:
            with open(file_path, "r", encoding="utf-8") as textfile:
                corpus_samples.extend(textfile.readlines() + [""])

        for file_path, file_name in structure_files_path:
            with open(file_path, "r", encoding="utf-8") as jsonfile:
                self.structure_dict[file_name] = json.load(jsonfile)

        return corpus_samples
