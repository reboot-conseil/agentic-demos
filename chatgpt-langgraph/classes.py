from langchain_core.messages import BaseMessage
import operator
from typing import Annotated, Sequence, TypedDict

class AgentState(TypedDict):
    # we use `Annotated` to hint that the `messages` field is a sequence of `BaseMessage` objects, and that we can add to it;
    # the `operator.add` is here to specify that we can add messages instead of overwriting the whole thing all the time
    messages: Annotated[Sequence[BaseMessage], operator.add]