import sqlite3
import uuid
# 创建数据库连接
conn = sqlite3.connect('/data1/wyyzah-work/PaperQuery_Backend/res/AcadeAgent/database.db')
cursor = conn.cursor()

# 创建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS "users" (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) NOT NULL,  -- 定义为最多50个字符的变长字符串
    password VARCHAR(255) NOT NULL, -- 定义为最多255个字符的变长字符串
    lid TEXT NOT NULL
)
''')

userlid=uuid.uuid1()
knowledgeID1=uuid.uuid1()
knowledgeID2=uuid.uuid1()
knowledgeID3=uuid.uuid1()
# 插入数据
users_data = [
    ("admin", "123456", "admin"),
    ("user1", "123456", "1234"),
]

for user in users_data:
    cursor.execute('''
    INSERT INTO "users" (username, password, lid)
    VALUES (?, ?, ?)
    ''', user)

# 提交事务
conn.commit()

# 查询数据并打印
cursor.execute('SELECT * FROM "users"')
rows = cursor.fetchall()
for row in rows:
    print(row)


# 关闭连接
conn.close()

'''
@Description: 
@Author: qwrdxer
@Date: 2024-07-22 21:31:52
@LastEditTime: 2024-07-23 15:28:49
@LastEditors: qwrdxer
'''
import sqlite3
import uuid
from datetime import datetime, timezone

# 创建数据库连接
conn = sqlite3.connect('/data1/wyyzah-work/PaperQuery_Backend/res/AcadeAgent/database.db')
cursor = conn.cursor()

# 删除表（如果存在）
cursor.execute('''
DROP TABLE IF EXISTS documents
''')

# 创建表，增加时间戳列
cursor.execute('''
CREATE TABLE IF NOT EXISTS documents (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    uid VARCHAR(255) NOT NULL,
    knowledgeID VARCHAR(255) NOT NULL,
    lid VARCHAR(255) NOT NULL,
    documentName VARCHAR(255) NOT NULL,
    documentPath VARCHAR(255) NOT NULL,
    documentStatus INTEGER,
    documentVector INTEGER,
    primaryClassification VARCHAR(255),
    secondaryClassification VARCHAR(255),
    tags VARCHAR(255),
    documentDescription TEXT,
    createTime TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# 插入数据
papers_data = [
    ("uid1", "kid1", "lid1", "example.pdf", "/path/to/example.pdf", 1, 100, "Computer Science", "Artificial Intelligence", "machine learning, deep learning", "This is an example paper on machine learning.", datetime.now(timezone.utc)),
    ("uid2", "kid2", "lid2", "another_example.pdf", "/path/to/another_example.pdf", 2, 200, "Physics", "Quantum Mechanics", "quantum, research", "This is another example paper on quantum mechanics.", datetime.now(timezone.utc))
]

for paper in papers_data:
    cursor.execute('''
    INSERT INTO documents (uid, knowledgeID, lid, documentName, documentPath, documentStatus, documentVector, primaryClassification, secondaryClassification, tags, documentDescription, createTime)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', paper)

# 提交事务
conn.commit()

# 查询数据并打印
cursor.execute('SELECT * FROM documents')
rows = cursor.fetchall()
for row in rows:
    print(row)

# 关闭连接
conn.close()


import sqlite3
from datetime import datetime, timezone

# 创建数据库连接
conn = sqlite3.connect('/data1/wyyzah-work/PaperQuery_Backend/res/AcadeAgent/database.db')
cursor = conn.cursor()

# 删除表（如果存在）
cursor.execute('''
DROP TABLE IF EXISTS knowledges
''')

# 创建表，并增加时间戳列
cursor.execute('''
CREATE TABLE IF NOT EXISTS knowledges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    knowledgeID VARCHAR(255) NOT NULL,
    lid VARCHAR(255) NOT NULL,
    knowledgeName VARCHAR(255) NOT NULL,
    knowledgeDescription TEXT,
    documentNum INTEGER,
    vectorNum INTEGER,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

# 插入数据
knowledges_data = [
    (f"kid{i+1}", "admin", f"Knowledge {i+1}", f"Description of Knowledge {i+1}", i+1, (i+1) * 100, datetime.now(timezone.utc))
    for i in range(3)
]

for knowledge in knowledges_data:
    cursor.execute('''
    INSERT INTO knowledges (knowledgeID, lid, knowledgeName, knowledgeDescription, documentNum, vectorNum, timestamp)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', knowledge)

# 提交事务
conn.commit()

# 查询数据并打印
cursor.execute('SELECT * FROM knowledges')
rows = cursor.fetchall()
for row in rows:
    print(row)

# 关闭连接
conn.close()