from asyncio.windows_events import NULL
import imp
import pymysql
import time
import datetime
from AnnounceTime import write_Time
from Shutup import insert_Shutup
def get_db():
    try:
        db = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="wakd2008", db="arkcomments", charset = "utf8")
    except:
        db = None

    return db

#登录
def Administrator_login(AID, Apassword):
    db = get_db()
    cursor = db.cursor()
    sql = "SELECT Aname FROM administrator WHERE AID = '%s' && Apassword = '%s'"% \
       (AID, Apassword)
    try:
   # 执行sql语句
        cursor.execute(sql)
        name = cursor.fetchall()
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

    return name

def select_admin(AID):
    db = get_db()
    cursor = db.cursor()
    sql = "SELECT * FROM administrator WHERE AID = '%s' "%(AID)
    try:
   # 执行sql语句
        cursor.execute(sql)
        user = cursor.fetchall()
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()
    return user

def update_admin(AID,Aname,Apassword,Asign,AgameID,Asex):
    db = get_db()
    cursor = db.cursor()
    sql = "update administrator SET Aname = '%s',Apassword = '%s', Asign = '%s', AgameID = '%s', Asex= '%s' WHERE AID = '%s'"%(Aname,Apassword,Asign,AgameID,Asex,AID)
    try:
   # 执行sql语句
        print(sql)
        cursor.execute(sql)   
        # 执行sql语句
        db.commit()
        return '操作成功'
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

#实现禁言
#建立定时触发器，将在下个函数调用，作用是到时间自动接触禁言
def set_talk(UID,EndTime):
    db = get_db()
    cursor = db.cursor()
    sql1="CREATE EVENT '%sA' ON SCHEDULE AT TIMESTAMP '%s' DO update userpeople set Utalk=False where UID='%s'"(UID,EndTime,UID)
    sql2="CREATE EVENT '%sB' ON SCHEDULE AT TIMESTAMP '%s' DO DELETE FROM Shutup WHERE UID = '%s'"(UID,EndTime,UID)
    try:
   # 执行sql语句
        print(sql1)
        print(sql2)
        cursor.execute(sql1)
        cursor.execute(sql2)
        db.commit()
        return '操作成功'
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

#UID：被禁言用户UID，gaptime:datetime.datetime型数据，禁言时间
def Shutup_user(UID,gaptime:datetime.datetime):
    db = get_db()
    cursor = db.cursor()
    timestamp = int(time.time())
    currenttime=datetime.datetime.fromtimestamp(timestamp)
    EndTime=currenttime+gaptime
    sql="update userpeople set Utalk=True where UID='%s'"(UID)
    set_talk(UID,EndTime)
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