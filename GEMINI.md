# Project Overview

This project is a data processing pipeline designed to merge multiple conversational datasets into a unified format. The primary script, `main.py`, reads all `.json` files from the `dataset` directory, combines them, and then outputs two consolidated files: `merged_dataset.json` and `merged_dataset.jsonl`.

The datasets are structured as conversations, with fields for `id`, `system` (system prompt), `user` (user input), and `assistant` (assistant's response). The conversations are in Vietnamese.

## Building and Running

To run the project, execute the `main.py` script from the root directory:

```bash
python main.py
```

This will generate the `merged_dataset.json` and `merged_dataset.jsonl` files in the root of the project.

## Key Files

*   `main.py`: The main script that performs the dataset merging.
*   `dataset/`: This directory contains the source `.json` files, organized into `single-turn` and `multi-turn` subdirectories.
*   `sample_dataset_10.csv`: A sample of the dataset in CSV format.
*   `README.md`: The project's README file.

## Development Conventions

The Python script `main.py` is self-contained and does not have any external dependencies. The code is straightforward and includes print statements to track the progress of the merging process.
