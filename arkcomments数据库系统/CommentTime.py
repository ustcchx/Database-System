from asyncio.windows_events import NULL
import pymysql
import time
import datetime

def get_db():
    try:
        db = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="wakd2008", db="arkcomments", charset = "utf8")
    except:
        db = None

    return db
#CommentTime将存储用户最近一次对表格操作以达到监管目的。


#根据UID查找用户操作记录
def select_Record(UID):
    db = get_db()
    cursor = db.cursor()
    sql="SELECT CTime,Operate,Ctable FROM commenttime WHERE UID = '%s' "%(UID)
    try:
   # 执行sql语句
        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        print(results)
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

    return results



#和记录管理员的表格类似，只是存储了操作类型和操作表
def write_Time(UID,currenttime,operate,table):
    db = get_db()
    cursor = db.cursor()
    gap=datetime.timedelta(seconds=20)
    if select_Record(UID)==():
        sql="INSERT INTO commenttime VALUES('%s','%s','%s','%s')"%(UID,currenttime,operate,table)
    else:
        if (currenttime-select_Record(UID)[0][0])<gap:
            print(currenttime-select_Record(UID)[0][0])
            return '频繁'
        else:
            sql="UPDATE commenttime SET CTime = '%s',operate='%s',Ctable='%s' WHERE UID = '%s'"%(currenttime,operate,table,UID)
    try:
   # 执行sql语句
        print(sql)
        cursor.execute(sql)
        db.commit()
        return '操作成功'
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()