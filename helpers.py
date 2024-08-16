import json
from typing import List
class Helper:
    def load_testimonials(self)->List[dict]:
        with open('testimonials.json' , 'r') as file:
            return json.load(file)
    
    def load_plans(self)->List[dict]:
        with open("plans.json" , 'r') as file:
            return json.load(file)