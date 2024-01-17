# docintegrity

## Description

`docintegrity` is a small python package for plagiarism checks in docx files. It takes a folder path as argument and employs vector embeddings to find 'similar' sentences across the documents in the respective folder. The user may specify a threshold for the sentence similarity, all sentences below the threshold will be saved to a .csv file.

## Installation

The package can be installed directly from GitHub via `pipx`.
```sh
pipx install git+https://github.com/danielseussler/docintegrity.git
```

## Usage

It can both be used as an imported package or a standalone cli program. For the former, import the function and specify the folder of the docx files. If desired, one can additionally set the threshold and the embedding model. 

```python
from docintegrity.core import find_duplicates

folder_path = "..."
duplicates = find_duplicates(folder_path)
```

When the output_path variable is specified, the dataframe is saved as csv to the provided directory.

Alternatively, one can run the package as a standalone cli program. After installation with `pipx`, run

```sh
# run program with interface or parse arguments
docintegrity
docintegrity --folder-path "..." --output-path "..."

# display help
docintegrity --help
```

The program creates a cached folder `.docintegrity/` in the user's home directory which can be safely deleted after usage.

## Documentation 

Documentation and examples on the usage can be found in the [docs](https://github.com/danielseussler/docintegrity/tree/master/docs).

## Disclaimer

tbd.
