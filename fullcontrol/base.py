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
        check_card_number_omitted: Validator to check if certain attributes are allowed.

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
    def check_card_number_omitted(cls, values):
        """
        Check if the card number is omitted.

        This function validates if the given values contain any card number that is not allowed for the class.
        It raises an exception if any invalid card number is found.

        Args:
            cls (Type): The class being validated.
            values (Dict[str, Any]): The values to be checked.

        Raises:
            Exception: If any invalid card number is found.

        Returns:
            Dict[str, Any]: The validated values.
        """
        fields = cls.model_fields if int(__version__.split('.')[0]) >= 2 else cls.__fields__
        for value in values:
            if value not in fields:
                raise Exception(
                    f'error: value "{value}" not allowed for the class {cls.__name__}\nattributes defined: {values}\nattributes allowed: {fields.keys()}')
        return values
