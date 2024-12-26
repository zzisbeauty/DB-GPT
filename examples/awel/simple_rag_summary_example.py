"""AWEL:
This example shows how to use AWEL to build a simple rag summary example.
    pre-requirements:
        1. install openai python sdk
        ```
            pip install openai
        ```
        2. set openai key and base
        ```
            export OPENAI_API_KEY={your_openai_key}
            export OPENAI_API_BASE={your_openai_base}
        ```
        or
        ```
            import os
            os.environ["OPENAI_API_KEY"] = {your_openai_key}
            os.environ["OPENAI_API_BASE"] = {your_openai_base}
        ```
        python examples/awel/simple_rag_summary_example.py
    Example:

    .. code-block:: shell

        curl -X POST http://127.0.0.1:5555/api/v1/awel/trigger/examples/rag/summary \
        -H "Content-Type: application/json" -d '{
            "url": "https://docs.dbgpt.site/docs/awel"
        }'
"""
from typing import Dict

from dbgpt._private.pydantic import BaseModel, Field
from dbgpt.core.awel import DAG, HttpTrigger, MapOperator
from dbgpt.model.proxy import OpenAILLMClient
from dbgpt.rag.knowledge import KnowledgeType
from dbgpt.rag.operators import KnowledgeOperator, SummaryAssemblerOperator


class TriggerReqBody(BaseModel):
    url: str = Field(..., description="url")


class RequestHandleOperator(MapOperator[TriggerReqBody, Dict]):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    async def map(self, input_value: TriggerReqBody) -> Dict:
        params = {
            "url": input_value.url,
        }
        print(f"Receive input value: {input_value}")
        return params


# 构造 DAG
with DAG("dbgpt_awel_simple_rag_summary_example") as dag:
    # 构造一个DAG后，需要输入到这个触发器中，才能触发这个DAG，也就是要输入到DAG中的第一个节点，数据
    trigger = HttpTrigger( # 构造一个http触发器，用于接收http请求，并将请求参数转换为TriggerReqBody对象，方便在HttpTrigger（这个触发器）中处理这个请求
        # 第一个URL请求参数，是这个触发器（server）需要的一个参数；
        "/examples/rag/summary", methods="POST", request_body=TriggerReqBody
    )


    # 构造算子，执行数据的后续处理操作：此算子为一个MapOperator，将输入的字典对象中的url字段提取出来;解析参数
    path_operator = MapOperator(lambda request: request["url"])


    # 构造算子，在RequestHandleOperator（这个算子）中处理这个请求，这个算子是在处理请求时才会使用；即 server 相应上述请求
    request_handle_task = RequestHandleOperator()


    # build knowledge operator
    # 构造算子，执行数据的后续处理操作：此算子为一个KnowledgeOperator，将输入的url字段转换为一个Knowledge对象；同时声明知识库存储的地址的URL
    knowledge_operator = KnowledgeOperator(knowledge_type=KnowledgeType.URL.name)

    # build summary assembler operator
    summary_operator = SummaryAssemblerOperator(llm_client=OpenAILLMClient(), language="en")


    # 这些操作符通过 >> 符号连接起来，形成一个工作流。
    # >> 表示依赖关系，也就是这个算子的输入是上一个算子的输出
    (
        trigger
        >> request_handle_task
        >> path_operator
        >> knowledge_operator
        >> summary_operator
    )


if __name__ == "__main__":
    # 运行工作流
    tmp = dag.leaf_nodes[0].dev_mode
    if tmp:
        # Development mode, you can run the dag locally for debugging.
        from dbgpt.core.awel import setup_dev_environment
        setup_dev_environment([dag], port=5555)
    else:
        pass
