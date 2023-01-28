from gpt_index import GPTSimpleVectorIndex, SimpleDirectoryReader, LLMPredictor
from gpt_index.indices.prompt_helper import PromptHelper
from langchain import OpenAI
from langchain.embeddings import OpenAIEmbeddings

import os

# code based from https://github.com/jerryjliu/gpt_index
class chatbot_gptindex:
    def __init__(self, index_file, llm_model, embed_model, max_input_size, num_output, chunk_size_limit, max_chunk_overlap, similarity_top_k):
        self.index_file = index_file
        # define embedding model
        # https://note.com/npaka/n/nee11eb7e620e
        #self.embed_model = OpenAIEmbeddings(model_name = embed_model) 
        # define LLM
        self.llm_predictor = LLMPredictor(llm=OpenAI(temperature=0, model_name=llm_model))
        # define prompt helper
        self.prompt_helper=PromptHelper(
                    max_input_size=max_input_size,  # LLM max input token length
                    num_output=num_output,  # LLM output token length
                    chunk_size_limit=chunk_size_limit,  # number of tokens per embedding
                    max_chunk_overlap=max_chunk_overlap
                    )
        # query settings
        self.similarity_top_k = similarity_top_k

        # skip embedding if index exists already
        if os.path.exists(self.index_file):
            # load from disk 
            print(f"loading context from {self.index_file}")
            self.index = GPTSimpleVectorIndex.load_from_disk(self.index_file, 
                llm_predictor = self.llm_predictor, 
                #embed_model = self.embed_model, 
                prompt_helper = self.prompt_helper)
        else:
            # read the data and embed into index
            self.documents = SimpleDirectoryReader("data").load_data()
            self.index = GPTSimpleVectorIndex(
                documents = self.documents,
                #embed_model = self.embed_model, 
                llm_predictor = self.llm_predictor,
                prompt_helper = self.prompt_helper,
                verbose = True
                )
            # save to disk
            self.index.save_to_disk(self.index_file)
    
    def query(self, user_input):
        return self.index.query(user_input, similarity_top_k = self.similarity_top_k, verbose=True)

'''
# test
user_input = "What is DeepNeuron?"
bot = chatbot_gptindex("data/index.json", "text-davinci-003", "text-embedding-ada-002", 3000, 200, 500, 0, 2)
response = bot.query(user_input)
print(response)
'''