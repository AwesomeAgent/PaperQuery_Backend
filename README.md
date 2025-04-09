<!--
 * @Description: 
 * @Author: qwrdxer
 * @Date: 2024-07-22 21:48:10
 * @LastEditTime: 2024-07-22 21:48:43
 * @LastEditors: qwrdxer
-->
## 论文助手后端

### 前端repo
https://github.com/AwesomeAgent/PaperQuery_Frontend

### 项目演示视频

https://www.bilibili.com/video/BV1fH23YnE3w/

### 项目简介
用户可以将自己的论文上传到本系统中， 系统会结合大模型对文档进行处理、 切片、 向量化、
标签。 上传完成后， 用户可以在本系统中阅读论文， 系统提供翻译和智能问答功能， 用户的
问题可以随时发送给大模型，结合 RAG 技术，大模型可以给出准确的回答。
使用 Langchain、chroma 实现 Agent 部分,拥有记忆、RAG、文档向量化处理功能
 
### 技术栈
- fastapi
- langchain
- chromadb

## 使用方式

初始化
```bash
bash clean.sh
#删除库文件,创建新的表
```
创建 .env文件,编写如下配置
```bash
## API
OPENAI_API_KEY=""
OPENAI_API_BASE="https://api.v3.cm/v1/"

## 目录相关
CHROMA_LAYER1_DIR="/home/PaperQuery_Backend/res/layer1"
CHROMA_LAYER2_DIR="/home/PaperQuery_Backend/res/layer2"

PAPER_SAVE_DIR="/home/PaperQuery_Backend/res/pdf"

#JWT
SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60000

#数据库路径
DB_PATH="/home/PaperQuery_Backend/res/AcadeAgent/database.db"

#项目位置
AcadeAgent_DIR="/home/PaperQuery_Backend"
```

安装包
```
pip install -r requirement
```

开启两个终端分别运行
```
## 启动后端api服务
python main.py

## 运行向量化服务
python vector.py
```