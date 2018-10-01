from django.db import models

from rests.core.utils.model_inspector import ModelInspector
from rests.typescript import code_generators as ts
from rests.typescript import types


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
    def private_name(self):
        return "_" + self.field.name

    @property
    def related_model_name(self):
        if self.is_concrete:
            return None
        return self.field.related_model.__name__

    @property
    def base_var_name(self):
        if not self.is_relational:
            return self.field.name
        return "_" + self.field.name

    @property
    def reverse_lookup_key(self):
        inspector = ModelInspector(model=self.field.related_model)
        return inspector.fk_field_to_model(model=self.field.model).name + '__id'

    def base_type_declaration(self):
        return ts.TypeDeclaration(var_name=self.base_var_name, type_=self.field, optional=self.is_optional)

    def type_declarations(self):
        type_declarations = list()
        # We don't declare many-to-one relational fields.
        if isinstance(self.field, models.ManyToOneRel):
            return type_declarations
        type_declarations.append(self.base_type_declaration())
        # If this field is a ForeignKey, add an extra declaration for its
        # `id` lookup.
        if isinstance(self.field, models.ForeignKey):
            type_declarations.append(
                ts.TypeDeclaration(var_name=self.field.name + '_id', type_=types.NUMBER, optional=self.is_optional)
            )
        return type_declarations

    @property
    def public_getter_method(self):
        if not self.is_relational:
            return ""
        return_type = f"undefined | Promise<{ self.related_model_name } | undefined> | { self.related_model_name }"
        return ts.public + ts.get + ts.Function(name=self.field.name, return_type=return_type)(f"""
        if (!this.{ self.fk_id_name }){{return undefined}}
        if (this.{ self.base_var_name }){{ return this.{ self.base_var_name } }}
        return (async () => {{
            return await this._get{ self.field.name.capitalize() }();
        }})();
        """)

    @property
    def private_getter_method(self):
        if not self.is_relational:
            return ""
        return_type = f"Promise<{ self.related_model_name } | undefined >"
        return ts.private + ts.async_ + ts.Function(name='_get' + self.field.name.capitalize(), return_type=return_type)(f"""
        if (this.{ self.fk_id_name } !== undefined){{
            const { self.field.name } = await { self.related_model_name }.objects.get(this.{ self.fk_id_name });
            this.{ self.base_var_name } = { self.field.name }
            return { self.field.name }
        }}
        return undefined
        """)

    @property
    def setter_method(self):
        if not self.is_relational:
            return ""
        call_sig = ts.CallSignature(ts.TypeDeclaration(
            var_name=self.field.name,
            type_=f"undefined | Promise<{ self.related_model_name } | undefined> | { self.related_model_name }")
        )
        return ts.public + ts.set_ + ts.Function(name=self.field.name, call_signature=call_sig)(f"""
        if ({ self.field.name } instanceof { self.related_model_name } ){{
            this.{ self.fk_id_name } = { self.field.name }.pk();
            this.{ self.base_var_name } = { self.field.name };
        }} else {{
            this.{ self.fk_id_name } = undefined;
            this.{ self.base_var_name } = undefined;
        }}
        """)

    @property
    def reverse_relation_getter(self):
        if not self.is_reverse_relation:
            return ""
        return ts.public + ts.Function(name=self.field.name, return_type=self.related_model_name + "QuerySet")(f"""
        return new { self.related_model_name }QuerySet({{...{{ { self.reverse_lookup_key }: this.pk() }}}})
        """)



