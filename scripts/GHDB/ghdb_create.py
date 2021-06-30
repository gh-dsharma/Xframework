'''
        Create a new FlowcellID based on an existing FlowcellID

        SYNOPSIS
        ========

        ::
        python3 ghdb_create.py -in_FCID '150911_NB501022_0013_AHJ33JBGXX'

        DESCRIPTION
        ===========

        Creates new FlowcellID based on existing FlowcellID by using the user input (-in_FCID)
        as a reference to create the new FlowcellID and samples.

        The script takes an optional parameter --out_FCID to create the FlowcellID as per the user.
        If the parameter is not set, the script will generate a FlowcellID and list it in the logs.

        The script takes an optional parameter --samples to limit the number of generated samples associated with the new FlowcellID.
        If the parameter is not set, the script will generate as many samples as the input FlowcellID.
        If the number of requested samples exceedes the number of samples available in the input FlowcellID, the request is rejected.

        The script takes an optional parameter --file to allow a CSV file to represent the mapping between input samples and output samples.
        This allows the user to model the output samples based on known input samples.
                The CSV file has two columns: in_sample and out_sample.
                Each row will model a sample from the -in_FCID to the --out_FCID.
                If an in_sample has a value, the script will check to see if it's associated with the -in_FCID. 
                If the check fails the script will exit.
                If an in_sample is <EMPTY>, the script will use the nth record returned by the query and use the out_value
                to create a new sample and associate it with the --out_FCID.
                The script will use the out_value to create a new sample and associate it with the --out_FCID
                If the out_value is <EMPTY>, the script will generate a new sample ID and associate it with the --out_FCID.
        Note: If the user passes both the --samples and --file parameter. The script will use the --file over the --sample parameter.

        The script takes an optional parameter --commit to write the new Flowcell and associate output samples. If this parameter is not set
        the script will only generate the log.

        FILES
        =====

        Writes a file, ```ghdb_create.log```.
        Optionally reads a file ```.env```. If the file does not exist, it uses the defaults from get_db_url()
        Optionally reads a file, ```*.csv```.

        EXAMPLES
        ========

        python3 ghdb_create.py -in_FCID '150911_NB501022_0013_AHJ33JBGXX'

        Executing the script above will take the -in_FCID and look for it in the database. It checks to see if there are one or more
        samples associated with it. It generates a new FlowcellID and all samples associated with it.

        python3 ghdb_create.py -in_FCID '150911_NB501022_0013_AHJ33JBGXX' --out_FCID 'VGTEST_D00560_0531_AAAAB0ZZZZ'

        Executing the script above will take the -in_FCID and look for it in the database. It checks to see if there are one or more
        samples associated with it. It checks that the --out_FCID does not exist, and if true, it creates it and generates as many samples
        as the -in_FCID and associates them with the --out_FCID. If the --out_FCID already exists, the script will exit.

        python3 ghdb_create.py -in_FCID '150911_NB501022_0013_AHJ33JBGXX' --out_FCID 'VGTEST_D00560_0531_AAAAB0ZZZZ' --samples 5

        Executing the script above will take the -in_FCID and look for it in the database. It checks to see if the the number of samples
        associated with it is equal or greater to the --samples value. It checks that the --out_FCID does not exist, and if true, it creates it
        and generates as many samples as specified by the --samples parameter and associates them with the --out_FCID.
        If the --out_FCID already exists, the script will exit.

        python3 ghdb_create.py -in_FCID '150911_NB501022_0013_AHJ33JBGXX' --out_FCID 'VGTEST_D00560_0531_AAAAB0ZZZZ' --file 'samples_list.csv'

        Executing the script above will take the -in_FCID and look for it in the database. It checks to see if the the number of samples
        associated with it is equal or greater to the number of samples listed in the CSV file. It checks that the --out_FCID does not exist, and if true, 
        it creates it and generates/creates as many samples as specified by the CSV file and associates them with the --out_FCID.
        If the --out_FCID already exists, the script will exit.
'''

import argparse
import json
import logging
import os
import pandas as pd
import random
import string
import sys

from dotenv import load_dotenv
from sqlalchemy import create_engine


logging.basicConfig(filename='ghdb_create.log', encoding='utf-8', format='%(asctime)s--%(levelname)s: %(message)s', level=logging.INFO)

logging.info(f"====================================Establishing the database connection===================================")

def get_db_url():
        """
                Construct the database url from the .env file or uses the defaults if the .env is not found

                Args: N/A

                Returns:
                        A string with the database url
        """
        load_dotenv()
        SRC_POSTGRES_USER = os.getenv("SRC_POSTGRES_USER", "admin")
        SRC_POSTGRES_PASSWORD = os.getenv("SRC_POSTGRES_PASSWORD", "password")
        SRC_POSTGRES_SERVER = os.getenv("SRC_POSTGRES_SERVER", "localhost")
        SRC_POSTGRES_DB = os.getenv("SRC_POSTGRES_DB", "ghdb")
        SRC_DB = f"postgresql://{SRC_POSTGRES_USER}:" \
                f"{SRC_POSTGRES_PASSWORD}@{SRC_POSTGRES_SERVER}:5432/{SRC_POSTGRES_DB}"

        DST_POSTGRES_USER = os.getenv("DST_POSTGRES_USER", "admin")
        DST_POSTGRES_PASSWORD = os.getenv("DST_POSTGRES_PASSWORD", "password")
        DST_POSTGRES_SERVER = os.getenv("DST_POSTGRES_SERVER", "localhost")
        DST_POSTGRES_DB = os.getenv("DST_POSTGRES_DB", "ghdb")
        DST_DB = f"postgresql://{DST_POSTGRES_USER}:" \
                f"{DST_POSTGRES_PASSWORD}@{DST_POSTGRES_SERVER}:5432/{DST_POSTGRES_DB}"

        prohibited_destination_servers = ['ghdb.ghdna.io', '10.4.170.26']
        if DST_POSTGRES_SERVER in prohibited_destination_servers:
                logging.error(f"You are not allowed to push data to {DST_POSTGRES_SERVER}")
                logging.error("Update the DST_POSTGRES_SERVER variable in your .env file with a non production database!")
                sys.exit(99)

        connections = {'source' : SRC_DB, 'destination' : DST_DB, 'source_server' : SRC_POSTGRES_SERVER, 'destination_server' : DST_POSTGRES_SERVER}

        return connections

src_db_conn = create_engine(get_db_url()['source']).connect()
dst_db_conn = create_engine(get_db_url()['destination']).connect()

logging.info(f"======================================Executing the ghdb_create script=====================================")
logging.info(f"Source Database is >>>>>>>>>> {get_db_url()['source_server']}")
logging.info(f"Destination Database is >>>>> {get_db_url()['destination_server']}")
samples_to_process_in, samples_to_process_out = [], []

def parse_args():
        """
                Return an ArgumentParser object containing the arguments passed in

                Args: N/A
                Returns:
                        An ArgumentParser object containing the arguments passed in
        """
        parser = argparse.ArgumentParser(description='Create a new FlowcellID based on an existing FlowcellID')
        parser.add_argument('-in_FCID', help='input FlowcellID (runid) that contains the necessary data to create a new FlowcellID', required=True)
        parser.add_argument('--out_FCID', help='output FlowcellID (runid) that will be used to create a new FlowcellID')
        parser.add_argument('--samples', help='limit the number of generated samples associated with the output FlowcellID')
        parser.add_argument('--file', help='path to a CSV file that represents the mapping between input samples and output samples')
        parser.add_argument('--commit', help='executes the script and writes out to the database', default=False, action="store_true")

        args_return = parser.parse_args()
        
        logging.debug(f"Arguments are: {args_return}")

        return args_return


def validate_in_FCID(in_FCID):
        """
                Check that the input FlowcellID exists in the database

                Args:
                        in_FCID: A string representing the input Flowcell ID

                Returns:
                        True if FlowcellID is found, logs an error and exists if not
        """
        query = f"SELECT * FROM gh_board WHERE runid = '{in_FCID}';"
        in_FCID_results = pd.read_sql(query, src_db_conn)
        logging.debug(f"Source DB Info: {get_db_url()['source']}")
        if len(in_FCID_results.index) > 0:
                return True
        else:
                logging.error(f"There are no flowcells that match the name of {in_FCID}")
                sys.exit(1)


def validate_in_samples(in_FCID, in_samples):
        """
                When a list of specific samples are passed, check that the input samples are associated with a FlowcellID
                and the output samples don't already exist

                Args:
                        in_FCID: A string representing the input Flowcell ID
                        in_samples: An integer representing the number of samples to generate
                                     OR a pandas DataFrame with the relationship between the input and output samples

                Returns:
                        Log an error and exit if there are no samples available for the specified input Flowcell ID
                        Log an error and exit if there are more samples requested than there are available for
                         the specified input Flowcell ID
                        Log an error and exit if the input sample is not associated with the specified input Flowcell ID
                        Log an error and exit if the output sample is already in the database
                        True otherwise
        """

        def generate_sample_out():
                """
                        Generates a new sample ID based on relevant criteria

                        Args: N/A
                        
                        Returns: A string with the generated value
                """
                #TODO: Generate the new sampleID based on relevant criteria
                random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
                return f"G{random_string}G_1"

        if type(in_samples) is not int:
                in_num_samples = len(in_samples.index)
                logging.debug(f"The number of parsed samples is {in_num_samples}")
        else:
                in_num_samples = in_samples

        query = f"SELECT * FROM gh_sample WHERE runid = '{in_FCID}';"
        limit_query = f"SELECT * FROM gh_sample WHERE runid = '{in_FCID}' LIMIT {in_num_samples};"
        num_of_samples_results = pd.read_sql(query, src_db_conn)
        logging.debug(f"Source DB Info: {get_db_url()['source']}")
        if len(num_of_samples_results.index) > 0:
                if (in_num_samples != 0) and (int(in_num_samples) > len(num_of_samples_results.index)):
                        logging.info(f"There are {len(num_of_samples_results.index)} sample(s) available")
                        logging.error(f"You have requested {in_num_samples} sample(s). Update the number of needed samples or choose a different flowcell")
                        sys.exit(2)
                elif (in_num_samples != 0) and (int(in_num_samples) <= len(num_of_samples_results.index)):
                        logging.info(f"There are {len(num_of_samples_results.index)} sample(s) available")
                        logging.info(f"You have requested {in_num_samples} sample(s)")
                        if type(in_samples) is not int:
                                in_sample = []
                                out_sample = []
                                
                                for index, row in in_samples.iterrows():
                                        in_sample.append(row['in_sample'])
                                        out_sample.append(row['out_sample'])

                                logging.debug(f"The in_sample list contains: {in_sample}")
                                logging.debug(f"The out_sample list contains: {out_sample}")

                                for index, sample in enumerate(in_sample):
                                        if sample != "<EMPTY>":
                                                check_sample = f"SELECT * FROM gh_sample WHERE runid = '{in_FCID}' AND run_sample_id = '{sample}';"
                                                result = pd.read_sql(check_sample, src_db_conn)
                                                logging.debug(f"Source DB Info: {get_db_url()['source']}")
                                                if len(result.index) == 1:
                                                        logging.info(f"Validation: Input sample {sample} is associated with {in_FCID}")
                                                        samples_to_process_in.append(sample)
                                                else:
                                                        logging.error(f"Validation: Input sample {sample} is NOT associated with {in_FCID}. Review the in_sample column of the CSV file")
                                                        sys.exit(2)
                                        else:
                                                logging.error(f"{sample} handling is currently not implemented")
                                                sys.exit(99)
                                                #TODO: Implement populating the samples_to_process_in based of the limit_num_of_samples_results.index
                                                sample = "NotImplemented"

                                                logging.info(f"Auto-assigned sample {sample} from {in_FCID}")
                                                samples_to_process_in.append(sample)

                                for sample in out_sample:
                                        if sample != "<EMPTY>":
                                                check_sample = f"SELECT * FROM gh_sample WHERE run_sample_id = '{sample}';"
                                                result = pd.read_sql(check_sample, dst_db_conn)
                                                logging.debug(f"Destination DB Info: {get_db_url()['source']}")
                                                if len(result.index) == 0:
                                                        logging.info(f"Validation: Output sample {sample} is available to be added")
                                                        samples_to_process_out.append(sample)
                                                else:
                                                        logging.error(f"Validation: Output sample {sample} already exists in the destination database. Review the out_sample column of the CSV file")
                                                        sys.exit(2)
                                        else:
                                                samples_to_process_out.append(generate_sample_out())
                        else:
                                limit_num_of_samples_results = pd.read_sql(limit_query, src_db_conn)
                                logging.debug(f"Source DB Info: {get_db_url()['source']}")
                                for sample in limit_num_of_samples_results.run_sample_id:
                                        samples_to_process_in.append(sample)
                                        samples_to_process_out.append(generate_sample_out())

                        logging.info(f"This is the list of {len(samples_to_process_in)} samples to process: {samples_to_process_in}")
                        logging.info(f"This is the list of {len(samples_to_process_out)} generated samples: {samples_to_process_out}")
                        return True
                else:
                        logging.info(f"There are {len(num_of_samples_results.index)} sample(s) available")
                        logging.info(f"You have not requested a specific number of samples")
                        for sample in num_of_samples_results.run_sample_id:
                                samples_to_process_in.append(sample)
                                samples_to_process_out.append(generate_sample_out())
                        logging.info(f"This is the list of {len(samples_to_process_in)} samples to process: {samples_to_process_in}")
                        logging.info(f"This is the list of {len(samples_to_process_out)} generated samples: {samples_to_process_out}")
                        return True
        else:
                logging.error(f"There are no samples available for this flowcell: {in_FCID}. Provide a different flowcell")
                sys.exit(2)


def create_and_push_to_db():
        """
                Parses the command line arguments
                Validates the input Flowcell ID and samples
                Writes the created/generated output to the database if the --commit argument is passed

                Args: N/A

                Returns: N/A
        """
        args = parse_args()

        commit = args.commit
        if commit:
                logging.info(f"=========================================Commiting to the database=========================================")
        else:
                logging.info(f"=========================The following output will NOT be commited to the database=========================")

        in_FCID = args.in_FCID

        if not args.out_FCID:
                random_number = ''.join(random.choice(string.digits) for _ in range(4))
                random_string = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
                out_FCID = f"{in_FCID[:-15]}{random_number}_G{random_string}G"
        else:
                out_FCID = args.out_FCID

        if not args.file:
                if not args.samples:
                        in_samples = 0
                else:
                        in_samples = int(args.samples)
        else:
                logging.info(f"Parsing the {args.file} file")
                input_csv_data = pd.read_csv(args.file, converters={'in_sample': lambda x: str(x), 'out_sample': lambda x: str(x)})
                in_samples = input_csv_data
        

        if validate_in_FCID(in_FCID) and validate_in_samples(in_FCID, in_samples):
                """
                These tables are treated separately because they don't have a run_sample_id column
                """
                runid_only_tables = {"gh_flowcell", "qc_seq"}

                for table in runid_only_tables:
                        logging.debug(f">>> Working on table: {table}")
                        query = f"SELECT * FROM {table} WHERE runid = '{in_FCID}';"
                        logging.debug(f"Query is: {query}")
                        df = pd.read_sql(query, src_db_conn)
                        logging.debug(f"Source DB Info: {get_db_url()['source']}")
                        if len(df.index) > 0:
                                logging.debug(f"<<IN<< Dataframe is:\n {df}")
                                query_check = f"SELECT * FROM {table} WHERE runid = '{out_FCID}';"
                                df_check = pd.read_sql(query_check, dst_db_conn)
                                logging.debug(f"Destination DB Info: {get_db_url()['source']}")
                                if len(df_check.index) > 0:
                                        logging.error(f"Record not added because record already exists in the destination database:\n {df_check}")
                                        sys.exit(3)
                                else:
                                        logging.info(f"New record will have runid = '{out_FCID}' instead of '{in_FCID}'")
                                        df.runid = out_FCID
                                        if table == "gh_flowcell":
                                                if df.comment.notnull().any():
                                                        df.comment = list(map(lambda x: json.dumps(x), df.comment))
                                                logging.info(f"Adding {len(df.index)} new record(s) to {table}")
                                        logging.info(f"Adding {len(df.index)} new record(s) to {table}")
                                        if commit:
                                                df.to_sql(name=table, con=dst_db_conn, index=False, method='multi', if_exists='append')
                                                logging.debug(f"Destination DB Info: {get_db_url()['source']}")
                                        logging.debug(f">>OUT>> Dataframe is:\n {df}")
                        else:
                                logging.error(f"{in_FCID} does not exist in {table}")
                                sys.exit(3)

                # Treating case where run_sample_id is NULL for sample_qc table (which is processed below)
                table = 'sample_qc'
                logging.debug(f">>> Working on table: {table} where category type is flowcell")
                query = f"SELECT * FROM sample_qc WHERE runid = '{in_FCID}' AND category = 'flowcell';"
                logging.debug(f"Query is: {query}")
                df = pd.read_sql(query, src_db_conn)
                logging.debug(f"Source DB Info: {get_db_url()['source']}")
                if len(df.index) > 0:
                        df.runid = out_FCID
                        logging.info(f"Adding {len(df.index)} new record(s) to {table}")
                        if commit:
                                df.to_sql(name=table, con=dst_db_conn, index=False, method='multi', if_exists='append')
                                logging.debug(f"Destination DB Info: {get_db_url()['source']}")
                        logging.debug(f">>OUT>> Dataframe is:\n {df}")
                else:
                        logging.error(f"{in_FCID} does not exist in {table}")
                        sys.exit(3)

                
                tables = {"gh_board", "snv_call", "indel_call", "gh_sample", "fusion_call", "cnv_call", "deletion_call",
                                "denovofusion_call", "hrd_call", "genomeloh_call", "sample_qc", "ghcnv_qc", "qc_on_target",
                                "sample_coverage", "tmb_call", "msi_call", "gh_fusion", "gh_indel", "gh_variant"}

                for table in tables:
                        logging.debug(f">>> Working on table: {table}")
                        for index, sample in enumerate(samples_to_process_in):
                                logging.debug(f">>> Working on sample: {sample}")
                                query = f"SELECT * FROM {table} WHERE runid = '{in_FCID}' AND run_sample_id = '{sample}';"
                                logging.debug(f"Query is: {query}")
                                df = pd.read_sql(query, src_db_conn)
                                logging.debug(f"Source DB Info: {get_db_url()['source']}")
                                if len(df.index) > 0:
                                        logging.debug(f"<<IN<< Dataframe is:\n {df}")
                                        logging.info(f"New record will have runid = '{out_FCID}' instead of '{in_FCID}'")
                                        df.runid = out_FCID
                                        logging.info(f"New record will have run_sample_id = '{samples_to_process_out[index]}' instead of '{sample}'")
                                        df.run_sample_id = samples_to_process_out[index]
                                        logging.info(f"Adding {len(df.index)} new record(s) to {table}")
                                        if commit:
                                                df.to_sql(name=table, con=dst_db_conn, index=False, method='multi', if_exists='append')
                                                logging.debug(f"Destination DB Info: {get_db_url()['source']}")
                                        logging.debug(f">>OUT>> Dataframe is:\n {df}")
                                else:
                                        logging.debug(f"Dataframe has no records.")


if __name__ == "__main__":
        create_and_push_to_db()
