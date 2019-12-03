from config.CloneFinderParams import CloneFinderParams
from parsers.ParamsParser import ParamsParser
import os.path
import sys
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

        Data = sys.argv[1]
        result.data_format = Data
        if Data == "snv":
            result.snv_data_file = sys.argv[2]
            result.cnv_data_file = sys.argv[2][:-4] + "snv-CNV.txt"
            adjust_format.snv2snv(result.snv_data_file, "withCNVfile")
            result.input_data_file = sys.argv[2][:-4] + "snv.txt"
        else:
            print(
                "the command should be python CloneFinder.py snv [input]\npython CloneFinder.py "
            )

        result.input_id = os.path.basename(sys.argv[2])[:-4] + Data
        if len(sys.argv) >= 4:
            result.outputFolder = sys.argv[3] + "/"
            if not os.access(outFolder, os.W_OK):
                outFolder = ""
                print(" outPutFolder", outFolder, " is not writable")

        clone_finder_params = result
        return clone_finder_params
