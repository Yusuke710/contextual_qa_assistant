
import os
from datetime import date
import tempfile
import yaml

from flask import Flask, request, render_template, jsonify, flash, redirect

from utils.chatbot import chatbot_gptindex
from utils.speech2text import speech2text_whisper


# read parameters from yaml
with open(r'config.yaml') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

# set your openai api
os.environ["OPENAI_API_KEY"] = config["OPENAI_API_KEY"]

# index file
index_file = config["index_file"]
# whisper model size
whisper_model = config["whisper_model"]
# llm model 
llm_model = config["llm_model"]
# embedding model 
embed_model = config["embed_model"]
# max_input_size
max_input_size = config["max_input_size"]
# num_output
num_output = config["num_output"]
# text chunk
chunk_size_limit = config["chunk_size_limit"]
# overlap
max_chunk_overlap = config["max_chunk_overlap"]
# top_k search
similarity_top_k = config["similarity_top_k"]



# class initialisation
# this class loads context and respond to query
chatbot = chatbot_gptindex(index_file, llm_model, embed_model, max_input_size, num_output, chunk_size_limit, max_chunk_overlap, similarity_top_k)        
# This class loads whisper as speech2text model and takes audio recording and output a text
audiobot = speech2text_whisper(whisper_model)

# flask handles html page setup and handles user input 
app = Flask(__name__)

@app.route("/")
def user_prompt():
    return render_template("chatbot.html")

# chatbot handles user_input
@app.route("/response", methods=["POST"])
def handle_response():
    # Get the text from the request
    data = request.get_json()
    user_input = data["text"]

    # process the user's input and generate a response
    response = chatbot.query(user_input)
    
    print(user_input)
    print(response)

    # log user input and chatbot's response for future improvement 
    file_path = "chatlog"
    filename = date.today()
    if not os.path.exists(file_path):
        # if the directory is not present then create it.
        os.makedirs(file_path)
    with open(os.path.join(file_path, str(filename) + ".txt"), "a+") as f:
        f.write("Q: " + user_input)
        f.write(str(response))
        f.write("\n")

    return jsonify(response=str(response))

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
    return text

if __name__ == "__main__":
    app.run()

