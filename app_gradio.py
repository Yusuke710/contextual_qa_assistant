from gpt_index import GPTSimpleVectorIndex, SimpleDirectoryReader
from gpt_index.indices.prompt_helper import PromptHelper
import os
from datetime import date

import whisper

import gradio as gr

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



chat_bot = chatbot()        
audio_bot = speech2text()

# function of gradio interface. 
def integrated_bot(audio):
    # whisper for speech2text
    # gpt-3 for chatbot
    texts = audio_bot.transcribe(audio)
    print(f"speech2text result: {texts}")
    response = chat_bot.query(texts)
    return str(response)

gr.Interface(
    title = "DeepNeuron Chatbot", 
    fn=integrated_bot, 
    inputs=[
        gr.inputs.Audio(source="microphone", type="filepath")
    ],
    outputs=[
        "textbox"
    ],
    live=True).launch()
