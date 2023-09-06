<div align="center">

# Doc-KV-Extractor: Convert unstructured document to structured key-value data.

</div>


  ```sh
  # Status
  The project is under active development.
  The current version is a proof of concept and is not ready for production use.
  ```
## Pre-requisites

First you must install the [tesseract](https://github.com/tesseract-ocr/tesseract) library:

- Mac OS X (using [Homebrew](https://brew.sh/)):

  ```sh
  brew install tesseract
  ```

- Ubuntu:

  ```sh
  sudo apt install tesseract-ocr
  ```
- Arch:

  ```sh
  sudo pacman -S tesseract
  ```
- Windows:
    
    - Download tesseract exe from https://github.com/UB-Mannheim/tesseract/wiki.
    - Configure your installation (choose installation path and language data to include)
    - Add Tesseract OCR to your environment variables


## Quickstart

- Optional: To create a Virtual ENV.

  ```sh
  python -m venv env
  ```
  ```sh
  source env/bin/activate
  ```

- Install the dependencies:

  ```sh
  pip install -r requirements.txt
  ```
- Run main.py:

  ```sh
  python -u "./main.py"      
  ```


## Use cases

Extracting key-value pairs out of the unstructured business documents like scanned bill-of-lading.

![](https://blogs.sap.com/wp-content/uploads/2020/11/fig12.png)

Information extracted from the document image along with the location of the extracts 

_(Not actual frontend, Image just for representation purpose)_


## Limitations

Handwritten invoices should be avoided, because of factors such as Variability in Handwriting, Lack of Standardization, Irregularities and Artifacts and Cursive Writing.


