import autogen
import os
from autogen.coding import LocalCommandLineCodeExecutor
#from autogen import Agent, AssistantAgent, ConversableAgent, UserProxyAgent

config_list = [{"model": "gpt-4o-mini", "api_key": os.getenv("OPENAI_API_KEY")}]

# create an AssistantAgent named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={
        "cache_seed": 41,  # seed for caching and reproducibility
        "config_list": config_list,  # a list of OpenAI API configurations
        "temperature": 0,  # temperature for sampling
    },  # configuration for autogen's enhanced inference API which is compatible with OpenAI API
)

# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        # the executor to run the generated code
        "executor": LocalCommandLineCodeExecutor(work_dir="coding"),
    },
)
# the assistant receives a message from the user_proxy, which contains the task description
chat_res = user_proxy.initiate_chat(
    assistant,
    message="""I have a table with columns - name, age, date, gender, id, timestamp. Write dbt code for me. I need to drop the column timestamp, and drop all rows with null values in date.""",
    summary_method="reflection_with_llm",
)

print("Chat history:", chat_res.chat_history)

print("Summary:", chat_res.summary)

print("Cost info:", chat_res.cost)

