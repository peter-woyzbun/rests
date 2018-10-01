from typing import List, Union

from jinja2 import Template


# =================================
# Code Generator
# ---------------------------------

class CodeGenerator(object):

    TEMPLATE: str = None

    def __init__(self, value: str = None):
        self.value = value
        self.prefixes: List[str] = list()

    def __add__(self, other: Union[str, 'CodeGenerator']):
        return CodeGenerator(str(self) + " " + str(other))

    def __str__(self):
        if self.value is not None:
            return self.value
        return self.render()

    def render(self):
        return " ".join(self.prefixes) + " " * (len(self.prefixes) > 0) + self._render()

    def _render(self) -> str:
        raise NotImplementedError

    def _render_template(self, **kwargs) -> str:
        return Template(self.TEMPLATE).render(**kwargs)


