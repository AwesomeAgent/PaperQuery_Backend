import erniebot

class LLM:
    def __init__(self):
        self.llms = {}

        # 设置文心大模型（ERNIE-Bot）的 API 类型和 Access Token
        erniebot.api_type = 'aistudio'
        erniebot.access_token = 'e78006946e211683837a6bf32c63788166e55c7c'  # 替换为你在百度 AI Studio 上生成的 Access Token

        # 将文心一言模型实例存入 llms 字典中
        self.llms['ernie'] = erniebot

        # 默认使用文心大模型
        self.chatllm = self.llms['ernie']

    def get_llm(self, name):
        return self.llms[name]

    def get_all_llms(self):
        return self.llms

    # 由于文心大模型不需要专门的 tokenizer，移除 tokenizer 相关的代码
    # 可以根据实际需求定义 token 相关的功能

    ## 将提示词发送给文心大模型（ERNIE-Bot），获取回复
    def chat_with_llm(self, chat_prompt):
        print(f"Sending prompt: {chat_prompt}")
        max_retries = 5
        retries = 0
        
        # 定义文心大模型消息格式
        messages = [{'role': 'user', 'content': chat_prompt}]
        
        while retries < max_retries:
            try:
                # 调用文心大模型 API，获取响应
                response = self.chatllm.ChatCompletion.create(
                    model='ernie-3.5',  # 文心大模型的版本
                    messages=messages
                )
                # 返回模型的结果
                return response.get_result()

            except Exception as e:
                retries += 1
                print(f"Error: {e}")
                if retries == max_retries:
                    print("Max retries reached. Exiting...")
                    return None
                print(f"Retrying... (Attempt {retries})")


