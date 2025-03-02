import os
import autogen
from autogen.coding import LocalCommandLineCodeExecutor


# Define the function that handles the chat
def generate_dbt_code(raw_prompt, metadata, new_table_name):
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

    # Start the final DBT code generation
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

    # Review the user prompt with the Reviewer agent
    review_res = user_proxy.initiate_chat(
        assistant,
        message=f"Review the following transformation request for a table. If the request does not contain a proper database transformation request, reply with NO. If it is perfectly correct or it makes logical sense but there are a few mistakes like typos or improperly explained concepts - clarify the transformation prompt and explain it better and return the corrected prompt ONLY WITH NO OTHER EXPLANATIONS OR ACKNOWLEDGEMENTS. Return NO ONLY if the prompt is rubbish. If it can be fixed, return the fixed prompt. The prompt is:\n{raw_prompt}.",
        summary_method="reflection_with_llm"
    )

    all_messages = list(assistant.chat_messages.values())
    flat_messages = [msg for sublist in all_messages for msg in sublist]

    # Iterate through flat_messages to find what the 'assistant' said
    assistant_messages = [msg['content'] for msg in flat_messages if msg['role'] == 'assistant']
    reviewed_prompt = assistant_messages[-2]

    print("reviewed_prompt - ", reviewed_prompt)
    if reviewed_prompt == 'NO':
        return("Error")
    
    full_prompt = (
                f"I need you to write code for a dbt model based on table details and user information that you'll find below. "
                f"We are using a Postgres database. Make sure the model is accurate and will execute with no changes necessary. "
                f"Return only the dbt code. NOTHING ELSE. Don't say anything. Do not use ref to reference the table you are selecting from - the name of the db is hackathon_pratiksha. An example of how the source table should be referred is -  {{ source('hackathon_pratiksha', 'tablename_here') }}. You can just put a from before that and write the rest of the sql normally. You will be reading the table from a source.yml file. DON'T RUN ANY CODE. Don't acknowledge my question, say yes or sure—just give me the code that I asked for.\n"
                f"Table Metadata:\n{metadata}\n\nTransformation Instructions:\n{reviewed_prompt}\n\nNew Table: {new_table_name}"
            )
        

    # Generate DBT code with the corrected prompt
    chat_res = user_proxy.initiate_chat(
        assistant,
        message=full_prompt,
        summary_method="reflection_with_llm",
    )

    result = None
    for agent, messages in assistant.chat_messages.items():
        # look only at the last message with any content
        for message in reversed(messages):
            if message.get("content") and message['content'].find("```sql") == 0:
                result = message['content']
                break


    # Extract the DBT code from the reply, ignoring any termination messages
    return {
        "result": result            
        }


# Example usage:
# if __name__ == "__main__":
#     user_prompt = """
#     I have a table with columns - name, age, date, gender, id, timestamp.
#     Write dbt code for me. I need to drop the column timestamp, and drop all rows with null values in date.
#     """
#     result = generate_dbt_code(user_prompt)

#     # Print the outputs
#     print("Reply:", result["reply"])
#     print("Chat history:", result["chat_history"])
#     print("Summary:", result["summary"])
