from typing import List

from rests.core.typescript.code_generator import CodeGenerator


# =================================
# Destructuring
# ---------------------------------

class Destructuring(CodeGenerator):

    TEMPLATE = "{ {{ destructuring.name_list }} }"

    def __init__(self, var_names: List[str]):
        self.var_names = var_names
        CodeGenerator.__init__(self)

    @property
    def name_list(self):
        return ", ".join(self.var_names)

    def _render(self):
        return self._render_template(destructuring=self)