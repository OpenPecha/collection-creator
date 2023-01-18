from datetime import datetime
from enum import Enum
from typing import Dict, Optional, Union,List

from pydantic import AnyHttpUrl, BaseModel, Extra, validator
import time
from . import ids
import re


class AlignmentMetadata(BaseModel):
    id:str
    title:str
    type: str
    pechas: List[str]
    alignment_to_base:Dict[str,str]
    source_metadata: Optional[Dict] = None

class Alignment():
    def __init__(self) -> None:
        pass
