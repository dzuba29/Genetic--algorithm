from itertools import (accumulate, combinations_with_replacement, islice,
                       product)
from random import choice, choices, randint, sample

import numpy as np


def random_genotype(arr_size, num_gen):
    """[summary]

    Arguments:
        arr_size {[int]} -- [rows and cols in one genotype]
        num_gen {[int]} -- [count of starting genotypes]

    Returns:
        [list] -- [list of genotypes]
    """
    list_gentp = []
    for _ in range(num_gen):
        temp = np.zeros((arr_size, arr_size))
        idxs = list(range(arr_size))
        for row in temp:
            item = choice(idxs)
            row[item] = 1
            idxs.remove(item)
        print(temp)
        list_gentp.append(temp)
    return list_gentp


def elementwise_mult(array, list_gentp):
    """[summary]

    Arguments:
        array {[ndarray]} -- [array of weights(cost)]
        list_gentp {[list]} -- [count of genotypes]

    Returns:
        [list] -- [list of fitness for every genotype]
    """
    fitness = []
    for item in list_gentp:
        el_wise_sum = np.sum(np.multiply(array, item))
        fitness.append(el_wise_sum)
    return fitness


def avrg(lst):
    """[summary]

    Arguments:
        lst {[list]} -- [fitness]

    Returns:
        [list] -- [list of avrg fitness]
    """
    avrg = [0]
    sum_fitness = sum(lst)
    for item in lst:
        avrg.append(item/sum_fitness)
    return avrg


def proc_avrgs(lst):
    """[summary]

    Arguments:
        lst {[list]} -- [list of avrg fitness]

    Returns:
        [list] -- [mult every el by 100 in avrg fitness]
    """
    return list(map(lambda x: x * 100, lst))


def crossover(tupl, list_gentp):
    """[summary]

    Arguments:
        tupl {[tuple]} -- [idxs of mom and dad as tuple]
        list_gentp {[list]} -- [all genotypes]

    Returns:
        [list] -- [list of index(1) in childs genotypes]
    """
    kids = []
    for item in tupl:
        mom = list_gentp[item[0]]
        dad = list_gentp[item[1]]
        kid = []
        for idx in range(mom.shape[0]):
            m_idx, d_idx = np.where(mom[idx] == 1)[
                0][0], np.where(dad[idx] == 1)[0][0]
            kid.append(min(m_idx, d_idx + randint(0, abs(m_idx-d_idx))))
        kids.append(kid)
    return kids


def check_intervals(lst):
    """[summary]

    Arguments:
        lst {[list]} -- [list of intervals]

    Returns:
        [list] -- [approved intervals by condition]
    """
    bin_intervals = [lst[i:i+2] for i in range(0, len(lst)-1, 1)]
    approved_intervals = []
    for item in range(len(lst)-1):
        rand_num = np.random.uniform(0, 100)
        for idx, item in enumerate(bin_intervals):
            if rand_num >= item[0] and rand_num <= item[1]:
                approved_intervals.append(idx)
    return approved_intervals


def mutation(kids_idx):
    """[summary]
    
    Arguments:
        kids_idx {[list of tuples]} -- [idxs of childs genotypes]
    
    Returns:
        [ndarray] -- [return shifted genotype of kid]
    """
    phenotype = np.zeros((len(kids_idx), len(kids_idx)))
    for idx, item in enumerate(kids_idx):
        phenotype[idx, item] = 1
    temp = []
    for i in range(0, phenotype.shape[0]):
        for j in range(0, phenotype.shape[0]):
            if phenotype[i][j] == 1:
                k = j
                if k in temp:
                    while(k in temp):
                        k = (k + 1) % phenotype.shape[0]
                    phenotype[i][j] = 0
                    phenotype[i][k] = 1
                temp.append(k)
                break
    return phenotype


def epoch(array, list_gentp):
    """[summary]
    
    Arguments:
        array {[ndarry]} -- [our matrix of weights(costs)]
        list_gentp {[list]} -- [list of genotypes]
    
    Returns:
        [list] -- [list of kids]
    """
    checkd_kids = []
    fitness = elementwise_mult(array, list_gentp)
    avrg_fitness = sum(fitness)/len(list_gentp)
    total_avrg = avrg(fitness)
    proc_avrg = proc_avrgs(total_avrg)
    intervals = list(accumulate(proc_avrg))
    approved_int = check_intervals(intervals)

    set_parent_pair = list(combinations_with_replacement(approved_int, 2))
    set_parent_pair = list(
        set(list(map(lambda x: tuple(sorted(x)), set_parent_pair))))
    print(set_parent_pair)

    random_parents = []
    if len(set_parent_pair) != 1:
        random_parents_id = np.random.randint(
            0, len(set_parent_pair) - 1, len(list_gentp))
    else:
        random_parents_id = [0 for _ in range(len(set_parent_pair))]

    for i in random_parents_id:
        random_parents.append(set_parent_pair[i])

    kids = crossover(random_parents, list_gentp)

    for i in range(len(list_gentp)):
        checkd_kids.append(mutation(kids[i]))

    return checkd_kids


def main(array, num_gen):
    """[summary]
    
    Arguments:
        array {[ndarry]} -- [our matrix of weights(costs)]
        num_gen {[int]} -- [size of generation genotypes]
    """
    list_gentp = random_genotype(array.shape[0], num_gen)
    fitness = elementwise_mult(array, list_gentp)
    y0 = sum(fitness)/len(list_gentp)

    for i in range(30):
        list_gentp = epoch(array, list_gentp)
        fitness = elementwise_mult(array, list_gentp)
        y1 = sum(fitness)/len(list_gentp)

        if abs(y0-y1) == 0:
            break
        y0 = y1
        print(max(elementwise_mult(array, list_gentp)))


if __name__ == "__main__":
    array = np.array(
        [
            [100, 150, 90, 200],
            [200, 100, 70, 150],
            [250, 80,  70, 100],
            [190, 100, 120, 200]
        ]
    )

    main(array, 24)

