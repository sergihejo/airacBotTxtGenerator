# airacBotTxtGenerator

Tool to extract data from AIRAC cycle PDF files and generate a TXT file.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Introduction

`airacBotTxtGenerator` is a Python-based tool designed to extract data from AIRAC cycle PDF files and generate a corresponding TXT file.

## Features

- Extracts text from AIRAC cycle PDF files.
- Validates AIRAC cycle number and amendment download link.
- Fetches AIRAC data from Eurocontrol.
- Generates a TXT file with the extracted data.

## Installation
### Windows

1. Download the latest executable from the [releases page](https://github.com/sergihejo/airacBotTxtGenerator/releases).
2. Run the executable.
3. Follow the prompts to enter the AIRAC cycle number and the amendment download link.
4. The TXT file will be generated in the same directory as the executable.

### Linux

1. Download the latest executable from the [releases page](https://github.com/sergihejo/airacBotTxtGenerator/releases).
2. Make the executable file executable:
    ```sh
    chmod +x airacBotTxtGenerator
    ```
3. Run the executable:
    ```sh
    ./airacBotTxtGenerator
    ```
4. Follow the prompts to enter the AIRAC cycle number and the amendment download link.
5. The TXT file will be generated in the same directory as the executable.

## Local Installation

If you prefer to run the script locally, follow the steps below:

1. Clone the repository:
    ```sh
    git clone https://github.com/sergihejo/airacBotTxtGenerator.git
    ```
2. Navigate to the project directory:
    ```sh
    cd airacBotTxtGenerator
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. Ensure the AIRAC cycle **PDF file is in the same directory as the script and named `AIRAC_XXXX.pdf`.**
2. Run the script:
    ```sh
    python main.py
    ```
3. Follow the prompts to enter the AIRAC cycle number and the amendment download link.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
