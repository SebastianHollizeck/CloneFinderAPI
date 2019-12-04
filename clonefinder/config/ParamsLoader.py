from config.CloneFinderParams import CloneFinderParams
from parsers.ParamsParser import ParamsParser
import os.path
import sys
import argparse
from config.FormatInput import FormatInput

clone_finder_params = None  # used as a global instance of the params object


class ParamsLoader(object):
    """
        Loads command-line parameters and parses the options.ini file
    """

    def __init__(self, file):
        global clone_finder_params
        self._params_file = file

    @property
    def params_file(self):
        return self._params_file

    @params_file.setter
    def params_file(self, value):
        self._params_file = value

    # this does the heavy lifting:  parsing the ini file and then reading from command line
    def load_params(self):

        parser = ParamsParser()
        adjust_format = FormatInput()

        if not os.path.exists(self._params_file):
            raise Exception("The required config.ini file is missing.")

        # now that we know the file exists, we can parse it
        result = parser.parse_config_file(self._params_file)

        # get to the commandline parsing
        parser = argparse.ArgumentParser()
        parser.add_argument(
            "data", help="Data type to analyse (currently only supports snv)"
        )
        parser.add_argument("input", help="input file of variants (tab seperated file)")
        parser.add_argument(
            "-o", "--output", help="Output folder to write final files to", default="./"
        )

        args = parser.parse_args()

        if args.data == "snv":
            result.data_format = args.data
            result.snv_data_file = args.input
            result.cnv_data_file = args.input[:-4] + "snv-CNV.txt"
            adjust_format.snv2snv(result.snv_data_file, "withCNVfile")
            result.input_data_file = args.input[:-4] + "snv.txt"
        else:
            raise EnvironmentError(
                "the command should be python CloneFinder.py snv [input]\npython CloneFinder.py "
            )

        result.input_id = os.path.basename(sys.argv[2])[:-4] + args.data
        result.outputFolder = args.output

        clone_finder_params = result
        return clone_finder_params
