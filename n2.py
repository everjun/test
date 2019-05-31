def insert_by_sorted_value(lst, val):
    i = 0
    while i < len(lst):
        if lst[i] > val:
            lst.insert(i, val)
            return
        i += 1
    lst.append(val)


def get_median_from_sorted_list(lst, length=None):
    if length is None:
        length = len(lst)
    median_index = length // 2
    if len(lst) == 1:
        return lst[0]
    elif length % 2 == 0:
        return (lst[median_index - 1] + lst[median_index]) / 2
    return lst[median_index]


def task_a(lst, row_counts=100):
    """

    :param lst: list of (tm, val)
    :param row_counts: window row counts, default 100
    :return: list of (tm, val, min, max, avg, median)
    """
    sorted_list = []
    non_sorted_list = []
    new_list = []
    avg = 0
    last_length = 0
    for tm, val in lst:
        insert_by_sorted_value(sorted_list, val)
        non_sorted_list.append(val)
        last_length += 1
        avg += val / last_length
        median = get_median_from_sorted_list(sorted_list, last_length)
        new_list.append((tm, val, sorted_list[0], sorted_list[-1], avg, median))
        if last_length == row_counts:
            el = non_sorted_list.pop(0)
            sorted_list.remove(el)
            avg -= el / row_counts
            last_length -= 1
        else:
            avg = sum(non_sorted_list) / (last_length + 1)
    return new_list


def task_b(lst):
    last_dt = None
    new_list = []
    day_list = []
    avg_sum = 0
    avg_count = 0
    for tm, val in lst:
        if last_dt is None:
            last_dt = tm.date()
        elif last_dt != tm.date():
            new_list.append((last_dt, day_list[0], day_list[-1], avg_sum / avg_count,
                             get_median_from_sorted_list(day_list, avg_count)))
            last_dt = tm.date()
            avg_sum = 0
            avg_count = 0
            day_list = []
        avg_sum += val
        avg_count += 1
        insert_by_sorted_value(day_list, val)
    new_list.append((last_dt, day_list[0], day_list[-1], avg_sum / avg_count,
                     get_median_from_sorted_list(day_list, avg_count)))
    return new_list
