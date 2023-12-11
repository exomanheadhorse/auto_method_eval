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
        self.evaluate()
        # add other properties here
        # self.density = args['density']
    
    def evaluate(self):
        self.resort()
#        print('before sort...')
#        for item in self.critical_temperature_eval_list:
#            print(item.method, item.value, self.sort_method(item.value, self.critical_temperature))
#        self.resort_critical_temperature()
#        print('after sort......')
#        for item in self.critical_temperature_eval_list:
#            print(item.method, item.value, self.sort_method(item.value, self.critical_temperature))

    def resort(self):
        self.resort_critical_pressure()
        self.resort_critical_temperature()

    def resort_critical_temperature(self):
        self.critical_temperature_eval_list.sort(key=lambda x: self.cal_deviation(x.value, self.critical_temperature))

    def resort_critical_pressure(self):
        self.critical_pressure_eval_list.sort(key=lambda x: self.cal_deviation(x.value, self.critical_pressure))

    def cal_deviation(self, exp_data, ref_data):
        return abs((exp_data - ref_data) / ref_data)

    def print_result(self):
        print('='*30)
        print(f'''formula={self.formula}, mol_id={self.mol_id}, iupac_name={self.name}:''')
        print(f''' Tc标准值：{str(self.critical_temperature)}''')
        print(f'''Tc推荐方法：{str(self.critical_temperature_eval_list[0].method)}, 数值为：{str(self.critical_temperature_eval_list[0].value)}''')
        self.print_sort_detail(self.critical_temperature_eval_list, self.critical_temperature)
        print(f'''Tp标准值：{str(self.critical_pressure)}''')
        print(f'''Tp推荐方法：{str(self.critical_pressure_eval_list[0].method)}, 数值为：{str(self.critical_pressure_eval_list[0].value)}''')
        self.print_sort_detail(self.critical_pressure_eval_list, self.critical_pressure)
        print('='*30)
    
    def print_sort_detail(self, iter_list: List[Property], ref_data):
        for item in iter_list:
            cur = f'''方法：{item.method}, 数值：{str(item.value)}, 误差：{'%.2f %%'%(self.cal_deviation(item.value, ref_data)*100)}'''
            # cur = f'''方法：{item.method}, 数值：{str(item.value)}, 误差：{'%.2f'%self.cal_deviation(item.value, ref_data)}'''
            print(cur)

    def output_result(self):
        pass