import requests
import json
import time

from groq import Groq
from typing import Optional
from src.func.write import write_response, write_error_response


def hf_query(payload: dict, api_url: str, hf_token: str) -> dict:
    headers = {"Authorization": f"Bearer {hf_token}"}
    response = requests.post(api_url, headers=headers, json=payload)
    return response.json()


def hf_request(text: str,
               api_url: str,
               hf_token: str,
               output_file_name: str,
               error_output_file_name: str,
               instruction: Optional[str] = None,
               temperature: float = 0.7,
               max_new_tokens: Optional[int] = None,
               sleep_time_in_seconds: int = 30,
               num_retries: int = 3) -> Optional[dict]:
    finished = False
    retry = 0

    system = f'<|system|>{instruction}<|end|>' if instruction is not None else ''

    while not finished:
        try:
            payload = {
                "inputs": f"{system}<|user|>\n{text}<|end|>\n<|assistant|>",
                "parameters": {
                    "temperature": float(temperature)
                }
            }

            if max_new_tokens is not None:
                payload['parameters']['max_new_tokens'] = int(max_new_tokens)

            output = hf_query(payload=payload, api_url=api_url, hf_token=hf_token)

            write_response(output=output[0]['generated_text'],
                           output_file_name=output_file_name,
                           instruction=instruction,
                           input_str=text)

            return None
        except Exception as e:
            retry += 1
            time.sleep(int(sleep_time_in_seconds))

            if retry == int(num_retries):
                write_error_response({'input': text, 'output': f'Error: {e}', 'instruction': instruction}, error_output_file_name)


def groq_query(groq_token: str,
               model_name: str,
               messages: list[dict],
               temperature: float = 0.7) -> Optional[str]:
    client = Groq(
        api_key=groq_token,
    )

    response = client.chat.completions.create(
        messages=messages,
        model=model_name,
        temperature=float(temperature),
    )
    return response.choices[0].message.content


def groq_request(text: str,
                 model_name: str,
                 groq_token: str,
                 output_file_name: str,
                 error_output_file_name: str,
                 instruction: Optional[str] = None,
                 temperature: float = 0.7,
                 sleep_time_in_seconds: int = 30,
                 num_retries: int = 3) -> Optional[dict]:
    finished = False
    retry = 0

    while not finished:
        try:
            messages = []

            if instruction is not None:
                messages.append(
                    {
                        'role': 'system',
                        'content': instruction
                    })

            messages.append({
                "role": "user",
                "content": text,
            })

            output = groq_query(groq_token=groq_token,
                                model_name=model_name,
                                messages=messages,
                                temperature=temperature)

            write_response(output=output,
                           output_file_name=output_file_name,
                           instruction=instruction,
                           input_str=text)

            return None
        except Exception as e:
            retry += 1
            time.sleep(int(sleep_time_in_seconds))

            if retry == int(num_retries):
                write_error_response({'input': text, 'output': f'Error: {e}', 'instruction': instruction}, error_output_file_name)
