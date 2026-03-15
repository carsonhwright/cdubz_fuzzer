from builtins import callable
import string
import json
import random
# TODO this inspect stuff proposes some interesting stuff, I need to look into this more
import inspect
# TODO traceback is certainly going to be necessary
import traceback
import logging
from pathlib import Path

from test_objects.test_me import main as tme
from fuzz_logger import FuzzLogger
from utils import Permutator


ITER_SIZE = 10
TRACE_LEN = 10
INT_MAX = 2**100 - 1
LOG_FP = "wungus.log"

with open(Path("cdfuzz/config/configs.json"), 'r') as f:
    CONFIG_JSON = json.load(f)


def fuzz_int(fuzz_range: tuple=(-INT_MAX, INT_MAX), **kwargs):
    get_rand = lambda x, y: [random.randint(x, y) for i in range(ITER_SIZE)] 
    return get_rand(*fuzz_range)

def fuzz_str(max_str_len: int, min_str_len: int, delim_range: int, std_dev: float, **kwargs):
    """Makes up random strings, 
    TODO need to figure out how to let `main`'s `new_args.append(arg())` make this work, failing on missing params error

    :param max_str_len: the longest a string is allowed to be
    :param min_str_len: the smallest a string is allowed to be
    :param delim_range: number of delimiters that should exist in the
            string, somewhat equivalent to how many words there should 
            be in the string
    :param std_dev: standard deviation for randomized number of 
            delimiters, if not provided, will be 0 and therefore will 
            stick to given param `delim_range`
    
    """
    # these will be used to separate 
    delims = [" ", "  ", ",", "|", ";", "\"", "/"]
    char_set = string.printable
    max_char = len(char_set)
    ret = []
    for _ in range(32):
        # TODO something with min/max str len being randomized, set to 
        # range being iter'd below
        next_str = ""
        for _i in range(max_str_len):
            # TODO do something with delims
            next_str += char_set[random.randint(0, max_char-1)]
        ret.append(next_str)
    return tuple(ret)




def main(func: callable = print, *args, **kwargs):

    # TODO iterations over the range of test values as well as 
    # perturbations needs to be added

    # TODO how are edge cases to be considered? We've implemented 
    # random, but are we going to include things like -2^32 + 1, 0, -1,
    # 2^32-1?
    new_args = []
    
    logger = logging.getLogger(__name__)
    if Path(LOG_FP).exists():
        with open(LOG_FP, "w") as f:
            f.write("")
    logging.basicConfig(filename="wungus.log", level=logging.INFO)

    for arg in args:
        # TODO how can this be expanded and included?
        sig = inspect.signature(arg)
        if not callable(arg):
            raise TypeError(f"Passed an argument: {arg} which was " \
                            "not callable")
        
        new_args.append(arg(**CONFIG_JSON.get(arg.__name__)))
    new_args = tuple(new_args)

    perturb = Permutator(*new_args)
    for inst in perturb:
        try:
            func(*inst)
        except Exception as e:
            breakpoint()
            logger.info(f"Logged!: {e}\n TRACE:\n{traceback.format_exc(TRACE_LEN)}")

if __name__ == "__main__":
    main(tme, fuzz_int, fuzz_int, fuzz_str)