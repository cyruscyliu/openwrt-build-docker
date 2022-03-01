import os
import json
import random

from multiprocessing import Pool


#
# dump
#

def dump_obj(obj, label, dumpto):
    print('[+] dump %s to %s' % (label, dumpto))
    with open(dumpto, 'w') as f:
        f.write(json.dumps(obj))


#
# multiprocessing
#

def chunks(lst):
    """Yield successive n-sized chunks from lst."""
    para = os.cpu_count()
    n = (len(lst) + para - 1) // para

    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def loop_wrapper(several_args):
    several_rslts = []

    for do_func, args in several_args:
        several_rslts.append(do_func(args))

    return several_rslts

def do_in_parallel(do_func, all_args, rslt_handle, debug=False, para=None):
    task_num = len(all_args)
    if task_num == 0:
        return

    # prepare wrapper args
    wrapper_args = [(do_func, args) for args in all_args]
    random.shuffle(wrapper_args)

    # chunkize the task, for parallel equally
    chunk_args = []
    for chunk in chunks(wrapper_args):
        chunk_args.append(chunk)

    # do tasks in parallel
    if para == None:
        para = os.cpu_count()
    if debug:
        para = 1
    if task_num < para:
        para = task_num

    with Pool(para) as pool:
        rslt_list = []

        chunk_rslt_list = pool.imap_unordered(loop_wrapper, chunk_args)
        for chunk_rslt in chunk_rslt_list:
            rslt_list.extend(chunk_rslt)

        rslt_handle(rslt_list)
