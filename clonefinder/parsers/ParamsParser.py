from config.CloneFinderParams import CloneFinderParams
import configparser
import os.path


class ParamsParser(object):
    def __init__(self):
        self._messages = []

    @property
    def messages(self):
        return self._messages

    def parse_config_file(self, config_file):
        if not os.path.exists(config_file):
            IOError("input config file not found")
        parser = configparser.RawConfigParser()

        try:
            print("loading config file: " + config_file)
            params = CloneFinderParams()
            parser.read(config_file)
            params.freq_cutoff = parser.getfloat("parameters", "FreqCutoff")
            params.total_read_cut = parser.getint(
                "parameters", "Total_Read_Count_CutOff"
            )
            params.mutant_read_cut = parser.getint(
                "parameters", "Mutant_Read_Count_CutOff"
            )
            return params
        except Exception as e:
            print(str(e))
            self._messages.append(str(e))
            return False
