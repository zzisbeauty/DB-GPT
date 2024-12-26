from dbgpt.core.awel import DAG, MapOperator



# 自定义 DAG 上下文管理器
with DAG("awel_hello_world") as dag:
    task = MapOperator(map_function=lambda x: print(f"Hello, {x}!")) # operator 接受的是一个 func
task._blocking_call(call_data="world")