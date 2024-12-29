"""DB-GPT: Next Generation Data Interaction Solution with LLMs.
"""
from dbgpt import _version  # noqa: E402
from dbgpt.component import BaseComponent  # noqa: F401
from dbgpt.component import SystemApp
# """ 此 componet 文件会导入很多文件： Config 等一系列 Utils 模块及方法 """
# """ 同时在 component 模块导入其他包时，又会进一步导入其他包的 __init__.py 模块信息 """


_CORE_LIBS = ["core", "rag", "model", "agent", "datasource", "vis", "storage", "train"]
_SERVE_LIBS = ["serve"]
_LIBS = _CORE_LIBS + _SERVE_LIBS


__version__ = _version.version
print(__version__,'*' * 50)

__ALL__ = ["__version__", "SystemApp", "BaseComponent"]


def __getattr__(name: str):
    # Lazy load
    import importlib

    if name in _LIBS:
        return importlib.import_module("." + name, __name__)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
