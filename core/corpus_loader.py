import os, json


class CorpusLoader:
    """
    Esta clase se encarga de obtener todos los datos de entrenamiento del corpus.
    Los archivos .txt contienen las muestras de conversacion a aprender y los .json
    contienen estructuras, respuestas constantes, patrones, etc...
    """

    def get_files_path(self, corpus_name="") -> list:
        corpus_files_path = []
        json_files_path = []

        corpus_path = os.path.join(self.main_path, f"assets/corpus/{corpus_name}")
        for root_path, dict_path, file_list in os.walk(corpus_path):
            for file_name in file_list:
                file_path = os.path.join(root_path, file_name)

                if ".txt" in file_name:
                    corpus_files_path.append(file_path)

                elif ".json" in file_name:
                    json_files_path.append([file_path, file_name[:-5]])

        return corpus_files_path, json_files_path

    def load_corpus(self, corpus_name: str):
        path_list = self.get_files_path(corpus_name)

        corpus_samples = []
        for file_path in path_list[0]:
            with open(file_path, "r", encoding="utf-8") as textfile:
                corpus_samples.extend(textfile.readlines() + [""])

        # Guarda la informacion de los archivos .json en json_dict
        for file_path, file_name in path_list[1]:
            with open(file_path, "r", encoding="utf-8") as jsonfile:
                self.json_dict[file_name] = json.load(jsonfile)

        return corpus_samples
