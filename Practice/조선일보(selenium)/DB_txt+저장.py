
# coding: utf-8

# In[12]:


import pymysql


# In[14]:


def dbConnect():
    conn = pymysql.connect(host='127.0.0.1', user='root', password='admin02',
                           db='python', charset='utf8')

    curs = conn.cursor()

    sql = "select * from chosunnews"
    curs.execute(sql)

    rows = curs.fetchall()
    conn.close()
    
    csvCreate(rows)
    
def csvCreate(rows):
    f = open("text_test.txt", 'w',encoding="utf8")
    for i in range(0,10):  # 임시로 10개의 행만 가져오게 설정
        content = rows[i][3]  # 본문내용만 가져오기
        f.write(content)
        f.write("\n")
    f.close()
    
dbConnect()    


# In[ ]:




