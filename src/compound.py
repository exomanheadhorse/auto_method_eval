import common
from property import Property
from typing import List


class Compound:
    def __init__(self, args) -> None:
        self.mol_id = args['mol_id']
        self.formula = args['formula']
        self.name = args['name']
        self.critical_temperature = args['critical_temperature']
        self.critical_temperature_eval_list: List[Property] = args['critical_temperature_eval_list']
        self.critical_pressure: float = args['critical_pressure']
        self.critical_pressure_eval_list: List[Property] = args['critical_pressure_eval_list']
        # add other properties here
        # self.density = args['density']
    
    def evaluate(self):
        pass

    def resort(self):
        pass