import click

from docintegrity.core import find_duplicates


@click.command()
@click.option("--folder-path", prompt="Document Folder", help="Path to the folder that includes the docx files. Note, the path should be provided without quotation marks.")
@click.option("--output-path", prompt="Output Folder", help="Path to the folder where the results should be saved. Note, the path should be provided without quotation marks.")
@click.option(
    "--distance-threshold",
    prompt="Threshold for sentence similarity",
    default=0.2,
    type=float,
    help="The threshold for which similar sentences are saved to the output. Lower is better. Default is 0.2.",
)
@click.option(
    "--model-name",
    prompt="Embedding model name",
    default="glove-wiki-gigaword-100",
    help="The embedding model used to embedd the sentences in the documents.",
)
def cli(*args, **kwargs) -> None:
    _ = find_duplicates(*args, **kwargs)
    print("The output was saved in {output_path}.")
