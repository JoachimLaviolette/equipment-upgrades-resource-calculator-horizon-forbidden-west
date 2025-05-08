# Equipment upgrades resource calculator - Horizon Forbidden West

Python program that computes total resources needed to fully upgrade a set of equipments (weapons, armors) in the game "Horizon - Forbidden West" (Guerilla Games)

## Input parameters

The `dataset` directory is expected to contain screenshots with the upgrade costs of the equipments you want to fully upgrade. To get such screenshots, find a workbench in the game, go to the upgrad epage of the equipment and take a screenshot. Then, crop the image so it displays the costs area only. Here is an example:

![Screenshot of some equipment's upgrade costs](./dataset_example_0.jpg)

## Description

1. The program extracts the upgrade costs from the provided screenshots via text extraction techniques. 2 text extraction engines can be used: 
- Google Cloud Vision
- Tesseract OCR (_still WIP_)
2. The program cleans up the extracted text so it can be processed easily
3. The program computes the total cost per resource (shards are omitted, I assume you will have enough 😉)
4. The program writes a compilation table with the resource costs in a file (see `output/results.md` file after execution), which looks like this *(in French)*:

| Ressource         | Total       |
|-------------------|-------------|
| Ressource 1      | 12     |
| Ressource 2      | 16     |
| ...      | ...     |

## Prerequisites

### If using Google Tesseract OCR engine

The engine must be installed on your personal workstation so the program can execute it (see https://tesseract-ocr.github.io/tessdoc/Installation.html)

## Environment variables

At the root of the projet tree, duplicate the `.env.sample` file and rename it `.env`. The following variables can be set:
- `GOOGLE_CLOUD_VISION_API_KEY`: API key required only if using this engine (optional - if not specified, you will be asked to provide an API key if you select GCV engine)
- `EXTRACTION_ENGINE`: either 'google_cloud_vision' or 'tesseract' (optional - if not specified, will be asked by the program)

## Execution

Run the following command to execute the program:
```shell
python -m venv venv 
source venv/Scripts/activate
pip install -r requirements.txt
py main.py
```