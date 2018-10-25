from typing import Iterable

from rests.typescript.type_model.fields.concrete_field import ConcreteField
from rests.typescript.utils.render_object import Literal


# =================================
# Relational Field
# ---------------------------------

class RelationalField(ConcreteField):

    def names(self) -> Iterable[str]:
        yield self.name
        yield self.fk_id_name

    def interface_type_declarations(self) -> Iterable[str]:
        """
        Return the `interface` type declarations for this field. This will be used
        to generate the `<model_name>Data` TypeScript interface.


        """
        yield self.base_interface_type_declaration
        yield self.fk_id_type_declaration

    def cls_type_declarations(self) -> Iterable[str]:
        """
        Return the class property declarations for this field. This will be used
        to declare the names/types for this field for its TypeScript Model class.

        """
        yield self.base_cls_type_declaration
        yield self.fk_id_type_declaration

    @property
    def fk_id_type_declaration(self):
        return self.fk_id_name + "?" * self.is_optional + " : number"

    @property
    def fk_id_name(self):
        return self.name + "_id"

    @property
    def related_model(self):
        return self.model_field.related_model

    @property
    def related_model_name(self):
        return self.related_model.__name__

    @property
    def _schema_related_model(self):
        return Literal("() => " + self.related_model_name)
