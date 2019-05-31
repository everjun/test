import random


def k_random(lst, k):
    if k < 0 or not isinstance(k, int):
        raise Exception('k должно быть неотрицательным и целым')
    elif k == 0:
        return []
    elif k <= len(lst):
        s = set(lst)
        if k <= len(s):
            s = list(s)
            random.shuffle(s)
            return s[:k]
    raise Exception('Выбрать %i элементов невозможно' % k)
