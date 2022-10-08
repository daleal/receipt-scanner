# Receipt Scanner

## Installation

Install using pip!

```sh
pip install receipt-scanner
```

## Usage

### As a package

After installation, you can import the `scan` method from the library. Just pass the image location (it can be a local path or a URL), an optional regular expression to filter the parsed text and the optional `debug` parameter:

```py
import re
from receipt_scanner import scan

expression = re.compile("([0-9]+\.[0-9]+)")
scanned_text_lines = scan(
    "path/to/some/image.jpg",
    regular_expression=expression,
    debug=True,
)
```

The `scan` method returns a list of strings for each text line that the regular expression matched. If no regular expression gets passed, every parsed text line will be returned.

### As a CLI

You can also use `receipt-scanner` as a CLI! Once installed, the `scanner` command will be available. Here is a sample usage:

```sh
scanner --image path/to/some/image.jpg --expression "([0-9]+\.[0-9]+)" --debug
```

### Debugging

The `debug` flag will show logs of every step, and will freeze each image manipulation step to show the result of said manipulation. This can be useful to understand why the `scan` command might be returning an empty list, for example (you might find that the image has poor contrast and that the contour of the receipt is not being correctly mapped).

## Developing

### Requirements

- [Poetry](https://python-poetry.org)
- [Tesseract](https://tesseract-ocr.github.io/tessdoc/Installation.html)
- [Teseract Spanish](https://parzibyte.me/blog/2019/05/18/instalar-tesseract-ocr-idioma-espanol-ubuntu)

### Steps

Clone the repository:

```sh
git clone https://github.com/daleal/receipt-scanner.git

cd receipt-scanner
```

Then, recreate the environment:

```sh
make build-env
```

Once the package is installed for development (`poetry install`), you can use the CLI from the virtualenv.

## Aknowledgements

Most of the code from this project was adapted from StackOverflow answers to questions about contour-finding, denoising and stuff like that. I also used code from several guides from the internet for utilities such as transforming a contour to a rect. Without those answers, most of this library would have been impossible for me to write. Thanks for the awesome information! 💖
