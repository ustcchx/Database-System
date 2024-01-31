from asyncio.windows_events import NULL
import imp
import pymysql
import time
import datetime
from CommentTime import select_Record,write_Time
from user import check_talk
def get_db():
    try:
        db = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="wakd2008", db="arkcomments", charset = "utf8")
    except:
        db = None

    return db
#EComment有8个属性，依次为
#CID int AI PK 
#EID int 
#UID int 
#Content varchar(50) 
#Ctime datetime 
#Strength int 
#Hate int 
#Oname varchar(10)

#查找表格中所有评论
def search_ALLECommment():
    db = get_db()
    cursor = db.cursor()
    sql = "select * from EComment"
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

#根据CID查找对应评论
def search_CIDECommmen(CID):
    db = get_db()
    cursor = db.cursor()
    sql = "select * FROM EComment WHERE CID = '%s' "%(CID)
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

#根据UID查找用户发的所有评论
def search_UIDEComment(UID):
    db = get_db()
    cursor = db.cursor()
    sql=sql="SELECT CID,Ename,Ctime,Content,Strength,Hate FROM EComment,enemy WHERE UID = '%s' and EComment.EID=enemy.EID"%(UID)
    try:
   # 执行sql语句
        print(sql)
        cursor.execute(sql)
        results = cursor.fetchall()
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

    return results

#根据EID查找所有评论
def search_EIDEComment(EID):
    db = get_db()
    cursor = db.cursor()
    sql="SELECT CID,Content,Strength,Hate,Uname,Ctime FROM EComment,userpeople WHERE EID = '%s' and EComment.UID=userpeople.UID ORDER BY CID DESC"%(EID)
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

#根据正在操作的评论UID判断是否是自己写的，将在下面被调用
def checkUID(UID,CID):
    check=search_CIDECommmen(CID)
    if int(UID)==int(check[0][2]):
        return False
    else:
        return True


#根据正在操作的用户写评论
def write_EComment(EID,UID,Concent,Strength,Hate):
    if check_talk(UID):
        return '您已被禁言'
    db = get_db()
    cursor = db.cursor()
    if len(search_ALLECommment())<1:
        CID=10001
    else:
        CID=NULL
    timestamp = int(time.time())
    currenttime=datetime.datetime.fromtimestamp(timestamp)
    if write_Time(UID,currenttime,'插入','EComment')=='频繁':
        return '操作频繁'
    sql="INSERT INTO EComment VALUES('%s','%s','%s','%s','%s','%s','%s')"%(CID,EID,UID,Concent,currenttime,Strength,Hate)
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

#根据正在操作的用户删除评论
def delete_EComment(CID,UID):
    db = get_db()
    cursor = db.cursor()
    #只允许删除自己的
    if checkUID(UID,CID):
        return '非本人评论'
    timestamp = int(time.time())
    currenttime=datetime.datetime.fromtimestamp(timestamp)
    if write_Time(UID,currenttime,'删除','EComment')=='频繁':
        return '操作频繁'
    sql="DELETE FROM EComment WHERE CID = '%s'"%(CID)
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

#根据正在操作的用户修改评论
def update_EComment(CID,UID,Concent,Strength,Hate):
    if check_talk(UID):
        return '您已被禁言'
    db = get_db()
    cursor = db.cursor()
    #只允许修改自己的
    if checkUID(UID,CID):
        return '非本人评论'
    timestamp = int(time.time())
    currenttime=datetime.datetime.fromtimestamp(timestamp)
    if write_Time(UID,currenttime,'修改','EComment')=='频繁':
        return '操作频繁'
    sql="UPDATE EComment SET Content = '%s', Ctime = '%s', Strength = '%s', Hate = '%s' WHERE CID = '%s'"%(Concent,currenttime,Strength,Hate,CID)
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