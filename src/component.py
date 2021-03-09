'''
Template Component main class.

'''

import logging
import os
import sys
import csv
from pathlib import Path

from kbc.env_handler import KBCEnvHandler

DEFAULT_TABLE_INPUT = "/data/in/tables/"
DEFAULT_FILE_INPUT = "/data/in/files/"

DEFAULT_FILE_DESTINATION = "/data/out/files/"
DEFAULT_TABLE_DESTINATION = "/data/out/tables/"
# configuration variables
KEY_API_TOKEN = '#api_token'
KEY_PRINT_HELLO = 'print_hello'

# #### Keep for debug
KEY_DEBUG = 'debug'

# list of mandatory parameters => if some is missing, component will fail with readable message on initialization.
MANDATORY_PARS = []
MANDATORY_IMAGE_PARS = []

APP_VERSION = '0.0.1'


class Component(KBCEnvHandler):

    def __init__(self, debug=False):
        # for easier local project setup
        default_data_dir = Path(__file__).resolve().parent.parent.joinpath('data').as_posix() \
            if not os.environ.get('KBC_DATADIR') else None

        KBCEnvHandler.__init__(self, MANDATORY_PARS, log_level=logging.DEBUG if debug else logging.INFO,
                               data_path=default_data_dir)
        # override debug from config
        if self.cfg_params.get(KEY_DEBUG):
            debug = True
        if debug:
            logging.getLogger().setLevel(logging.DEBUG)
        logging.info('Running version %s', APP_VERSION)
        logging.info('Loading configuration...')

        try:
            # validation of mandatory parameters. Produces ValueError
            self.validate_config(MANDATORY_PARS)
            self.validate_image_parameters(MANDATORY_IMAGE_PARS)
        except ValueError as e:
            logging.exception(e)
            exit(1)
        # ####### EXAMPLE TO REMOVE
        #         # intialize instance parameteres
        #
        #         # ####### EXAMPLE TO REMOVE END

    def run(self):
        '''
        Main execution code
        '''
        source_file_path = DEFAULT_TABLE_INPUT + 'properties.csv'
        logging.info(source_file_path)

        result_file_path = DEFAULT_TABLE_DESTINATION + 'properties_id.csv'
        logging.info(result_file_path)

        with open(source_file_path, 'r') as input, open(result_file_path, 'w+', newline='') as out:
            reader = csv.DictReader(input)
            new_columns = reader.fieldnames

            new_columns.append('row_number')
            writer = csv.DictWriter(out, fieldnames=new_columns, lineterminator='\n', delimiter=',')
            writer.writeheader()
            for index, l in enumerate(reader):
                # if param_print_lines:
                # print(f'Printing line {index}: {l}')
                l['row_number'] = index
                writer.writerow(l)
        print('done')


"""
        Main entrypoint
"""
if __name__ == "__main__":
    if len(sys.argv) > 1:
        debug_arg = sys.argv[1]
    else:
        debug_arg = False
    try:
        comp = Component(debug_arg)
        comp.run()
    except Exception as exc:
        logging.exception(exc)
        exit(1)
