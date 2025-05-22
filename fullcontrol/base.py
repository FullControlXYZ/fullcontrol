
# from pydantic import model_validator, BaseModel
from pydantic import BaseModel, __version__


def check_fields(allowed_fields, defined_attributes, class_name):
   for attribute in defined_attributes.keys():
       if attribute not in allowed_fields:
           raise Exception(f'\nattribute "{attribute}" not allowed for the class {class_name}\nattributes defined: {str(defined_attributes)[1:-1]}\nattributes allowed: {repr(list(allowed_fields))[1:-1]}')

    
class BaseModelPlus(BaseModel):

    """
    A subclass of BaseModel with additional functionality.

    This class extends the functionality of the BaseModel class by adding the ability to update its attributes from another object,
    and a validator to check if certain attributes are allowed.

    Attributes:
        None

    Methods:
        __setitem__: Sets the value of an attribute.
        __getitem__: Retrieves the value of an attribute.
        update_from: Updates the attributes of the object from another object.
        reject_extra_fields (classmethod): Validator to check if certain attributes are allowed.

    """

    def __setitem__(self, name, value): setattr(self, name, value)

    def __getitem__(self, name): return getattr(self, name)

    def update_from(self, source):
            """
            Updates the attributes of the current object from the attributes of another object.

            Args:
                source: The object from which to update the attributes.

            Returns:
                None
            """
            self_vars = vars(self)  # cache, for multiple checks
            for key, value in vars(source).items():
                if (value is not None) and (key in self_vars):
                    self[key] = value

    if int(__version__.split('.')[0]) >= 2:
        # Pydantic v2 config
        model_config = {"extra": "allow"}
        from pydantic import model_validator
        @model_validator(mode="before")
        @classmethod
        def reject_extra_fields(cls, values):
            check_fields(cls.model_fields.keys(), values, cls.__name__)
            # values must be returned for pydantic v2
            return values
    else:
        from pydantic import root_validator
        # Pydantic v1 config
        class Config:
            extra = "allow"
        @root_validator(pre=True)
        @classmethod
        def reject_extra_fields(cls, values):
            check_fields(cls.__fields__.keys(), values, cls.__name__)
            return values