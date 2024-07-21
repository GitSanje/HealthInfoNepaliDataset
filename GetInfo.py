
import utils

class GetHealthInfo:
    def __init__(self, sections, csvfile=None) -> None:
        self.sections = sections
        self.nested_dict = utils.nested_defaultdict()
        self.csvfile = csvfile or "health_info_nepali.csv"
        
    def getDict(self):
        nested_dict = utils.extract_health_info(self.sections, self.nested_dict)
        flat_dict = utils.flatten_dict(nested_dict)
        self.csvfile = utils.convert_to_csv(flat_dict, self.csvfile)
        return self.csvfile
        