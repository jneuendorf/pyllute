import builtins
from dataclasses import dataclass, field
import json
import math
from typing import Callable, Dict

from _utils import generate


@dataclass
class Meta:
    namespaces: list
    serializers: Dict[str, Callable] = field(default_factory=dict)


tests = {
    'converters': Meta([builtins], {
        'object': lambda o: dict(),
    }),
    'iterables': Meta([builtins], {
        'enumerate': list,
        'iter': list,
    }),
    'math': Meta([builtins]),
    'stdtypes': Meta([builtins], {
        'bytearray': list,
        'bytes': list,
        'float': lambda x: (
            str(x)
            if math.isinf(x) or math.isnan(x)
            else x
        ),
        'range': list,
        'set': list,
        # 'str': lambda x: (
        #     x
        #     if x != 'None'
        #     else '__None__'
        # ),
    }),
}

if __name__ == "__main__":
    try:
        for testname, meta in tests.items():
            generate(testname, meta.namespaces, meta.serializers)
    except json.decoder.JSONDecodeError as e:
        raise RuntimeError(f'Error while generating "{testname}"') from e
