<!--
 * @Description: 
 * @Author: qwrdxer
 * @Date: 2024-07-22 21:48:10
 * @LastEditTime: 2024-07-22 21:48:43
 * @LastEditors: qwrdxer
-->
## 论文助手后端

使用百度杯的API进行后续开发

初始化
```bash
bash clean.sh
#删除库文件,创建新的表
```
创建 .env文件
```bash
## API
OPENAI_API_KEY="sk-WMwF3ZICC7ebCTTyC57c38Ff2b4246Ce8108A6DcF8B045C7"
OPENAI_API_BASE="https://api.v3.cm/v1/"

## 目录相关
CHROMA_LAYER1_DIR="/home/PaperQuery_Backend/res/layer1"
CHROMA_LAYER2_DIR="/home/PaperQuery_Backend/res/layer2"

PAPER_SAVE_DIR="/home/PaperQuery_Backend/res/pdf"

#JWT
SECRET_KEY = "sk-IBcCSHhyiEKZGHVv6bE4Fc5045Dd459aA01366057a834aDb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60000

#数据库路径
DB_PATH="/home/PaperQuery_Backend/res/AcadeAgent/database.db"

#项目位置
AcadeAgent_DIR="/home/PaperQuery_Backend"
```