from pydantic import BaseModel, Field


class RedisSetModel(BaseModel):
    key: str
    value: str
    expire: int = Field(default=0)


class RedisValueModel(BaseModel):
    value: str
