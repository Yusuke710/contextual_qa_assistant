import whisper

# Based on github repo: https://github.com/amrrs/openai-whisper-webapp
class speech2text_whisper:
    def __init__(self, model_size):
        print(f"loading {model_size}")
        self.model = whisper.load_model(model_size)

    def transcribe(self, audio_file):
    # load audio and pad/trim it to fit 30 seconds
        self.audio = whisper.load_audio(audio_file)
        self.audio = whisper.pad_or_trim(self.audio)

        # make log-Mel spectrogram and move to the same device as the model
        self.mel = whisper.log_mel_spectrogram(self.audio).to(self.model.device)

        # decode the audio
        self.options = whisper.DecodingOptions(fp16 = False)
        self.result = whisper.decode(self.model, self.mel, self.options)
        return self.result.text