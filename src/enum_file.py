"""
   @Create Author: Luka
   @Create Date: 2023-12-11 10:30:02
   @Last Modified by:   Luka
   @Last Modified time: 2023-12-11 10:30:02
"""


"""
    Properties is the enum class for experimental data type, and the value refers to the table name in mysqlDB.
    For example, the table name in mysqlDB for critical_temperature is 'critical_temperature_exp_data'.
"""

from enum import Enum


class Properties(Enum):
    critical_temperature = 'critical_temperature_exp_data'
    critical_pressure = 'critical_pressure_exp_data'