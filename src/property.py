"""
   @Create Author: Luka
   @Create Date: 2023-12-11 10:32:23
   @Last Modified by:   Luka
   @Last Modified time: 2023-12-11 10:32:23
"""


"""
    Property is the class for experiment data, which possess method name and value for method.
"""

class Property:
    def __init__(self, method, value) -> None:
        self.method = method  # experiment method name
        self.value = value  # experiment value