# hf_data_generation
This repo contains a simple machine-learning instruction datasets generation script using open-sourced **Hugging Face** models and a Hugging Face PRO subscription (required) or free tier of **Groq Cloud account**, which allows you to generate ~14k requests per day (30 per minute).

### Installation
```pip install -r requirements.txt```

### HF Configuration
1. Setup your huggingface account.
2. Subscribe to huggingface pro and get the api key.
3. Copy `config.ini-example` to `config.ini` and edit the `config.ini` file and add your api key.
4. To use a different model, edit the `config.ini` file and change the model name. You can get the endpoint from the hugging face model hub by clicking on "Deploy model" and copying the "Inference Endpoint (Serverless)" URL.

![Image](assets/img.png)

### Groq Configuration
1. Setup your groq.com cloud account.
2. Copy `config.ini-example` to `config.ini` and edit the `config.ini` file and add your groq api key.
3. To use a different model, edit the `config.ini` file and change the model name. You can get the endpoint from the groq cloud account documentation (https://console.groq.com/docs/models).

### Usage
1. From the root of your project, run the `python src/main.py` script.
2. Your data must contain a column named `input` with the prompt input.
3. The generation process is parallel but may take some time depending on data size, jobs count and timeout.
4. Each response is immediately included in the output file, so you don't have to wait for the process to complete.
5. Please, give a star if you like it. Thanks ! 
6. Enjoy!