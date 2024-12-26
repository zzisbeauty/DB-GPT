import asyncio

# dag api
from dbgpt.core.awel import DAG

# operator api
# from dbgpt.core.operators import (
#     PromptBuilderOperator,
#     RequestBuilderOperator,
# )
from dbgpt.core.operators import PromptBuilderOperator
from dbgpt.core.operators import RequestBuilderOperator



# model api
from dbgpt.model.proxy import OpenAILLMClient
from dbgpt.model.operators import LLMOperator


with DAG("simple_sdk_llm_example_dag") as dag:
    prompt_task = PromptBuilderOperator(
        "Write a SQL of {dialect} to query all data of {table_name}."
    )
    model_pre_handle_task = RequestBuilderOperator(model="gpt-3.5-turbo")
    llm_task = LLMOperator(OpenAILLMClient())
    prompt_task >> model_pre_handle_task >> llm_task
    
output = asyncio.run(
    llm_task.call({
        "dialect": "MySQL", 
        "table_name": "users"
    }
))

print(output)