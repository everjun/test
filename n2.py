from multiprocessing import Process, Manager, Queue


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


def task_b_for_day(lst, q):
    last_dt = lst[0][0].date()
    day_list = []
    avg_sum = 0
    avg_count = 0
    for tm, val in lst:
        avg_sum += val
        avg_count += 1
        insert_by_sorted_value(day_list, val)
    q.put((last_dt, day_list[0], day_list[-1], avg_sum / avg_count,
           get_median_from_sorted_list(day_list, avg_count)))


def task_b(lst):
    last_dt = None
    manager = Manager()
    new_list = manager.list([])
    q = Queue()
    procs = []
    last_index = 0
    for i, (tm, val) in enumerate(lst):
        if last_dt is None:
            last_dt = tm.date()
        elif last_dt != tm.date():
            last_dt = tm.date()
            proc = Process(target=task_b_for_day, args=(lst[last_index:i], q))
            proc.start()
            procs.append(proc)
            last_index = i
    proc = Process(target=task_b_for_day, args=(lst[last_index:], q))
    proc.start()
    procs.append(proc)
    for proc in procs:
        proc.join()
    while not q.empty():
        new_list.append(q.get())
    return new_list


if __name__ == '__main__':
    import random
    from datetime import datetime, timedelta

    l = [(datetime(2019, 1, 1) + timedelta(seconds=k), k % 50) for k in range(1000)]
    with open('initial_a.txt', 'w') as f:
        f.write("time    value\n")
        for time, value in l:
            f.write("%s %s\n" % (time.strftime('%Y-%m-%d %H:%M:%S'), value))
    with open('result_a.txt', 'w') as f:
        f.write("time    value    min    max    avg    median\n")
        for time, value, mn, mx, avg, median in task_a(l):
            f.write("%s %s %s %s %s %s\n" % (time.strftime('%Y-%m-%d %H:%M:%S'), value, mn, mx, avg, median))
    l = [(datetime(2019, 1, 1) + timedelta(seconds=k), k % 50) for k in range(60 * 60)]
    l += [(datetime(2019, 1, 2) + timedelta(seconds=k), k % 40) for k in range(60 * 60)]
    l += [(datetime(2019, 1, 3) + timedelta(seconds=k), k % 60) for k in range(60 * 60)]
    with open('initial_b.txt', 'w') as f:
        f.write("time    value\n")
        for time, value in l:
            f.write("%s %s\n" % (time.strftime('%Y-%m-%d %H:%M:%S'), value))
    with open('result_b.txt', 'w') as f:
        f.write("time    min    max    avg    median\n")
        print('start counting task b')
        for time, mn, mx, avg, median in task_b(l):
            f.write("%s %s %s %s %s\n" % (time.strftime('%Y-%m-%d'), mn, mx, avg, median))
        print('end counting task b')
