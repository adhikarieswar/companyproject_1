# models/base.py
from pydantic import BaseModel, ConfigDict
from typing import Any

class BaseModelConfig(BaseModel):
    # Disable deep copying of complex objects
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        ignored_types=(type(...),)  # Add any other types you need to ignore
    )