from django.db import models

from rests.core.utils.model_inspector import ModelInspector
from rests.typescript.type_transpiler import TypeTranspiler


# =================================
# Typescript Model Field
# ---------------------------------

class Field(object):

    """
    Helper class for rendering "type declarations" for Model fields.

    """

    def __init__(self, field: models.Field):
        self.field = field

    @property
    def is_relational(self):
        return isinstance(self.field, (models.ForeignKey, models.OneToOneField))

    @property
    def is_reverse_relation(self):
        return isinstance(self.field, models.ManyToOneRel)

    @property
    def is_concrete(self):
        return not self.is_relational and not self.is_reverse_relation

    @property
    def is_optional(self) -> bool:
        return self.field.null

    @property
    def fk_id_name(self):
        return self.field.name + "_id"

    @property
    def name(self):
        return self.field.name

    def names(self):
        names = list()
        if isinstance(self.field, models.ManyToOneRel):
            return names
        names.append(self.name)
        if self.is_relational:
            names.append(self.fk_id_name)
        return names

    @property
    def private_name(self):
        return "_" + self.field.name

    @property
    def related_model_name(self):
        if self.is_concrete:
            return None
        return self.field.related_model.__name__

    @property
    def reverse_lookup_key(self):
        inspector = ModelInspector(model=self.field.related_model)
        return inspector.fk_field_to_model(model=self.field.model).name + '__id'

    @property
    def base_interface_type_declaration(self):
        type_dec = self.name + "?" * self.is_optional + " : " + TypeTranspiler.transpile(self.field)
        return type_dec

    @property
    def base_cls_type_declaration(self):
        type_dec = self.name + "?" * self.is_optional + " : " + TypeTranspiler.transpile(self.field)
        if self.is_relational:
            return f"@foreignKeyField({self.related_model_name}) " + type_dec
        return type_dec

    @property
    def fk_id_type_declaration(self):
        return self.fk_id_name + "?" * self.is_optional + " : number"

    def interface_type_declarations(self):
        type_declarations = list()
        # We don't declare many-to-one relational fields.
        if isinstance(self.field, models.ManyToOneRel):
            return type_declarations
        type_declarations.append(self.base_interface_type_declaration)
        # If this field is a ForeignKey, add an extra declaration for its
        # `id` lookup.
        if isinstance(self.field, models.ForeignKey):
            type_declarations.append(self.fk_id_type_declaration)
        return type_declarations

    def cls_type_declarations(self):
        type_declarations = list()
        # We don't declare many-to-one relational fields.
        if isinstance(self.field, models.ManyToOneRel):
            return type_declarations
        type_declarations.append(self.base_cls_type_declaration)
        # If this field is a ForeignKey, add an extra declaration for its
        # `id` lookup.
        if isinstance(self.field, models.ForeignKey):
            type_declarations.append(self.fk_id_type_declaration)
        return type_declarations

