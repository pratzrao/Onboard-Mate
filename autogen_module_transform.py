import autogen
import os
from autogen.coding import LocalCommandLineCodeExecutor

# Define the function that handles the chat
def generate_dbt_code(user_prompt):
    # Configuration for the LLM
    config_list = [{"model": "gpt-4o-mini", "api_key": os.getenv("OPENAI_API_KEY")}]

    # Create an AssistantAgent instance
    assistant = autogen.AssistantAgent(
        name="assistant",
        llm_config={
            "cache_seed": 41,
            "config_list": config_list,
            "temperature": 0,
        },
    )

    # Create a Reviewer Agent to correct prompt logic
    reviewer = autogen.AssistantAgent(
        name="reviewer",
        llm_config={
            "cache_seed": 42,  # Different seed for different behavior
            "config_list": config_list,
            "temperature": 0.1,  # Slightly more creative for prompt correction
        },
    )

    # Review the user prompt with the Reviewer agent
    review_res = reviewer.initiate_chat(
        assistant,
        message=f"Review the following transformation request for any logical issues and correct it if needed:\n{user_prompt}",
        summary_method="reflection_with_llm",
        silent=True
    )

    reviewed_prompt = review_res.chat_history[-1]['content']

    # Start the final DBT code generation
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
        code_execution_config={
            "executor": LocalCommandLineCodeExecutor(work_dir="coding"),
        },
    )


    # Generate DBT code with the corrected prompt
    chat_res = user_proxy.initiate_chat(
        assistant,
        message=reviewed_prompt,
        summary_method="reflection_with_llm",
        silent=True
    )

    result = None
    for agent, messages in assistant.chat_messages.items():
        # look only at the last message with any content
        for message in reversed(messages):
            if message.get("content") and message['content'].find("```sql") == 0:
                print(message['content'])
                result = message['content']
                break
        # for message in messages:
        #     for k, v in message.items():
        #         print("%20s %50s" % (k, v))

    # Extract the DBT code from the reply, ignoring any termination messages
    return {
        "result": result            
        }
