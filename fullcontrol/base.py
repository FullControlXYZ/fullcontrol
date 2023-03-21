
from pydantic import BaseModel, root_validator


class BaseModelPlus(BaseModel):
    def __setitem__(self, name, value): setattr(self, name, value)

    def __getitem__(self, name): return getattr(self, name)

    def update_from(self, source):
        for key in source.__dict__:
            if source.__dict__[key] != None:
                if key in self.__dict__:
                    self[key] = source.__dict__[key]

    @root_validator(pre=True)
    def check_card_number_omitted(cls, values):
        annots = cls.__fields__
        for value in values:
            if value not in annots:
                # print(f'error: value "{value}" not allowed for the class {cls.__name__}. attributes defined: {values}')
                raise Exception(
                    f'error: value "{value}" not allowed for the class {cls.__name__}\nattributes defined: {values}\nattributes allowed: {cls.__fields__.keys()}')
        return values
