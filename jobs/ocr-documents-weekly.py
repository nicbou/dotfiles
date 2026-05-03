#!/usr/bin/env python3
"""
Weekly job: OCR all PDFs in ~/Documents in-place.
Skips files that are already OCR'd, encrypted, signed, or tagged.
"""

import ocrmypdf
from ocrmypdf.exceptions import (
    DigitalSignatureError,
    EncryptedPdfError,
    PriorOcrFoundError,
    TaggedPDFError,
)
from pathlib import Path

SKIP = (PriorOcrFoundError, EncryptedPdfError, DigitalSignatureError, TaggedPDFError)

ocrmypdf.configure_logging(ocrmypdf.Verbosity.quiet)

for pdf in sorted((Path.home() / "Documents" / "Important Documents").glob("**/*.pdf")):
    try:
        ocrmypdf.ocr(pdf, pdf, deskew=True)
    except SKIP:
        pass
