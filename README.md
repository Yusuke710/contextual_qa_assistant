# overview 
This chatbot, inspired by ChatGPT, leverages the advanced language understanding capabilities of a Large Language Model (LLM) and embedding techniques to extract relevant context from a data-embedded text database, enabling it to respond to user prompts in a coherent and accurate manner. The chatbot employs the [OpenAI GPT-3](https://openai.com/api/) API and [GPT Index](https://github.com/jerryjliu/gpt_index) to achieve this functionality, which has been exemplified by its use in Monash DeepNeuron's showcase where it acts as a customer service representative, providing information on DeepNeuron's projects and activities. The chatbot utilizes data extracted from the [Monash DeepNeuron website](https://www.deepneuron.org/) as a source of context for its responses.

## requirements 
1. Install software dependencies
- flask
- gpt-index
2. get OpenAI API key from [https://beta.openai.com/account/api-keys](https://beta.openai.com/account/api-keys)
3. Put your data files into the directory /data for chatbot to read

## commands to run 
- `export OPENAI_API_KEY=<your_key>`
- `python app.py`
- browse to http://127.0.0.1:5000 

## Example of the chatbot compared to ChatGPT: The chatbot is able to answer about Monash DeepNeuron correctly
![ChatGPT_example](/assets/ChatGPT_example.png)
![example](/assets/example.png)


## TODO
- fix web scraping. Same code works on google colab works but not extract_website.py. Maybe versions of software?
- you need to format beautiful soup for every website :(
- nice frontend 
- add memory to the chatbot to have a conversationla feature
- local GPT-2
- use free embedding model
