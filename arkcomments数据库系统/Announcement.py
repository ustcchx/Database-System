from asyncio.windows_events import NULL
import imp
import pymysql
import time
import datetime
from AnnounceTime import write_Time
def get_db():
    try:
        db = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="wakd2008", db="arkcomments", charset = "utf8")
    except:
        db = None

    return db

#查找所有公告
def get_Announcement():
    db = get_db()
    cursor = db.cursor()
    sql = "select ANID,Announce,Atime,Aname from Announcement,Administrator WHERE Announcement.AID=Administrator.AID ORDER BY ANID DESC"
    try:
   # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

    return results

#根据ANID查找对应公告
def get_ann(ANID):
    db = get_db()
    cursor = db.cursor()
    sql = "select AID,Announce from Announcement WHERE ANID = '%s'"%(ANID)
    try:
   # 执行sql语句
        cursor.execute(sql)
        results = cursor.fetchall()
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

    return results

#查找某个管理员发的所有公告
def search_Announcement(AID):
    db = get_db()
    cursor = db.cursor()
    sql="SELECT ANID FROM announcement WHERE AID = '%s' "%(AID)
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

#根据正在操作的管理员写公告，调用了判断时间的write_Time函数，判断失败返回，成功将记录
def write_Announcement(AID,words):
    db = get_db()
    cursor = db.cursor()
    if len(get_Announcement())<1:
        ANID=10001
    else:
        ANID=NULL
    timestamp = int(time.time())
    currenttime=datetime.datetime.fromtimestamp(timestamp)
    if write_Time(AID,currenttime)=='频繁':
        return '操作频繁'
    sql="INSERT INTO Announcement VALUES('%s','%s','%s','%s')"%(ANID,AID,words,currenttime)
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

#根据正在操作的管理员删除公告
def delete_Announcement(ANID,AID):
    db = get_db()
    cursor = db.cursor()
    #只允许修改自己的
    check=get_ann(ANID)
    checkID=check[0][0]
    sql="DELETE FROM Announcement WHERE ANID = '%s'"%(ANID)
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

#根据正在操作的管理员修改公告
def update_Announcement(ANID,AID,words):
    db = get_db()
    cursor = db.cursor()
    #只允许修改自己的
    check=get_ann(ANID)
    checkID=check[0][0]
    if int(AID)!=int(checkID):
        return 'ERROR'
    sql="UPDATE Announcement SET Announce = '%s' WHERE ANID = '%s'"%(words,ANID)
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

def db_close():
    db = get_db()
    if db is not None:
        db.close()

if __name__ == "__main__":
    db_close()