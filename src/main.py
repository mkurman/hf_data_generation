import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import os
import random

from joblib import Parallel, delayed
from tqdm import tqdm
from configparser import ConfigParser
from src.func.load import load_dataset
from src.func.request import groq_request, hf_request

tqdm.pandas()

# Load config
config = ConfigParser()
config.read('config.ini')

## Basic
USE_HF = int(config['base']['USE_HUGGING_FACE'])
DATASET_PATH = config['base']['DATASET_PATH']
HF_TOKEN = os.environ['HF_TOKEN'] if 'HF_TOKEN' in os.environ and os.environ['HF_TOKEN'] is not None else config['base']['HF_TOKEN']
GROQ_TOKEN = os.environ['GROQ_TOKEN'] if 'GROQ_TOKEN' in os.environ and os.environ['GROQ_TOKEN'] is not None else config['base']['GROQ_TOKEN']
N_JOBS = config['base']['N_JOBS']
OUTPUT_FILE_NAME = config['base']['OUTPUT_FILE_NAME']
ERROR_OUTPUT_FILE_NAME = config['base']['ERROR_OUTPUT_FILE_NAME']
SLEEP_TIME_S = config['base']['SLEEP_TIME_S']
TIMEOUT = config['base']['TIMEOUT']
NUM_RETRIES = config['base']['NUM_RETRIES']
INSTRUCTION = config['base']['INSTRUCTION']
TEMPERATURE = config['base']['TEMPERATURE']
MAX_NEW_TOKENS = config['base']['MAX_RESPONSE_TOKENS']
SHUFFLE_INSTRUCTIONS = int(config['base']['SHUFFLE_INSTRUCTIONS'])
SKIP_X_INSTRUCTIONS = int(config['base']['SKIP_X_INSTRUCTIONS'])

INSTRUCTION = INSTRUCTION if len(INSTRUCTION.strip()) > 0 else None

## Hugging Face & Groq generation
HF_MODEL_API = config['hf_generation']['MODEL_API_ENDPOINT']
GROQ_MODEL_NAME = config['groq_generation']['MODEL_NAME']


if __name__ == '__main__':
    # Load dataset
    print(f"Loading dataset from {DATASET_PATH}...")
    df = load_dataset(DATASET_PATH)

    instructions = df['input'].tolist()

    del df

    # Shuffle instructions
    if SHUFFLE_INSTRUCTIONS:
        print("Shuffling instructions...")
        random.shuffle(instructions)

    # Generate
    if not USE_HF and GROQ_TOKEN is not None:
        print("Generating using GROQ...")
        groq_responses = Parallel(n_jobs=int(N_JOBS), batch_size=1, timeout=int(TIMEOUT))(
            delayed(groq_request)(instructions[i+SKIP_X_INSTRUCTIONS],
                model_name=GROQ_MODEL_NAME,
                groq_token=GROQ_TOKEN,
                output_file_name=OUTPUT_FILE_NAME,
                error_output_file_name=ERROR_OUTPUT_FILE_NAME,
                instruction=INSTRUCTION,
                temperature=TEMPERATURE,
                sleep_time_in_seconds=SLEEP_TIME_S,
                num_retries=NUM_RETRIES
            )
            for i in tqdm(range(len(instructions[SKIP_X_INSTRUCTIONS:])))
        )

    elif USE_HF and HF_TOKEN is not None:
        print("Generating using Hugging Face...")
        hf_responses = Parallel(n_jobs=N_JOBS, batch_size=1, timeout=int(TIMEOUT))(
            delayed(hf_request)(instructions[i+SKIP_X_INSTRUCTIONS],
                api_url=HF_MODEL_API,
                hf_token=HF_TOKEN,
                output_file_name=OUTPUT_FILE_NAME,
                error_output_file_name=ERROR_OUTPUT_FILE_NAME,
                instruction=INSTRUCTION,
                temperature=TEMPERATURE,
                max_new_tokens=MAX_NEW_TOKENS,
                sleep_time_in_seconds=SLEEP_TIME_S,
                num_retries=NUM_RETRIES
            )
            for i in tqdm(range(len(instructions[SKIP_X_INSTRUCTIONS:])))
        )
    else:
        raise ValueError("Please set either USE_HF or GROQ_TOKEN to True. Make sure you have set the correct environment variables. " +
                         "HF_TOKEN: Hugging Face API token; GROQ_TOKEN: GROQ CloudA PI token")