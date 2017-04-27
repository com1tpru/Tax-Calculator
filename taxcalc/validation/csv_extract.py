"""
Tax-Calculator validation script that extracts non-zero input variables for
the filing unit with specified RECID in specified CSV-formated file.
"""
# CODING-STYLE CHECKS:
# pep8 --ignore=E402 csv_extract.py
# pylint --disable=locally-disabled csv_extract.py

import argparse
import sys
import os
import numpy as np
import pandas as pd
from taxcalc import Records


def main(filename, recid, input_vars_only):
    """
    Contains high-level logic of the script.
    """
    # read all file content into Pandas DataFrame
    adf = pd.read_csv(filename)
    adf_vars = set(adf.columns)

    # check that both files contain required tax variables
    required_input_vars = set(['RECID', 'MARS'])
    required_input_vars_str = 'RECID, MARS'
    if not required_input_vars.issubset(adf_vars):
        msg = 'ERROR: FILE does not include required input variables: {}\n'
        sys.stderr.write(msg.format(required_input_vars_str))
        return 1

    # check that RECID actually identifies a filing unit in FILE
    if not recid in adf['RECID'].values:
        msg = 'ERROR: RECID={} not in FILE\n'
        sys.stderr.write(msg.format(recid))
        return 1

    # extract the adf row with specified recid
    edf = adf[adf['RECID'] == recid]
    edf.is_copy = False

    # optionally remove all but Tax-Calculator usable input variables from edf
    if input_vars_only:
        Records.read_var_info()
        for colname in edf.columns:
            if colname not in Records.USABLE_READ_VARS:
                edf.drop(colname, axis=1, inplace=True)

    # remove all zero-valued variables from edf
    for colname in edf.columns:
        if edf[colname].iloc[0] == 0:
            edf.drop(colname, axis=1, inplace=True)

    # write edf to stdout in CSV format with column names in sorted order
    ofilename = '{}-{}.csv'.format(filename[:-4], recid)
    out = edf.to_csv(path_or_buf=ofilename, columns=sorted(edf.columns),
                     index=False, float_format='%.2f')
    sys.stdout.write('EXTRACT in {}\n'.format(ofilename))

    # normal return code
    return 0
# end of main function code


if __name__ == '__main__':
    # parse command-line arguments:
    PARSER = argparse.ArgumentParser(
        prog='python csv_extract.py',
        description=('Writes CSV-formatted file that contains all non-zero '
                     'variables from CSV-formatted FILE for row with RECID.'))
    PARSER.add_argument('FILE', type=str, default='',
                        help=('Name of file, which must end with ".csv".'))
    PARSER.add_argument('RECID', type=int, default=0,
                        help=('RECID value of filing unit row to extract.'))
    PARSER.add_argument('--inputonly', default=False, action='store_true',
                        help=('optional flag that excludes variables that '
                              'are not Tax-Calculator usable input.'))
    ARGS = PARSER.parse_args()
    # check for invalid command-line argument values
    ARGS_ERROR = False
    if ARGS.FILE == '':
        sys.stderr.write('ERROR: FILE must be specified\n')
        ARGS_ERROR = True
    if not os.path.isfile(ARGS.FILE):
        MSG = 'ERROR: FILE [{}] does not exist\n'
        sys.stderr.write(MSG.format(ARGS.FILE))
        ARGS_ERROR = True
    if not ARGS.FILE.endswith('.csv'):
        MSG = 'ERROR: FILE [{}] does not end with ".csv"\n'
        sys.stderr.write(MSG.format(ARGS.FILE))
        ARGS_ERROR = True
    if ARGS.RECID <= 0:
        MSG = 'ERROR: RECID [{}] must be positive\n'
        sys.stderr.write(MSG.format(ARGS.RECID))
        ARGS_ERROR = True
    if ARGS_ERROR:
        sys.stderr.write('USAGE: python csv_extract.py --help\n')
        RCODE = 1
    else:
        RCODE = main(ARGS.FILE, ARGS.RECID, ARGS.inputonly)
    sys.exit(RCODE)
