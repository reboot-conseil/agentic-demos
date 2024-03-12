from dotenv import load_dotenv
load_dotenv()

import json
from langchain_community.tools.ddg_search import DuckDuckGoSearchRun
from langchain_community.tools.arxiv.tool import ArxivQueryRun
from langchain_core.messages import FunctionMessage, HumanMessage
from langchain_core.utils.function_calling import convert_to_openai_function
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import chat_agent_executor, ToolExecutor, ToolInvocation

from classes import AgentState

tool_belt = [DuckDuckGoSearchRun(), ArxivQueryRun()]

# the tool executor is how we are going to call the tools

model = ChatOpenAI(model="gpt-4-0125-preview")

# turning our tools into something that OpenAI models can understand
functions = [convert_to_openai_function(tool) for tool in tool_belt]

# binding the functions to the model
app = chat_agent_executor.create_function_calling_executor(model, tool_belt)

def call_model_node(state):
    messages = state["messages"]
    response = model.invoke(messages)
    # we modify the state with the response from the model
    return {"messages": [response]}

async def call_tool_node(state):
    last_message = state["messages"][-1]
    action = ToolInvocation(
        tool=last_message.additional_kwargs["function_call"]["name"],
        tool_input=json.loads(
            last_message.additional_kwargs["function_call"]["arguments"]
        )
    )
    response = app.invoke(action)
    function_message = FunctionMessage(content=str(response), name=action.tool)
    # modifies the state to get the response from the tool call
    return {"messages": [function_message]}

# defining the function that determines if we are going to continue the workflow
def should_continue_workflow(state):
    # if the last message was not a question, we are going to use a tool
    last_message = state["messages"][-1]

    print("\n")
    print("getting message from `should_continue_workflow`")
    print(last_message)
    print("\n")

    if "function_call" not in last_message.additional_kwargs:
        return "end"
    
    return "continue"


# initializing the state of the workflow as a list of messages
workflow = StateGraph(AgentState)

# setting the two nodes of the graph, they are not connected at this point
workflow.add_node("agent", call_model_node)
workflow.add_node("action", call_tool_node)

# this is what will allow you to take the user's input and move it through the graph
workflow.set_entry_point("agent")

# adding the conditional edge that will determine when to stop the workflow
workflow.add_conditional_edges(
    # origin node
    "agent",
    # moving the state object to this function
    should_continue_workflow,
    {
        # if we receive the "continue" response from the conditional edge, we proceed to calling a tool
        "continue": "action",
        "end": END
    }
)

# last edge, that connects the action node back to the agent node
workflow.add_edge("action", "agent")

# initializing the state of the workflow as a list of messages
inputs = {
    "messages": [HumanMessage(
        content="will software developers disappear? use the tools at your disposal to find out"
    )]
}

print(app.invoke(inputs))