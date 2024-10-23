import os
import asyncio

import streamlit as st
from autogen import AssistantAgent, UserProxyAgent
from autogen.coding import LocalCommandLineCodeExecutor

class TrackableAssistantAgent(AssistantAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
        return super()._process_received_message(message, sender, silent)

class TrackableUserProxyAgent(UserProxyAgent):
    def _process_received_message(self, message, sender, silent):
        with st.chat_message(sender.name):
            st.markdown(message)
        return super()._process_received_message(message, sender, silent)

class ChartCreator:
    @staticmethod
    def is_termination_msg(msg):
        content = 'content' in msg
        return content and msg['content'].rstrip().endswith('TERMINATE')

    def __init__(self):
        # Create an AssistantAgent instance
        self.assistant = TrackableAssistantAgent(
            name="assistant",
            llm_config={
                "cache_seed": 41,
                "config_list": [{
                    "model": "gpt-4o-mini",
                    "api_key": os.getenv("OPENAI_API_KEY"),
                }],
                "temperature": 0,
            },
        )

        # Create a UserProxyAgent instance
        self.user_proxy = TrackableUserProxyAgent(
            name="user_proxy",
            human_input_mode='ALWAYS',
            max_consecutive_auto_reply=10,
            is_termination_msg=self.is_termination_msg,
            code_execution_config={
                "executor": LocalCommandLineCodeExecutor(work_dir="coding"),
            },
        )

    def __call__(self, message):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop.run_until_complete(self.process(message))

    async def process(self, message):
        response = await self.user_proxy.ainitiate_chat(
            self.assistant,
            message=message,
            summary_method="reflection_with_llm",
        )

        # Extract and return the reply, chat history, and summary
        if chat_res.chat_history:
            (*_, last) = chat_res.chat_history
            reply = last['content']
        else:
            reply = None

        return reply
