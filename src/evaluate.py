"""
   @Create Author: Luka
   @Create Date: 2023-12-11 10:30:06
   @Last Modified by:   Luka
   @Last Modified time: 2023-12-11 10:30:06
"""


"""
    Evaluate is the entrance of this system. 
"""

from typing import List, Dict
import common
from compound import Compound
from enum_file import Properties
from property import Property



"""
    BatchEvaluateHandler is the class for experimental method evaluation of compounds batchly.
    The class provide two method: evaluate via name list, evalute via id list(the id is mol_id in mol-instincts system)
"""


class BatchEvaluateHandler:
    def __init__(self) -> None:
        self.db_ins = common.get_db_hander('compounds')  # db handler
        self.id_2_name: Dict[str, str] = dict()  # mol_id->iupac_name
        self.id_2_compounds: Dict[str, Compound] = dict()  #mol_id->compounds obj


    def eval_via_name_list(self, compounds_list: List[str]):
        sql = f'''
                    SELECT mol_id, iupac_name 
                    FROM compounds_name_info WHERE iupac_name 
                    IN ('{("','").join(compounds_list)}')
               '''
        data = self.db_ins.query(sql)
        id_list: List[int] = list()
        for item in data:
            self.id_2_name.setdefault(item['mol_id'], item['iupac_name'])
            id_list.append(item['mol_id'])
        self.eval_via_id_list(id_list)


    def eval_via_id_list(self, compounds_id_list: List[int]):
        params = dict()
        ref_data = self.get_ref_data(compounds_id_list)
        exp_data_p = self.get_experiment_data(compounds_id_list, Properties.critical_pressure.value)
        exp_data_t = self.get_experiment_data(compounds_id_list, Properties.critical_temperature.value)
        for id in compounds_id_list:
            args = dict()
            if id not in ref_data: # decide id whether in reference data or not
                print(f'{id} does not has data in ref data!')
                # raise Exception(f'{id} does not exist in db!')
            else:
                args['mol_id'] = id
                args['formula'] = ref_data[id]['formula']
                args['name'] = ref_data[id]['iupac_name']
                args['critical_temperature'] = ref_data[id]['critical_temperature']
                args['critical_pressure'] = ref_data[id]['critical_pressure']

            if id not in exp_data_p:  # decide id whether in experental data or not
                print(f'{id} not exist in critical_pressure exp data')
                raise Exception(f'{id} not exist in critical_pressure exp data')
            else:
                cur = []
                for method, value in exp_data_p[id].items():
                    cur.append(Property(method, value))
                args['critical_pressure_eval_list'] = cur

            if id not in exp_data_t:  # decide id whether in eexperental data or not
                print(f'{id} not exist in critical_temperature data')
                raise Exception(f'{id} not exist in critical_temperature data')
            else:
                cur = []
                for method, value in exp_data_t[id].items():
                    cur.append(Property(method, value))
                args['critical_temperature_eval_list'] = cur
            # print(args)
            params.setdefault(id, Compound(args=args))
        print(len(params))

        # print output result into terminal
        for _, item in params.items():
            item.print_result()



    def get_ref_data(self, id_list: List[int]):
        sql = f'''
            SELECT a.mol_id, a.critical_temperature, a.critical_pressure, 
            b.iupac_name, b.formula FROM compounds_basic_properties a 
            LEFT JOIN compounds_name_info b 
            ON a.mol_id = b.mol_id
            WHERE a.mol_id IN ('{"','".join(id_list)}')
        '''
        print(sql)
        data = self.db_ins.query(sql)
        input_data: Dict[str: dict] = dict()
        for item in data:
            input_data.setdefault(item['mol_id'], item)
        return input_data


    def get_experiment_data(self, id_list: List[int], table_name):
        sql = f'''
            SELECT * FROM {table_name}
            WHERE mol_id in ('{"','".join(id_list)}')
        '''
        data = self.db_ins.query(sql)
        input_data: Dict[str: dict] = dict()
        for item in data:
            cur = dict()
            for k, v in item.items():
                if k in ('id', 'mol_id'): # only read experiment values, ignore id and mol_id
                    continue
                cur.setdefault(k, v)
            input_data.setdefault(item['mol_id'], cur)
        return input_data


if __name__=='__main__':
    c_list = ['butanedithioic acid', '2-methyl-1,3-dithiolane', '(1S)-1-[(2R)-thiiran-2-yl]ethane-1-thiol', '(propylsulfanyl)carbothialdehyde']
    x = BatchEvaluateHandler()
    x.eval_via_name_list(c_list)
    # import enum_file
    # print(enum_file.Properties.critical_pressure.value)