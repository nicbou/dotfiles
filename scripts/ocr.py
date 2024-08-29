#!/usr/bin/env python3
"""
OCR a given PDF or the PDFs in a given directory. The OCR data is added to the files.
"""
from ocrmypdf.exceptions import PriorOcrFoundError, EncryptedPdfError, DigitalSignatureError, TaggedPDFError
from pathlib import Path
import logging
import ocrmypdf
import sys

if len(sys.argv) > 1:
    ocr_path = Path(sys.argv[1])
else:
    ocr_path = Path.cwd()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(message)s',
)

ocrmypdf.configure_logging(ocrmypdf.Verbosity.default)

if ocr_path.is_file():
    filenames = [ocr_path, ]
else:
    filenames = ocr_path.glob("**/*.pdf")

for filename in filenames:
    logging.info(f"Processing {filename}")
    try:
        result = ocrmypdf.ocr(filename, filename, deskew=True)
    except PriorOcrFoundError:
        logging.warning("Skipped document because it already contained text")
    except EncryptedPdfError:
        logging.warning("Skipped document because it's encrypted")
    except DigitalSignatureError:
        logging.warning("Skipped document because it has a digital signature")
    except TaggedPDFError:
        logging.warning("Skipped document because it's marked as a tagged PDF")
