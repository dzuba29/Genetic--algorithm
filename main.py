from itertools import accumulate, islice, product
from random import choice, sample, randint

import numpy as np


def random_genotype(size):
    list_gentp = []
    for i in range(size):
        temp = np.zeros((size, size))
        idxs = list(range(size))
        for row in temp:
            item = choice(idxs)
            row[item] = 1
            idxs.remove(item)
        list_gentp.append(temp)
    return list_gentp


def elementwise_mult(array, list_gentp):
    fitness = []
    for item in list_gentp:
        el_wise_sum = np.sum(np.multiply(array, item))
        fitness.append(el_wise_sum)
    return fitness


def avrg(lst):
    avrg = [0]
    sum_fitness = sum(lst)
    for item in lst:
        avrg.append(item/sum_fitness)
    return avrg


def proc_avrg(lst):
    return list(map(lambda x: x * 100, lst))


def check_intervals(lst):
    bin_intervals = [lst[i:i+2] for i in range(0, len(lst)-1, 1)]
    approved_intervals = []
    for item in range(len(lst)-1):
        rand_num = np.random.uniform(0, 100)
        for idx, item in enumerate(bin_intervals):
            if rand_num >= item[0] and rand_num <= item[1]:
                approved_intervals.append(idx)
    return approved_intervals

def crossover(tupl,list_gentp):
    kids = []
    for idx,item in enumerate(tupl):
        mom = list_gentp[item[0]]
        dad = list_gentp[item[1]]
        m_idx, d_idx =  np.where(mom[idx] == 1)[0][0],np.where(dad[idx] == 1)[0][0]
        kids.append(min(m_idx, d_idx + randint(0, abs(m_idx-d_idx))))
    return kids


if __name__ == "__main__":
    array = np.array(
        [
            [100, 150, 90, 200],
            [200, 100, 70, 150],
            [250, 80,  70, 100],
            [190, 100, 120, 200]
        ]
    )
    list_gentp = random_genotype(array.shape[0])
    print(len(list_gentp))

    fitness = elementwise_mult(array, list_gentp)
    print(fitness)

    avrg_fitness = sum(fitness)/array.shape[0]
    print(avrg_fitness)

    total_avrg = avrg(fitness)
    print(total_avrg)

    proc_avrg = proc_avrg(total_avrg)
    print(proc_avrg)

    intervals = list(accumulate(proc_avrg))
    print(intervals)

    approved_int = check_intervals(intervals)
    print(approved_int)

    set_parent_pair = list(product(approved_int, approved_int))
    print(set_parent_pair)

    random_parents = sample(set_parent_pair, array.shape[0])
    print(random_parents)

    crossover(random_parents,list_gentp)