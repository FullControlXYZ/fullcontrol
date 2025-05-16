
# from pydantic import model_validator, BaseModel
from pydantic import BaseModel, __version__

if int(__version__.split('.')[0]) >= 2:
    from pydantic import model_validator as validator
    validator_args = {"mode": "before"}
else:
    from pydantic import root_validator as validator
    validator_args = {"pre": True}

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

    @classmethod
    @validator(**validator_args)
    def reject_extra_fields(cls, values):
        """
        This method checks if any extra fields are present in the values dictionary
        that are not defined in the class. If any extra fields are found, an exception is raised.

        Args:
            cls (Type): The class being validated.
            values (Dict[str, Any]): The values to be checked.

        Raises:
            Exception: If any invalid field name is found.

        Returns:
            Dict[str, Any]: The validated values.
        """
        annots = cls.__fields__
        for value in values:
            if value not in annots:
                # print(f'error: value "{value}" not allowed for the class {cls.__name__}. attributes defined: {values}')
                raise Exception(
                    f'error: value "{value}" not allowed for the class {cls.__name__}\nattributes defined: {values}\nattributes allowed: {cls.__fields__.keys()}')
        return values
