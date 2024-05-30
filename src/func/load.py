import pandas as pd
from datasets import load_from_disk, load_dataset


def load_dataset(path: str) -> pd.DataFrame:
    if path.endswith('json') or path.endswith('jsonl'):
        df = pd.read_json(path, lines=path.endswith('jsonl'))
    elif path.endswith('csv'):
        df = pd.read_csv(path)
    elif path.endswith('xlsx'):
        df = pd.read_excel(path)
    elif path.endswith('parquet'):
        dataset = load_from_disk(path)
        df = dataset.to_pandas()

        del dataset
    elif path.endswith('arrow'):
        dataset = load_from_disk(path)
        df = dataset.to_pandas()

        del dataset
    else:
        try:
            dataset = load_dataset(path, split='train')
            df = dataset.to_pandas()

            del dataset
        except:
            raise "This data type is not supported."

    return df
