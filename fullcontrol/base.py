
# from pydantic import model_validator, BaseModel
from pydantic import BaseModel, root_validator


class BaseModelPlus(BaseModel):
    def __setitem__(self, name, value): setattr(self, name, value)

    def __getitem__(self, name): return getattr(self, name)

    def update_from(self, source):
        self_vars = vars(self)  # cache, for multiple checks
        for key, value in vars(source).items():
            if (value is not None) and (key in self_vars):
                self[key] = value

    # @model_validator(mode="before")
    # @classmethod
    @root_validator(pre=True)
    def check_card_number_omitted(cls, values):
        annots = cls.__fields__
        for value in values:
            if value not in annots:
                # print(f'error: value "{value}" not allowed for the class {cls.__name__}. attributes defined: {values}')
                raise Exception(
                    f'error: value "{value}" not allowed for the class {cls.__name__}\nattributes defined: {values}\nattributes allowed: {cls.__fields__.keys()}')
        return values
