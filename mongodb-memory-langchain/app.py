from langchain_community.chat_message_histories import MongoDBChatMessageHistory, RedisChatMessageHistory
from langchain_community.chat_models import ChatOllama
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

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
    lambda session_id: MongoDBChatMessageHistory(
        session_id=session_id,
        connection_string="mongodb://localhost:27017",
        database_name="my_db",
        collection_name="chat_histories",
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
    
    llm_output = chain_with_history.invoke({
        "question": user_input
    }, config=config) # type: ignore
    print(llm_output.content)
