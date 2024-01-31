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
#OComment有8个属性，依次为
#CID int AI PK 
#OID int 
#UID int 
#Content varchar(50) 
#Ctime datetime 
#Strength int 
#Generic int 
#Syn int

#查找表格中所有评论
def search_ALLOCommment():
    db = get_db()
    cursor = db.cursor()
    sql = "select * from OComment"
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
def search_CIDOCommmen(CID):
    db = get_db()
    cursor = db.cursor()
    sql = "select * FROM OComment WHERE CID = '%s' "%(CID)
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

#根据UID查找用户发的所有评论
def search_UIDOComment(UID):
    db = get_db()
    cursor = db.cursor()
    sql="SELECT CID,Oname,Ctime,Content,Strength,Generic FROM OComment,operator WHERE UID = '%s' and OComment.OID=operator.OID"%(UID)
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

#根据OID查找所有评论
def search_OIDOComment(OID):
    db = get_db()
    cursor = db.cursor()
    sql="SELECT CID,Content,Strength,Generic,Uname,Ctime FROM OComment,userpeople WHERE OID = '%s' and OComment.UID=userpeople.UID ORDER BY CID DESC"%(OID)
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

#根据正在操作的评论UID判断是否是自己写的
def checkUID(UID,CID):
    check=search_CIDOCommmen(CID)
    print(UID)
    print(check[0][2])
    if int(UID)==int(check[0][2]):
        return False
    else:
        return True


#根据正在操作的用户写评论
def write_OComment(OID,UID,Concent,Strength,Generic):
    if check_talk(UID):
        return '您已被禁言'
    db = get_db()
    cursor = db.cursor()
    if len(search_ALLOCommment())<1:
        CID=10001
    else:
        CID=NULL
    timestamp = int(time.time())
    currenttime=datetime.datetime.fromtimestamp(timestamp)
    if write_Time(UID,currenttime,'插入','OComment')=='频繁':
        return '操作频繁'
    sql="INSERT INTO ocomment VALUES('%s','%s','%s','%s','%s','%s','%s')"%(CID,OID,UID,Concent,currenttime,Strength,Generic)
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
def delete_OComment(CID,UID):
    db = get_db()
    cursor = db.cursor()
    #只允许删除自己的
    if checkUID(UID,CID):
        return '非本人评论'
    timestamp = int(time.time())
    currenttime=datetime.datetime.fromtimestamp(timestamp)
    if write_Time(UID,currenttime,'删除','EComment')=='频繁':
        return '操作频繁'
    sql="DELETE FROM ocomment WHERE CID = '%s'"%(CID)
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
def update_OComment(CID,UID,Concent,Strength,Generic):
    if check_talk(UID):
        return '您已被禁言'
    db = get_db()
    cursor = db.cursor()
    #只允许修改自己的
    if checkUID(UID,CID):
        return '非本人评论'
    timestamp = int(time.time())
    currenttime=datetime.datetime.fromtimestamp(timestamp)
    if write_Time(UID,currenttime,'修改','OComment')=='频繁':
        return '操作频繁'
    sql="UPDATE OComment SET Content = '%s', Ctime = '%s', Strength = '%s', Generic = '%s' WHERE CID = '%s'"%(Concent,currenttime,Strength,Generic,CID)
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