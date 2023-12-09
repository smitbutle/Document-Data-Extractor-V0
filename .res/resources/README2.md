<div align="center">

# Doc-KV-Extractor: Convert unstructured document to structured key-value data.

</div>

## Configuration

Define the ‘key’s and their associated ‘value’s regular expression definitions that are to be extracted.

Depending on the need, on the applications’ configuration pane, you can optionally add ‘synonyms’ for a particular ‘key’ that share value’s regular expressions among multiple keys. This helps in sharing regular expressions among multiple keys either from the same or across different documents.

Example: The key entity called ‘Customer’ and ‘Vendor’ may share the same value expression

![Configuration%20pane%20to%20define%20key%20and%20values%20regular%20expressions](https://blogs.sap.com/wp-content/uploads/2020/11/fig2-1.png)

Configuration pane to define key and values regular expressions

On saving the configuration, the application creates a JSON file with all the specified fields and will be used in the information extraction process.

<br>

## Document capture

Capture a picture of the physical Bill-of-Lading document using a mobile phone or a scanner

![Bill-of-lading%20document%20captured%20using%20mobile%20phone](https://blogs.sap.com/wp-content/uploads/2020/11/fig3.jpg)

Bill-of-lading document captured using a mobile phone

<br>

### Image pre-processing

The document after being captured may not always be in a shape or form that we would like to use for extracting information. In this case, you can see that the document is tilted, inclined, and is of poor contrast. This will be transformed into a workable format using corner detection, image registration, and local-histogram equalization techniques.

![Corner%20detection%20as%20part%20of%20image%20pre-processing](https://blogs.sap.com/wp-content/uploads/2020/11/fig4.jpg)

Corner detection as part of image pre-processing

![Transformed%20bill-of-lading%20document%20after%20pre-processing](https://blogs.sap.com/wp-content/uploads/2020/11/fig5.jpg)

Transformed bill-of-lading document after pre-processing

<br>

### Entity location and centroid determination

1.  Extract all words and word locations from the transformed document image. In this case, an open-source optical character recognition algorithm called ‘Tesseract’ is used to extract the words and word coordinates information.![Extracted%20word%20and%20word%20locations](https://blogs.sap.com/wp-content/uploads/2020/11/fig6-1.png)
2.  Check if the keys have multiple words. If so, identify and merge the multi-word keys to form a single entity.![](https://blogs.sap.com/wp-content/uploads/2020/11/fig7.png)
3.  Calculate the centroid of all the word or entity locations as shown in the example below. A centroid is the arithmetic mean of all the positions in a given shape (rectangle in this case) box. The red star in the center of the box from the following figure represents the centroid of the particular entity.  
    
    #### ![](https://blogs.sap.com/wp-content/uploads/2020/11/fig8.png)

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

## How it works


It works by using `openCV` to transform image into scanned format, and later using `DocQuery` to extract necessory information.

DocQuery is created by the team at Impira.
Under the hood, docquery uses a pre-trained zero-shot language model, based on [LayoutLM](https://arxiv.org/abs/1912.13318), that has been
fine-tuned for a question-answering task. The model is trained using a combination of [SQuAD2.0](https://rajpurkar.github.io/SQuAD-explorer/)
and [DocVQA](https://rrc.cvc.uab.es/?ch=17) which make it particularly well suited for complex visual question answering tasks on
a wide variety of documents. The underlying model is also published on HuggingFace as [impira/layoutlm-document-qa](https://huggingface.co/impira/layoutlm-document-qa)
which you can access directly.

## Limitations

Handwritten invoices should be avoided, because of factors such as Variability in Handwriting, Lack of Standardization, Irregularities and Artifacts and Cursive Writing.


## Status

This project is ready to be used on your local machine as of now. 