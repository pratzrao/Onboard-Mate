import os
import autogen
from autogen.coding import LocalCommandLineCodeExecutor


# Define the function that handles the chat
def generate_charts(user_prompt):
    # Configuration for the LLM
    # You need to set the API Key in your environment by running in terminal - "export OPENAI_API_KEY=/"Your API Key/" "
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

    # Create a UserProxyAgent instance
    user_proxy = autogen.UserProxyAgent(
        name="user_proxy",
        human_input_mode="NEVER",
        max_consecutive_auto_reply=10,
        is_termination_msg=lambda x: x.get("content", "")
        .rstrip()
        .endswith("TERMINATE"),
        code_execution_config={
            "executor": LocalCommandLineCodeExecutor(work_dir="coding"),
        },
    )

    # Start the chat and get the response
    chat_res = user_proxy.initiate_chat(
        assistant,
        message=user_prompt,
        summary_method="reflection_with_llm",
    )

    # Extract and return the reply, chat history, and summary
    reply = chat_res.chat_history[-1]["content"] if chat_res.chat_history else None
    return {
        "reply": reply,
        "chat_history": chat_res.chat_history,
        "summary": chat_res.summary,
    }


# Example usage:
# if __name__ == "__main__":
#     user_prompt = """
#     Build xyz chart for me thanks
#     """
#     result = generate_dbt_code(user_prompt)

#     # Print the outputs
#     print("Reply:", result["reply"])
#     print("Chat history:", result["chat_history"])
#     print("Summary:", result["summary"])
