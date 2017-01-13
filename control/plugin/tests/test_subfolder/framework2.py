from ...manager import DeclarePlugin, DeclareFramework


@DeclareFramework('framework1')
class ExampleFramework(object):
    def __init__(self, options=None):
        pass


@DeclarePlugin('plugin1', 100)
class ExamplePlugin1(ExampleFramework):
    pass


@DeclarePlugin('plugin2', 100)
class ExamplePlugin2(ExampleFramework):
    pass


@DeclarePlugin('plugin3', 100)
class ExamplePlugin3(ExampleFramework):
    pass
