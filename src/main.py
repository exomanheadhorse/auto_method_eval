from typing import List, Dict
import common
from compound import Compound
from enum_file import Properties


# class EvaluateHandler:
#     def __init__(self) -> None:
#         self.db_ins = common.get_db_hander('compounds')
#         self.id_2_name: Dict[str, str] = dict()
#         self.id_2_compounds: Dict[str, Compound] = dict()

#     def load_data(self):
#         pass

#     def get_ref_data(self):
#         # return two dict, ct and cp
#         pass

#     def get_exp_data(self):
#         # return one dict
#         pass
    

# class SingleEvaluateHandler:
#     def __init__(self) -> None:
#         self.db_ins = common.get_db_hander('compounds')
    
#     def eval_via_name(self, compound_name):
#         pass

#     def eval_via_id(self, compound_id):
#         pass

#     def get_ref_data(self, id):
#         pass


class BatchEvaluateHandler:
    def __init__(self) -> None:
        self.db_ins = common.get_db_hander('compounds')
        self.id_2_name: Dict[str, str] = dict()
        self.id_2_compounds: Dict[str, Compound] = dict()


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
            data.append(item['mol_id'])
        self.eval_via_id_list(id_list)


    def eval_via_id_list(self, compounds_id_list: List[int]):
        params = dict()
        ref_data = self.get_ref_data(compounds_id_list)
        exp_data_p = self.get_experiment_data(compounds_id_list, Properties.critical_pressure.value)
        exp_data_t = self.get_experiment_data(compounds_id_list, Properties.critical_temperature.value)
        for id in compounds_id_list:
            if id not in ref_data:
                print(f'{id} does not has data in ref data!')
                # raise Exception(f'{id} does not exist in db!')
            else:
                pass # fill into params

            if id not in exp_data_p:
                print(f'{id} not exist in critical_pressure exp data')
                raise Exception()
            else:
                pass

            if id not in exp_data_t:
                print(f'{id} not exist in critical_temperature data')
            else:
                pass


    def get_ref_data(self, id_list: List[int]):
        sql = f'''
            SELECT * FROM compound_basic_properties
            WHERE mol_id in ({",".join(id_list)})
        '''
        data = self.db_ins.query(sql)
        input_data: Dict[str: dict] = dict()
        for item in data:
            input_data.setdefault(item['mol_id'], item)
        return input_data


    def get_experiment_data(self, id_list: List[int], table_name):
        sql = f'''
            SELECT * FROM {table_name}
            WHERE mol_id in ({",".join(id_list)})
        '''
        data = self.db_ins.query(sql)
        input_data: Dict[str: dict] = dict()
        for item in data:
            input_data.setdefault(item['mol_id'], item)
        return input_data


if __name__=='__main__':
    # c_list = ['2-methyl-1,3-dithiolane', '(3S)-thiolane-3-thiol']
    # x = EvaluateHandler()
    # x.eval_via_name(c_list)
    import enum_file
    print(enum_file.Properties.critical_pressure.value)