import json

def write_response(output: str,
                   output_file_name: str,
                   instruction: str = '',
                   input_str: str = '') -> None:
    response = output.replace(instruction, '') \
                .replace(input_str, '') \
                .replace('<|end|>', '') \
                .replace('<|assistant|>', '') \
                .replace('<|system|>', '') \
                .replace('<|user|>', '').strip()

    with open(f'{output_file_name}.jsonl', 'a') as f:
        f.write(json.dumps({'instruction': instruction, 'output': response, 'input': input_str.strip()}))
        f.write('\n')
        f.close()


def write_error_response(output: dict, error_output_file_name: str) -> None:
    with open(f'{error_output_file_name}.jsonl', 'a') as f:
        f.write(json.dumps(output))
        f.write('\n')
        f.close()