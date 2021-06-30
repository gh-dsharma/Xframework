import subprocess
import logging

logger = logging.getLogger(__name__) 

def run(input: str, verbose=True, *args, **kwargs):
    """
    Run a bash command and return the output

    :Usage:
        bash = "md5sum {} | cut -d ' ' -f1".format(str(filepath))
        md5sum = helper.subprocess_helper.run(bash)
    :Returns:
        the output of the command
    """
    p1 = subprocess.run(input, shell=True, capture_output=True, text=True, *args, **kwargs)
    #default drectory is in /CSRM-Emerald/test/framework/
    #shell to pass args as str
    #capture_output so we can log the results of the command in p1.stdout
    #text so it doesn't have to be decoded
    if verbose:
        logger.info("running bash command: {}".format(input))
        logger.info("stdout is: {}".format(p1.stdout))
    if p1.returncode: #return code is 0 if successful and non-zero otherwise
        logger.error("error: {}, p1.returncode: {}".format(p1.stderr, p1.returncode))
        return p1.returncode
    return p1.stdout.rstrip('\n')



        

    

