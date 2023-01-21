# code based from https://github.com/jerryjliu/gpt_index

from gpt_index import GPTSimpleVectorIndex, SimpleDirectoryReader
from gpt_index.indices.prompt_helper import PromptHelper
import os

from flask import Flask, request, render_template

# this class loads context and respond to query
class chatbot():
    def __init__(self):
        # skip embedding if index exists already
        self.index_file = 'data/index.json'
        if os.path.exists(self.index_file):
            # load from disk 
            print('loading context from a disk')
            self.index = GPTSimpleVectorIndex.load_from_disk(self.index_file)
        else:
            # read the data and embed into index
            self.documents = SimpleDirectoryReader('data').load_data()
            self.index = GPTSimpleVectorIndex(
                documents = self.documents,
                #embed_model=embed_model,  # embedding model to use 
                prompt_helper=PromptHelper(
                    max_input_size=3500,  # LLM max input token length
                    num_output=500,  # LLM output token length
                    chunk_size_limit=500,  # number of tokens per embedding
                    max_chunk_overlap=30
                    ),
                verbose=True
                )
            # save to disk
            self.index.save_to_disk(self.index_file)
    
    def query(self, user_input):
        return self.index.query(user_input, verbose=True)

bot = chatbot()        

# flask handles html page setup and handles user input as well as sending response from the chatbot
app = Flask(__name__)

@app.route("/")
def user_prompt():
    return render_template("chatbot_static.html")

@app.route("/response", methods=["POST"])
def handle_response():
    user_input = request.form["user_input"]
    # process the user's input and generate a response
    response = bot.query(user_input)
    return render_template("chatbot_static.html", user_input=user_input, response=str(response))

if __name__ == "__main__":
    app.run()
