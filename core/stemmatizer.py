import json, unicodedata, math


class Stemmatizer:
    """Esta clase permite separar las palabras en su raiz y subfijo"""

    memory = {}

    @staticmethod
    def format(text: str) -> str:
        normalize_text = unicodedata.normalize("NFD", text.lower())
        encoded_text = normalize_text.encode("ascii", "ignore")
        return encoded_text.decode("utf-8")

    def train(self, word_list: list) -> None:
        for word in word_list:
            word = self.format(word)
            for i in range(len(word) - 1):
                part = word[i : i + 2]

                if not part in self.memory:
                    self.memory[part] = 1
                else:
                    self.memory[part] += 1

    def save_model(self, path: str) -> None:
        with open(path, "w") as jsonfile:
            json.dump(self.memory, jsonfile)

    def load_model(self, path: str) -> None:
        with open(path, "r") as jsonfile:
            self.memory = json.load(jsonfile)

    def predict(self, word: str, bias=0.1) -> str:
        prob_total = 0
        root = ""

        word = self.format(word)
        for i in range(len(word) - 1):
            part = word[i : i + 2]
            if not part in self.memory:
                break
            proba = math.log(self.memory[part] / len(word))

            if prob_total == 0:
                prob_total = proba
                root += part

                continue

            elif proba / prob_total > bias:

                prob_total += proba
                root += part

            else:
                break

        if root:
            root_lenght = len(root) // 2
            root = "".join([root[i * 2] for i in range(root_lenght)]) + root[-1]

        return root

    def get_stemma(self, word: str, bias=0.35) -> tuple:
        word_root = self.predict(word, bias)
        word_subfix = word.lower().replace(word_root, "")

        if word_root == word_subfix:
            word_subfix = ""

        return (word_root, word_subfix)
