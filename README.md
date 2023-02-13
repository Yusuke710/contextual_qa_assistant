# overview 
This chatbot, inspired by ChatGPT, leverages the advanced language understanding capabilities of a Large Language Model (LLM) and embedding techniques to extract relevant context from a data-embedded text database, enabling it to respond to user prompts in a coherent and accurate manner. The chatbot employs the [OpenAI GPT-3](https://openai.com/api/) API and [GPT Index](https://github.com/jerryjliu/gpt_index) to achieve this functionality, which has been exemplified by its use in Monash DeepNeuron's showcase where it acts as a customer service representative, providing information on DeepNeuron's projects and activities. The chatbot utilizes data extracted from the [Monash DeepNeuron website](https://www.deepneuron.org/) as a source of context for its responses. Furthermore, the chatbot accepts audio input as an user input to enhance the user experience of it.

## commands to run 
- Put your data files into the directory `data` for chatbot to read as well as your OpenAI API key.
- `pip install -r requirements.txt`
You can get API key from [OpenAI](https://beta.openai.com/account/api-keys)
- `python app.py`
- As the terminal instructs, browse to http://127.0.0.1:5000 

## Example of the chatbot compared to ChatGPT: The chatbot is able to answer about Monash DeepNeuron correctly
![ChatGPT_example](/assets/ChatGPT_example.png)
![chatbot_example](/assets/my_example.png)_

## TODO
- local GPT-2
- use cuntom embedding model


- record conversation in a better format
- reduce the amount of times it refine response, too much loading time and money!!
https://github.com/jerryjliu/gpt_index/blob/becde98138295aa20d8664d5c26ec4cba433b814/gpt_index/indices/response/builder.py
add 2 breaks to only get initial response. Refinement of response diverges from optimal answer
read from text_chunks instead of text_chunk
- typing feature similar to chatGPT, in this way user is easy to keep track of the output generated
- add source of information, break up chunks using LLM
- deploy it on AWS instance and access it using ssh
- People scan QR code and it leads to the website. Use this https://www.qr-code-generator.com/solutions/static-url-qr-code/ 