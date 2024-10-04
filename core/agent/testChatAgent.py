import erniebot
import unittest
from unittest.mock import MagicMock


def test_chat_with_memory_ret():
    erniebot.api_type = 'aistudio'
    erniebot.access_token = 'e78006946e211683837a6bf32c63788166e55c7c'  # 替换为你自己的 Access Token

    # 调用文心大模型的流式 API
    response = erniebot.ChatCompletion.create(
        model="ernie-3.5", 
        messages=[{
            "role": "user",
            "content": """
                你是一个专业的论文摘要员,使用中文进行任务处理,你精通各个领域的论文,你需要根据给定的论文内容,提供相应的摘要总结,同时对论文给出相应的一级标签、二级标签,具体来说你的任务如下:
                1. 首先,为了后续的数据处理,你的回答必须是统一格式的,这点十分重要,你的回复只能是单条JSON格式的输出,除此以外不要出现任何多余的内容.
                2. 我给你提供的是一篇论文部分相对重要的内容,你需要根据这部分内容,提供一个详细的总结,确保你的总结准确无误,并且尽可能的详细.几个比较基础的点是: 论文的主要贡献、创新方法、实验结果、深入分析、重大进展等等.
                3. 总结完成内容后,你需要对论文进行一级、二级归类以及给出论文的相应的标签,一级归类是他的大领域(如Computer Science)，二级归类是子领域(如Artificial Intelligence)，具体的归类使用ArXiv的分类体系. 标签是指这篇论文具体的方向,如联邦学习、联邦学习攻击、图神经网络等等.
                4. 如果提供的内容不存在你任务需要的信息，不要省略字段,将那个JSON字段置为空字符串即可,你的回答要以大括号开始、以大括号结束,你的回答必须包含"Abstract", "Primary Classification", "Secondary Classification", "Research Direction Tags"字段!
                
                >>>
                为了让你更理解你的任务，这是一个输出的模板,即一条JSON格式的输出,不要关注它具体的内容，你只需按照相同的格式对我给你的论文进行分析:
                    {{
                        "Abstract": "论文的主要贡献、创新方法、实验结果、深入分析、重大进展等等",
                        "Primary Classification": "",
                        "Secondary Classification": "",
                        "Research Direction Tags": ["", "", "", ""]
                    }}
                <<<
                >>>
                如果你理解了你的任务,请开始你的工作,我给你的论文内容如下:
                {Multimodal and crossmodal representation learning from textual and visual features with bidirectional deep neural networks for video hyperlinking. In Proceedings of the 2016 ACM workshop on Vision and Language Integration Meets Multimedia Fusion. 37–44. [59] Kangkang Wang, Rajiv Mathews, Chloé Kiddon, Hubert Eichner, Françoise Beau- fays, and Daniel Ramage. 2019. Federated evaluation of on-device personalization. arXiv preprint arXiv:1910.10252 (2019). [60] Qiang Yang, Yang Liu, Tianjian Chen, and Yongxin Tong. 2019. Federated machine learning: Concept and applications. ACM Transactions on Intelligent Systems and Technology (TIST) 10, 2 (2019), 1–19. [61] Timothy Yang, Galen Andrew, Hubert Eichner, Haicheng Sun, Wei Li, Nicholas Kong, Daniel Ramage, and Françoise Beaufays. 2018. Applied federated learning: Improving google keyboard query suggestions. arXiv preprint arXiv:1812.02903 (2018). [62] Tao Yu, Eugene Bagdasaryan, and Vitaly Shmatikov. 2020. Salvaging federated learning by local adaptation. arXiv preprint arXiv:2002.04758 (2020). [63] Yue Zhao, Meng Li, Liangzhen Lai, Naveen Suda, Damon Civin, and Vikas Chan- dra. 2018. Federated learning with non-iid data. arXiv preprint arXiv:1806.00582 (2018).'), Document(metadata={'documentID': '8d23cb29c7007b5dd42862db137588ec', 'knowledge_name': '322cf80c-80b7-11ef-b964-00163e2b4d96', 'page_number': 7, 'source': '/home/workspace/baiducup/PaperQuery_Backend/res/pdf/Liu 等 - 2021 - PFA Privacy-preserving Federated Adaptation for E.pdf'}, page_content='Rw represent different domains. Method Ar Cl Pr Rw Avg Baseline 51.03 46.18 72.97 64.09 58.57 Fine-tune 54.32 52.59 77.37 65.94 62.55 KD 56.17 54.53 78.38 67.08 64.04 EWC 54.94 54.19 78.71 66.39 63.56 Ours 58.02 58.79 79.95 68.57 66.33 Note that all these methods are conducted in a single device, failing to borrow the useful knowledge existed in other devices. 5.2 RQ1: Overall Results Before applying personalization, we first need to implement tra- ditional FL to generate a federated model. Towards our simulated FL datasets, we observe that using FL alone cannot achieve a good performance. To give a more direct understanding, we visualize the training process for the two types of datasets on MobileNetV2.'), Document(metadata={'documentID': '8d23cb29c7007b5dd42862db137588ec', 'knowledge_name': '322cf80c-80b7-11ef-b964-00163e2b4d96', 'page_number': 11, 'source': '/home/workspace/baiducup/PaperQuery_Backend/res/pdf/Liu 等 - 2021 - PFA Privacy-preserving Federated Adaptation for E.pdf'}, page_content='114, 13 (2017), 3521– 3526. [30] Jakub Konečn`y, H Brendan McMahan, Felix X Yu, Peter Richtárik, Ananda Theertha Suresh, and Dave Bacon. 2016. Federated learning: Strategies for improving communication efficiency. arXiv preprint arXiv:1610.05492 (2016). [31] Alex Krizhevsky, Geoffrey Hinton, et al. 2009. Learning multiple layers of features from tiny images. (2009). [32] Yann LeCun, Léon Bottou, Yoshua Bengio, and Patrick Haffner. 1998. Gradient- based learning applied to document recognition. Proc. IEEE 86, 11 (1998), 2278– 2324. [33] Xiang Li, Kaixuan Huang, Wenhao Yang, Shusen Wang, and Zhihua Zhang. 2019. On the convergence of fedavg on non-iid data. arXiv preprint arXiv:1907.02189 (2019). [34] Tsung-Yi Lin, Priya Goyal, Ross Girshick, Kaiming He, and Piotr Dollár. 2017. Focal loss for dense object detection. In Proceedings of the IEEE international conference on computer vision. 2980–2988. [35] Bingyan Liu, Yifeng Cai, Yao Guo, and Xiangqun Chen. 2021. TransTailor: Pruning the Pre-trained Model for Improved Transfer Learning. arXiv preprint arXiv:2103.01542 (2021). [36] Bingyan Liu, Yao Guo, and Xiangqun Chen. 2019. WealthAdapt: A general network adaptation framework for small data tasks. In Proceedings of the 27th ACM International Conference on Multimedia. 2179–2187. [37] Bingyan Liu, Yuanchun Li, Yunxin Liu, Yao Guo, and Xiangqun Chen. 2020. PMC: A Privacy-preserving Deep Learning Model Customization Framework for Edge Computing. Proceedings of the ACM on Interactive, Mobile, Wearable and Ubiquitous Technologies 4, 4 (2020), 1–25. [38] Aravindh Mahendran and Andrea Vedaldi. 2015. Understanding deep image rep- resentations by inverting them. In Proceedings of the IEEE conference on computer vision and pattern recognition. 5188–5196. [39] Yishay Mansour, Mehryar Mohri, Jae Ro, and Ananda Theertha Suresh. 2020. Three approaches for personalization with applications to federated learning. arXiv preprint arXiv:2002.10619 (2020). [40] Brendan McMahan, Eider Moore, Daniel Ramage, Seth Hampson, and Blaise Aguera y Arcas. 2017. Communication-efficient learning of deep net- works from decentralized data. In Artificial Intelligence and Statistics. PMLR, 1273–1282. [41] Luca Melis, Congzheng Song, Emiliano De Cristofaro, and Vitaly Shmatikov. 2019. Exploiting unintended feature leakage in collaborative learning. In 2019 IEEE Symposium on Security and Privacy (SP)}

                """
        }], 
        stream=True
    )

    return response

   
# 运行测试
if __name__ == '__main__':
    response = test_chat_with_memory_ret()
    for i in response:
        print(i)
    answer = ""
    for r in response:
        answer += r["result"]

    print(answer)  
