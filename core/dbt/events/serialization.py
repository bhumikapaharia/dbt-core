from mashumaro import DataClassDictMixin
from mashumaro.config import (
    BaseConfig as MashBaseConfig
)
from mashumaro.types import SerializationStrategy
from datetime import datetime
from dateutil.parser import parse
from typing import cast


class ExceptionSerialization(SerializationStrategy):
    def serialize(self, value):
        out = str(value)
        return out

    def deserialize(self, value):
        return (Exception(value))


class DateTimeSerialization(SerializationStrategy):
    def serialize(self, value):
        out = value.isoformat()
        # Assume UTC if timezone is missing
        if value.tzinfo is None:
            out += "Z"
        return out

    def deserialize(self, value):
        return (
            value if isinstance(value, datetime) else parse(cast(str, value))
        )


class BaseExceptionSerialization(SerializationStrategy):
    def serialize(self, value):
        return str(value)

    def deserialize(self, value):
        return (BaseException(value))


class dbtClassEventMixin(DataClassDictMixin):

    class Config(MashBaseConfig):
        serialization_strategy = {
            Exception: ExceptionSerialization(),
            datetime: DateTimeSerialization(),
            BaseException: ExceptionSerialization(),
        }
