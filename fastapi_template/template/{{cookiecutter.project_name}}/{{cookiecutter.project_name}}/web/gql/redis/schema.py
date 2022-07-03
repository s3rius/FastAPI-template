from typing import Optional

import strawberry


@strawberry.type
class RedisDTO:
    """Output type for redis queries."""

    key: str
    value: Optional[str]


@strawberry.input
class RedisDTOInput:
    """Input type for redis mutation."""

    key: str
    value: str
