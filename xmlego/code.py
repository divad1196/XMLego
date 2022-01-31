import functools
import contextlib
import sys


# _ALLOWED_MODULES = ['_strptime', 'math', 'time']

# def _import(name, globals=None, locals=None, fromlist=None, level=-1):
#     if globals is None:
#         globals = {}
#     if locals is None:
#         locals = {}
#     if fromlist is None:
#         fromlist = []
#     if name in _ALLOWED_MODULES:
#         return __import__(name, globals, locals, level)
#     raise ImportError(name)

def _import(name, globals=None, locals=None, fromlist=None, level=-1):
    raise Exception("Import is prohibited inside templates")

BUILTINS = {
    "__import__": _import,
    "all": all,
    "any": any,
    "ascii": ascii,
    "bin": bin,
    "bool": bool,
    "bytearray": bytearray,
    "bytes": bytes,
    "callable": callable,
    "chr": chr,
    "complex": complex,
    "dict": dict,
    "dir": dir,
    "divmod": divmod,
    # "Ellipsis": Ellipsis,
    "enumerate": enumerate,
    "False": False,
    "filter": filter,
    "float": float,
    "format": format,
    "frozenset": frozenset,
    "getattr": getattr,
    # "globals": globals,
    "hasattr": hasattr,
    "hash": hash,
    "hex": hex,
    # "id": id,
    "int": int,
    "isinstance": isinstance,
    "issubclass": issubclass,
    "iter": iter,
    "len": len,
    "list": list,
    "map": map,
    "max": max,
    "min": min,
    "next": next,
    "None": None,
    "oct": oct,
    "ord": ord,
    "pow": pow,
    # "print": print,
    "range": range,
    "reduce": functools.reduce,
    "repr": repr,
    "reversed": reversed,
    "round": round,
    "set": set,
    "setattr": setattr,
    "slice": slice,
    "sorted": sorted,
    "str": str,
    "sum": sum,
    "True": True,
    "tuple": tuple,
    "type": type,
    "zip": zip,
}

# In case we need to filter
# Globals must contain __builtins__ entry 
def exec_code(code, globals=None, locals=None):
    if globals is None:
        globals = {"__builtins__": BUILTINS}
    if locals is None:
        locals = {}
    exec(code, globals, locals)
    return globals, locals

def eval_code(code, globals=None, locals=None):
    if globals is None:
        globals = {"__builtins__": BUILTINS}
    if locals is None:
        locals = {}
    return eval(code, globals, locals)



# TODO: Not working
# @contextlib.contextmanager
# def safe_code():
#     modules = sys.modules
#     builtins = globals()["__builtins__"]
#     sys.modules = []
#     globals()["__builtins__"] = BUILTINS
#     sys.modules = []
#     try:
#         yield
#     finally:
#         print("restauring data")
#         globals()["__builtins__"] = builtins
#         sys.modules = modules


# with safe_code():
#     print("print" in dir(globals()["__builtins__"]))