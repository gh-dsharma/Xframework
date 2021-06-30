from libraries.helper.pdf_helper import PdfHelper
from pathlib import Path
import pytest


def test_gid_205078_get_text():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) Run this unit test
            ER: This unit test passes
            Notes: NA

    Projects: BI Internal SW Tools
    """
    pdf_helper = PdfHelper()
    pdf_path = Path(__file__).parent / "unit_test_data/SPK_QC_Results_846294.pdf"
    pdf_text = pdf_helper.get_text(pdf_path)
    string_to_find = "GuardantOMNI CDx Sample Preparation Kit - QC Lot Release Data"
    assert string_to_find in pdf_text.decode()


def test_gid_205079_get_text_negative():
    """
    Description:
        Verify this unit test

    Prerequisites: NA

    Test Data: NA

    Steps:
        1) Run this unit test
            ER: This unit test passes
            Notes: NA

    Projects: BI Internal SW Tools
    """
    pdf_helper = PdfHelper()
    pdf_path = Path(__file__).parent / "unit_test_data/nonexistent_pdf"
    with pytest.raises(Exception):
        pdf_helper.get_text(pdf_path)
