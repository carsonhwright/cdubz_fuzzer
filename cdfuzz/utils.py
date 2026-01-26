class Perturbator():
    def __init__(self, *args, **kwargs):
        self.generate_args(*args)
    
    def __iter__(self):
        """this is going to require the use of get_next_digit
        """
        while True:
            if self.irreg_int.overflow:
                return
            out = self.get_args()
            yield out
            self.irreg_int += 1


    def generate_args(self, *args):
        """Create a perturbation object
        for example, given: ['a', 'b', 'c'], [1, 2]
        return:
        - [('a', 1), ('b', 1), ('c', 1), ('a', 2), ('b', 2), ('c', 2)]
        TODO problem for modularity, these need to be ordered which 
        would require that on the frontend that these arguments be 
        well-defined, assume the worst of the userbase
        """
        temp = []
        
        for arg in args:
            temp.append({"base": len(arg), "val": arg, "index": 0})
        # breakpoint()
        self.irreg_int = IrregularLittleEndianInt([x["base"] for x in temp])
        self.arg_array = temp
        self.max_val = 1
        for arg in self.arg_array:
            self.max_val *= len(arg)

    def get_args(self):
        """Each set of arguments is a 'digit' with a unique 'base',
        it will behave like a little-endian number
        """
        indices = self.irreg_int.value
        ret = []
        try:
            for idx in range(len(indices)):
                ret.append(self.arg_array[idx]['val'][indices[idx]])
        except:
            # TODO do something
            breakpoint()
        return ret

class IrregularLittleEndianInt():
    def __init__(self, l_bases: list):
        # TODO error handling for failure to pass correct type
        self.bases = l_bases
        self.value = [0] * len(l_bases)
        self.overflow = False
    
    def __iadd__(self, other: int):
        if isinstance(other, int):
            pass
        else:
            raise ValueError("Iterated IrregularLittleEndianInt by something other than an integer")
        for _ in range(other):
            idx = 0
            while True:
                self.value[idx] += 1
                if self.value[idx] % self.bases[0] == 0:
                    # breakpoint()
                    self.value[0] = 0
                    if idx + 1 == len(self.bases) and (self.value[idx]) % self.bases[-1] == 0:
                        self.overflow = True
                        break
                    else:
                        idx += 1
                else:
                    break
        return self
