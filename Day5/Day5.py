import numpy as np
from typing import Dict, Set, List
from numpy.typing import NDArray

def create_preconditions(rules: np.ndarray) -> Dict[int, Set[int]]:
    pres = rules[:,0]
    posts = rules[:,1]
    preconditions = {(int)(pre):set([v for p, v in rules if p == pre]) for pre in pres}
    return preconditions

def check_valid(preconditions: Dict[int, Set[int]], order: np.ndarray):
    items = []
    for i, element in enumerate(order):
        if preconditions.get(element, set()) & set(items):
            return False
        items.append(element)
    return True

def get_correct_orders_center_sum(preconditions: Dict[int, Set[int]], orders: List[np.ndarray]) -> int:
    center_sum = 0
    for order in orders:
        if check_valid(preconditions, order):
            #print(order)
            center_sum += order[order.size//2]
            
    return center_sum
    
def fix_order(preconditions: Dict[int, Set[int]], order: np.ndarray) -> np.ndarray:
    fixed_order = order
    items = []
    i = 0
    while i < order.size:
        element = fixed_order[i]
        broken_conditions = preconditions.get(element, set()) & set(items)
        items.append(element)
        if broken_conditions:
            for j, subelement in enumerate(fixed_order[:i]):
                if subelement in broken_conditions:
                    print(fixed_order[:j], element , np.delete(fixed_order[j:], np.argwhere(fixed_order[j:]==element)))
                    fixed_order = np.concatenate([fixed_order[:j],[element] , np.delete(fixed_order[j:], np.argwhere(fixed_order[j:]==element))])
                    i = 0
                    items = []
                    break
        else:
            i+=1
    return fixed_order
                    
                    
if __name__=='__main__':
    with open("Day5/input.txt", "r") as f:
        da = np.array(f.read().splitlines())

    split_index = np.where(da=='')[0][0]
    rules,_, order = np.array_split(da, [split_index,split_index+1])
    
    rules = np.array([[(int)(n) for n in rule.split('|')] for rule in rules])
    
    preconditions = create_preconditions(rules)
    
    orders = [np.array(o.split(','), dtype=int) for o in order]    
    center_sum = get_correct_orders_center_sum(preconditions, orders)
    print(center_sum)
    
    fixed = fix_order(preconditions, orders[3])
    print(fixed)
    fixed_orders = [fix_order(preconditions, o) for o in orders if not check_valid(preconditions, o)]
    print(sum(o[o.size//2] for o in fixed_orders))
    
    #print([check_valid(preconditions, o) for o in orders])
    
    #print(preconditions)
    #print(order)
    #print(orders)
