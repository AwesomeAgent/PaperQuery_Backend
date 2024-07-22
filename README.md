<!--
 * @Description: 
 * @Author: qwrdxer
 * @Date: 2024-07-22 21:48:10
 * @LastEditTime: 2024-07-22 21:48:43
 * @LastEditors: qwrdxer
-->
## 论文助手后端
todo: 增加向量化

todo:  增加条件过滤

创建 .env文件
```bash
## API
OPENAI_API_KEY="sk-WMwF3ZICC7ebCTTyC57c38Ff2b4246Ce8108A6DcF8B045C7"
OPENAI_API_BASE="https://api.v3.cm/v1/"

## 目录相关
CHROMA_LAYER1_DIR="C:\Users\qwrdxer\Desktop\AcadeAgent\res\layer1"
CHROMA_LAYER2_DIR="C:\Users\qwrdxer\Desktop\AcadeAgent\res\layer2"

PAPER_SAVE_DIR="C:\Users\qwrdxer\Desktop\AcadeAgent\res\pdf"

#JWT
SECRET_KEY = "sk-IBcCSHhyiEKZGHVv6bE4Fc5045Dd459aA01366057a834aDb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60000
```

修改
`AcadeAgent\core\backend\database.py` 的dbpath