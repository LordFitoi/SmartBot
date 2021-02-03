import re , random, string

# Modelo usando cadenas de Markov
class MarkovModel: 
    memory = {}
    
    def format(self, text : str) -> str:
        text = re.sub("\W", " ", text.lower())
        text = re.sub(",", " ,", text)
        text = re.sub("\s+", " ", text)
        
        return "START "+re.sub("\n+", "", text)+" END"
        
    def train(self, sent_list : list) -> None:
        for sentence in sent_list:
            word_list = self.format(sentence).split()
            for i in range(len(word_list) - 1):
                token = word_list[i]
                if token not in self.memory:
                    self.memory[token] = {}
                
                next_token = word_list[i+1]
                if next_token not in self.memory[token]:
                    self.memory[token][next_token] = 1
                else: 
                    if next_token == "END":
                        self.memory[token][next_token] += 2
                    else: self.memory[token][next_token] += 1

    def __call__(self, initial_token = "", text_lenght = 20) -> str:
        if self.memory:
            word_list = ["START"]
            if initial_token: word_list.append(initial_token)
            current_token = word_list[-1]
            for _ in range(text_lenght):
                if current_token not in self.memory:
                    current_token = random.choice(list(self.memory.keys()))

                max_freq = sum(self.memory[current_token].values())

                for word, value in self.memory[current_token].items():
                    if random.randrange(0, max_freq + 1) <= value:
                        
                        word_list.append(word); break
                    else: max_freq -= value
                
                if word_list[-1] == "END": break
                current_token = word_list[-1]
            generated_text = " ".join(word_list[1 :len(word_list) - 1]).capitalize()
            return generated_text
        else: return ""

# Modelo usando cadenas de Markov con contexto
class ContextMarkovModel: 
    memory = {}
    punctuation = string.punctuation[:22] + "¡¿"
    def format(self, text : str, clean_punct = False) -> None:
        if not clean_punct:
            for symbol in self.punctuation:
                text = re.sub(f"[{symbol}]", f" {symbol} ", text.lower())
        else:
            text = re.sub("\W", " ", text.lower())
        text = re.sub(",", " ,", text)
        text = re.sub("\s+", " ", text)

        return "START "+re.sub("\n+", "", text)+" END"
        

    def train(self, sent_list : list) -> None:
        for i in range(len(sent_list) - 1):
            if not sent_list[i+1] or not sent_list[i]: continue
            
            wordA_list = self.format(sent_list[i+1]).split()
            wordB_list = self.format(sent_list[i], True).split()[1:-1]

            for i in range(len(wordA_list) - 1):
                if i >= len(wordB_list): x_input = ""
                else: x_input =  wordB_list[i]

                token = (wordA_list[i], x_input)
                if token not in self.memory:
                    self.memory[token] = {}
                
                next_token = wordA_list[i+1]
                if next_token not in self.memory[token]:
                    self.memory[token][next_token] = 1
                else: self.memory[token][next_token] += 1

    def __call__(self, context : str, text_lenght = 20) -> str:
        if self.memory:
            context = self.format(context, True).split()[1:-1]
            word_list = [("START", context[0])]

            current_token = word_list[-1]
            for _ in range(text_lenght):
                if current_token not in self.memory:
                    if current_token[1]:
                        candidates = [
                            item for item in self.memory
                            if item[1] == current_token[1]
                        ]

                    else:
                        candidates = [
                            item for item in self.memory
                            if item[0] == current_token[0]
                        ]
                    if not candidates: candidates = list(self.memory.keys())
                    current_token = random.choice(candidates)

    
                max_freq = sum(self.memory[current_token].values())

                for word, value in self.memory[current_token].items():
                    if random.randrange(0, max_freq + 1) <= value:
                        index = len(word_list)
                        if index >= len(context): x_input = ""
                        else: x_input = context[index]

                        word_list.append((word, x_input)); break
                    else: max_freq -= value
                
                if word_list[-1][0] == "END": break
                current_token = word_list[-1]
            
            sentence_word = [item[0] for item in word_list[1 :len(word_list) - 1]]
            generated_text = " ".join(sentence_word).capitalize()
            return generated_text
        else: return ""
