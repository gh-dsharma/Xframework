import logging
import time
import re
logger = logging.getLogger(__name__)


def generate_accession_id() -> 'str':
    """
    Generate a random accession id

    :Usage:
        acs:generate_accession_id
    :Returns:
        An accession id
    """
    accession_id_base = "A012250001"
    timestamp = time.time()
    accession_id = accession_id_base + str(timestamp)
    accession_id = re.sub('[.]', '', accession_id) 
    logger.info("generated {}".format(accession_id))
    return accession_id