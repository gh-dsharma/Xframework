import textract
import logging

logger = logging.getLogger(__name__)

class PdfHelper:

    @staticmethod
    def get_text(pdf_path: str, verbose: bool = False, method: str = None, ) -> 'str':
        """
        :Usage:
            pdf_location = "/ghds/groups/bip_sqa/personal_spaces/pco/temp/pytest_framework_develop/tests/hamster_demo/data/EIO_NTC_RESULT_test_oct.pdf"
            text = helper.pdf_helper.get_text(pdf_location, True)
        :Returns:
            Pdf text
        :Note:
            Pdf might be a long line. VSCode has a line wrap feature in View -> Toggle Word Wrap
        """
        if method == None:
            method = 'pdfminer'
        text = textract.process(pdf_path, method='pdfminer')
        if verbose:
            logger.info("pdf {} has the following text:\n {} ".format(pdf_path, text))
        return text
        