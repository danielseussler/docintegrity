import datetime
import os
from pathlib import Path

import gensim
import gensim.downloader as api
import nltk
import pandas as pd
from tqdm import tqdm

from docintegrity.utils import (filter_files_by_encoding, get_file_list,
                                prune_short_sentences,
                                read_docx_and_get_sentences)

home_dir = Path.home()
cache_dir = os.path.join(home_dir, ".docintegrity")
gensim_dir = os.path.join(home_dir, ".docintegrity", "gensim-data")
nltk_dir = os.path.join(home_dir, ".docintegrity", "nltk_dir")

# append cache directory
nltk.data.path.append(nltk_dir)
api.BASE_DIR = gensim_dir


def init_tokenizer(download_dir: str):
    """Download tokenizer to split documents to sentences."""
    nltk.download("punkt", download_dir=nltk_dir, quiet=True)
    return nltk.sent_tokenize


def init_model(cache_dir: str, model_name: str) -> str:
    """Download model to specified cache directory and return model path."""
    api.BASE_DIR = os.path.join(cache_dir, "gensim-data")
    available_models = api.info()["models"].keys() # type: ignore

    assert (
        model_name in available_models
    ), "Invalid model_name: {}. Choose one from {}".format(
        model_name, ", ".join(available_models)
    )
    model_path = api.load(model_name, return_path=True)

    return model_path


def calculate_sentence_distance(
    model: gensim.models.keyedvectors.KeyedVectors, sentence1: str, sentence2: str
) -> float:
    return model.wmdistance(sentence1, sentence2)  # type: ignore


def find_duplicates(
    folder_path: str,
    output_path: None | str = None,
    distance_threshold: float = 0.2,
    model_name: str = "glove-wiki-gigaword-100",
) -> pd.DataFrame:
    # Setup model

    model_path = init_model(cache_dir=cache_dir, model_name=model_name)
    model = gensim.models.KeyedVectors.load_word2vec_format(model_path, binary=False)

    # Setup text docx
    file_list = get_file_list(folder_path)
    file_list = filter_files_by_encoding(file_list=file_list, file_extension=".docx")

    # Setup tokenizer
    tokenizer = init_tokenizer(download_dir=nltk_dir)
    docs = []

    for file_path in file_list:
        doc = read_docx_and_get_sentences(
            file_path=file_path, tokenizer=tokenizer, cache_dir=cache_dir
        )
        doc = prune_short_sentences(doc, min_length=20)
        docs.append(doc)

    # Compare sentences by embedding similiarity
    duplicates = []

    for i, current_doc in enumerate(tqdm(docs[:-1])):
        for sentence1 in current_doc:
            for j, other_doc in enumerate(docs[i + 1 :], start=i + 1):
                for sentence2 in other_doc:
                    distance = calculate_sentence_distance(
                        model, sentence1.lower().split(), sentence2.lower().split()
                    )
                    if distance < distance_threshold:
                        duplicates.append(
                            {
                                "similarity": distance,
                                "doc1": os.path.basename(file_list[i]),
                                "sentence1": sentence1,
                                "doc2": os.path.basename(file_list[j]),
                                "sentence2": sentence2,
                            }
                        )

    df = pd.DataFrame(duplicates)
    df = df.sort_values(by=["similarity"])
    
    if output_path:  
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y%m%d_%H%M%S")

        folder_name = os.path.basename(os.path.dirname(folder_path))
        fname = f"{formatted_datetime}_{folder_name}.csv"
        
        df.to_csv(os.path.join(output_path, fname), index=False)

    return df
