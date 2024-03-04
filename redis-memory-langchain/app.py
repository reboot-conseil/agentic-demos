from langchain_community.chat_message_histories import RedisChatMessageHistory
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

history = RedisChatMessageHistory("foo", url="redis://localhost:6379")

llm = ChatOllama(model="mistral")

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You're an old friend."),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{question}"),
    ]
)

chain = prompt | llm
chain_with_history = RunnableWithMessageHistory(
    chain, # type: ignore
    lambda session_id: RedisChatMessageHistory(
        # this is supposed to run in the Docker Compose stack
        session_id, url="redis://localhost:6379"
    ),
    input_messages_key="question",
    history_messages_key="history",
)

config = {"configurable": {"session_id": "demo"}}


# start an infinite dialog loop
while True:
    user_input = input("speak your mind or ctrl + c:")
    
    # check if the user wants to exit the loop
    if user_input == 'exit':
        print("until next time! 👋🏼")
        break 
    
    history.add_user_message(user_input)
    llm_output = chain_with_history.invoke({
        "question": user_input
    }, config=config) # type: ignore
    print(llm_output.content)
    history.add_ai_message(llm_output.content)
