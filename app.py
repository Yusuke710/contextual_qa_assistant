from gpt_index import GPTSimpleVectorIndex, SimpleDirectoryReader
from gpt_index.indices.prompt_helper import PromptHelper
import os
from datetime import date

import whisper
import tempfile

from flask import Flask, request, render_template, jsonify, flash, redirect

# this class loads context and respond to query
# code based from https://github.com/jerryjliu/gpt_index
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
                    chunk_size_limit=1000,  # number of tokens per embedding
                    max_chunk_overlap=50
                    ),
                verbose=True
                )
            # save to disk
            self.index.save_to_disk(self.index_file)
    
    def query(self, user_input):
        return self.index.query(user_input, similarity_top_k = 2, verbose=True)

# This class loads whisper as speech2text model and takes audio recording and output a text
# Based on github repo: https://github.com/amrrs/openai-whisper-webapp

class speech2text():
    def __init__(self):
        self.model = whisper.load_model("small")

    def transcribe(self, audio_file):
    #time.sleep(3)
    # load audio and pad/trim it to fit 30 seconds
        self.audio = whisper.load_audio(audio_file)
        self.audio = whisper.pad_or_trim(self.audio)

        # make log-Mel spectrogram and move to the same device as the model
        self.mel = whisper.log_mel_spectrogram(self.audio).to(self.model.device)

        # detect the spoken language
        #_, probs = self.model.detect_language(mel)
        #print(f"Detected language: {max(probs, key=probs.get)}")

        # decode the audio
        self.options = whisper.DecodingOptions(fp16 = False)
        self.result = whisper.decode(self.model, self.mel, self.options)
        return self.result.text



bot = chatbot()        
audiobot = speech2text()

# flask handles html page setup and handles user input as well as sending response from the chatbot
app = Flask(__name__)

@app.route("/")
def user_prompt():
    return render_template("chatbot.html")

# chatbot handles user_input
@app.route("/response", methods=["POST"])
def handle_response():
    # Get the text from the request
    user_input = request.form["user_input"]

    # process the user's input and generate a response
    response = bot.query(user_input)
    #response = 'test test test'
    print(user_input)
    print(response)

    # log user input and chatbot's response for future improvement 
    file_path = "chatlog"
    filename = date.today()
    with open(os.path.join(file_path, str(filename) + '.txt'), "a+") as f:
        f.write(user_input)
        f.write(str(response))
        f.write("\n")

    return render_template("chatbot.html", user_input=user_input, response=str(response))

# audio process, output of this goes to input column of html to replace placeholder="Enter your message here"
@app.route("/audio", methods=["POST"])
def handle_audio():
    # Get the audio file from the request
    # check if the post request has the file part
    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)
    audio_file = request.files["file"]

    # Save the audio file to disk
    temp_dir = tempfile.mkdtemp()
    save_path = os.path.join(temp_dir, "temp.wav")
    audio_file.save(save_path)

    # Process the audio file to apply the whisper effect
    
    text = audiobot.transcribe(save_path)
    print(f"speech2text output: {text}")

    # Return the text as a response
    #return jsonify(text=text)
    return text

if __name__ == "__main__":
    app.run()

