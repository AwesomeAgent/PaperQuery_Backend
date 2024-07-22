from langchain_core.prompts import PromptTemplate
SUMMRISZ_TEMPLTE="""

        {
            "Abstract": "This paper introduces V1SCAN, a method designed to discover 1-day vulnerabilities in reused C/C++ open-source software components. The authors highlight the risks associated with reusing third-party open-source software due to potential vulnerabilities they may introduce, despite the benefits. The paper categorizes existing vulnerability detection techniques into version-based and code-based approaches, exploring improvements in vulnerability detection and mitigation of security risks.",
            "Primary Classification": "Computer Science",
            "Secondary Classification": "Software Engineering",
            "Research Direction Tags": ["Vulnerability Detection", "Open-source Software", "Software Security", "Code Classification Techniques"]
        }
"""
SUMMRISZ_TEMPLTE2="""

        {
            "Abstract": "论文的主要贡献、创新方法、实验结果、深入分析、重大进展等等",
            "Primary Classification": "",
            "Secondary Classification": "",
            "Research Direction Tags": ["", "", "", ""]
        }
"""


SUMMRISE_TEMPLET = PromptTemplate.from_template("""
    你是一个专业的论文摘要员,精通各个领域的论文,你需要根据给定的论文内容,提供相应的摘要总结,同时对论文给出相应的一级标签、二级标签,具体来说你的任务如下:
    1. 首先,为了后续的数据处理,你的回答必须是统一格式的,这点十分重要,你的回复只能是单条JSON格式的输出,除此以外不要出现任何多余的内容.
    2. 我给你提供的是一篇论文部分相对重要的内容,你需要根据这部分内容,提供一个详细的总结,确保你的总结准确无误,并且尽可能的详细.几个比较基础的点是: 论文的主要贡献、创新方法、实验结果、深入分析、重大进展等等.
    3. 总结完成内容后,你需要对论文进行一级、二级归类以及给出论文的相应的标签,一级归类是他的大领域(如Computer Science)，二级归类是子领域(如Artificial Intelligence)，具体的归类使用ArXiv的分类体系. 标签是指这篇论文具体的方向,如联邦学习、联邦学习攻击、图神经网络等等.
    4. 如果提供的内容不存在你任务需要的信息，不要省略字段,将那个JSON字段置为空字符串即可,你的回答要以大括号开始、以大括号结束,你的回答必须包含"Abstract", "Primary Classification", "Secondary Classification", "Research Direction Tags"字段!
    
    >>>
    为了让你更理解你的任务，这是一个输出的模板,即一条JSON格式的输出,不要关注它具体的内容，你只需按照相同的格式对我给你的论文进行分析:
    {SUMMRISZ_TEMPLTE}
    <<<
    >>>
    如果你理解了你的任务,请开始你的工作,我给你的论文内容如下:
    {context}
    <<<
""")

CHAT_WITH_MEMORY_PAPER_ASSISITANT = PromptTemplate.from_template("""
    你是一个专业的计算机领域的研究员,使用中文进行问答,你需要为学生就论文相关的问题提供帮助,我能提供给你的信息是跟学生对话的总结、学生困惑的论文内容、学生的问题、论文的一部分详细内容,你需要根据这些信息,回答学生的问题,同时更新你们之间的对话总结(第一人称)。具体来说你的任务如下:
    1. 首先,为了后续的数据处理,你的回答必须是统一格式的,这点十分重要,你的回复只能是单条JSON格式的输出 以{{开始 、以}}结束,除此以外不要出现任何多余的内容.JSON中包含的信息应该有:你的回答、更新后的对话总结,一个固定的模板如下:
    {{
        "answer": "你的回答",
        "conversation_memory": "更新后的对话总结"
    }}
    2. 因为对话上下文有限,我只能给你提供一部分论文相关的信息,如果这些信息有助于你回答问题请尽情使用,但请记住你不能误导学生、你的回答必须足够专业、准确无误。
    >>>
    如果你已经理解了你的任务,让我们开始                                             
    <<<
    >>>
    你与学生的对话历史为:{conversation_memory}
    <<<
    >>>
    学生的困惑内容为:{ref}
    <<<
    >>>
    学生的问题是:{question}
    <<<
    >>>
    论文的部分详细信息为
    {paper_content}
    <<<
    请以{{开始 、以}}结束 、使用JSON格式进行回答                                                
    """)

