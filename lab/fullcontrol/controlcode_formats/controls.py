from typing import Optional
from pydantic import BaseModel
from fullcontrol import GcodeControls


class CodeControls(BaseModel):
    ''' Controls to adjust the language/format of a generated set of instructions (i.e. machine control code)'''
    code_format: Optional[str] = None
    controls: Optional[GcodeControls] = None
    filename: Optional[str] = 'my_design'
