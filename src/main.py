from typing import List
import common
from compound import Compound


class EvaluateHandler:
    def __init__(self) -> None:
        self.db_ins = common.get_db_hander('compounds')


def eval_via_name(compounds_list: List[str]):
    db_ins = common.get_db_hander('compounds')
    sql = f'''SELECT id FROM compounds WHERE iupac_name IN ('{("','").join(compounds_list)}')'''
    data = db_ins.query(sql)
    id_list: List[int] = [x['id'] for x in data]
    eval_via_id(id_list)


def eval_via_id(compounds_list: List[int]):
    pass


def get_ref_data(id_list: List[int]):
    sql = f'''
        SELECT * FROM compounds
        WHERE id in ({",".join(id_list)})
    '''
    data = common.get_db_hander('compounds').query(sql)
    input_data = dict()
    pass


def get_experiment_data():
    pass


if __name__=='__main__':
    c_list = ['2-methyl-1,3-dithiolane', '(3S)-thiolane-3-thiol']
    eval_via_name(c_list)