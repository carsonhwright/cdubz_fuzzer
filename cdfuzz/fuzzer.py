from builtins import callable
import random
# TODO this inspect stuff proposes some interesting stuff, I need to look into this more
import inspect
# TODO traceback is certainly going to be necessary
import traceback
import logging
from pathlib import Path

from test_objects.test_me import main as tme
from fuzz_logger import FuzzLogger
from utils import Perturbator



ITER_SIZE = 10
TRACE_LEN = 10
INT_MAX = 2**100 - 1
LOG_FP = "wungus.log"

def fuzz_int(fuzz_range: tuple=(-INT_MAX, INT_MAX)):
    get_rand = lambda x, y: [random.randint(x, y) for i in range(ITER_SIZE)] 
    return get_rand(*fuzz_range)

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
        new_args.append(arg())
    new_args = tuple(new_args)

    perturb = Perturbator(*new_args)
    for inst in perturb:
        try:
            func(*inst)
        except Exception as e:
            breakpoint()
            logger.info(f"Logged!: {e}\n TRACE:\n{traceback.format_exc(TRACE_LEN)}")

if __name__ == "__main__":
    main(tme, fuzz_int, fuzz_int)