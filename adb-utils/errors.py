
# 当没有定义 __all__ 变量时，使用 from module import * 导入语句会导入模块中所有未以下划线开头的名称。
# ，在没有 __all__ 的情况下，所有未以下划线开头的方法和属性都会被认为是公共的，并可以被其他模块访问。
# 尽管如此，这种方式并不可靠，并且容易导致命名空间污染和命名冲突等问题。
#
# 为了避免这些潜在的问题，建议在模块中显式地定义 __all__ 变量，以指定应该暴露给外部的公共接口。
# 通过明确指定 __all__，可以提供更好的控制和文档化，并防止意外导入和使用模块中的私有对象。
__all__ = [
    "AdbError",
    "AdbTimeoutError"
]


class AdbError(Exception):
    pass


class AdbTimeoutError(AdbError):
    pass
