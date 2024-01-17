import os
import pprint
from typing import Any, List

import gensim.downloader as api
from docx import Document


def print_model_info(model_name: str = "glove-wiki-gigaword-100") -> None:
    """Print model info corresponding to the embedding model specified in model_name."""
    pprint.pprint(api.info(name=model_name))


def get_file_list(directory_path: str, include_directory: bool = True) -> List[Any]:
    """Get a list of file names of a directory passed to the function."""
    try:
        files = os.listdir(directory_path)

        if include_directory:
            return [os.path.join(directory_path, file) for file in files]
        else:
            return files
    except OSError as e:
        print(f"Error reading directory {directory_path}: {e}")
        return []


def print_file_list(file_list: List[Any]) -> None:
    """Print list of file nicely with counter."""
    counter = 0
    for file in file_list:
        counter = counter + 1
        print(f"File {counter}: {file}")


def filter_files_by_encoding(
    file_list: List[str], file_extension: str = ".docx"
) -> List[str]:
    """Filters a list of files by the respective file extension."""
    filtered_files = []

    for file_path in file_list:
        if file_path.endswith(file_extension):
            filtered_files.append(file_path)

    return filtered_files


def read_docx_and_get_sentences(file_path: str, tokenizer, cache_dir: str) -> List[str]:
    """Read the document and chunk it into seperate sentances."""
    doc = Document(file_path)
    sentence_tokenizer = tokenizer

    sentences = []
    for paragraph in doc.paragraphs:
        sentences.extend(sentence_tokenizer(paragraph.text))

    return sentences


def prune_short_sentences(input_list: List[str], min_length: int = 20) -> List[str]:
    """Prune strings in the list that have a length less than the specified threshold."""
    return [string for string in input_list if len(string) >= min_length]
