from builtins import callable
import random
# TODO this inspect stuff proposes some interesting stuff, I need to look into this more
import inspect
# TODO traceback is certainly going to be necessary
import traceback

from test_objects.test_me import main as tme
from fuzz_logger import FuzzLogger



ITER_SIZE = 10
INT_MAX = 2**100 - 1

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
    
    # TODO this is throwing missing argument errors __name__ or something
    # logger = FuzzLogger("Wunk")

    for arg in args:
        # TODO how can this be expanded and included?
        sig = inspect.signature(arg)
        breakpoint()
        if not callable(arg):
            raise TypeError(f"Passed an argument: {arg} which was " \
                            "not callable")
        new_args.append(arg())
    new_args = tuple(new_args)
    try:
        # here the iterator/perturbator needs to be
        func(*new_args)
    except Exception as e:
        print(f"Do logging, exception was {e} see traceback: "\
              f"{traceback.print_exc()}")
        # logger.warning(f"Logged!: {e}")
    breakpoint()

if __name__ == "__main__":
    main(tme, fuzz_int)