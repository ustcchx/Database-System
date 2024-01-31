from asyncio.windows_events import NULL
from pickle import TRUE
import pymysql
from Report import insert_Report
def get_db():
    try:
        db = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="wakd2008", db="arkcomments", charset = "utf8")
    except:
        db = None

    return db


def user_login(Uname, Upassword):
    db = get_db()
    cursor = db.cursor()
    sql = "SELECT UID FROM Userpeople WHERE Uname = '%s' && Upassword = '%s'"% \
       (Uname, Upassword)
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

#查找所有用户
def select_ALLuser():
    db = get_db()
    cursor = db.cursor()
    sql = "SELECT * FROM Userpeople "
    try:
   # 执行sql语句
        cursor.execute(sql)
        user = cursor.fetchall()
        print(user)
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

    return user

#注册
def register(Uname,Upassword,UgameID):
    db = get_db()
    cursor = db.cursor()
    if len(select_ALLuser())<1:
        UID=10001
    else:
        UID=NULL
    sql1 = "INSERT INTO userpeople  (UID,Uname,Upassword,UgameID) VALUES('%s','%s','%s','%s')"%(UID,Uname,Upassword,UgameID)
    sql2='SELECT MAX(UID) FROM userpeople'
    try:
   # 执行sql语句
        cursor.execute(sql1)   
        cursor.execute(sql2)
        user = cursor.fetchall()
        # 执行sql语句
        db.commit()
        return user
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

def select_user(UID):
    db = get_db()
    cursor = db.cursor()
    sql = "SELECT * FROM Userpeople WHERE UID = '%s' "%(UID)
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

def update_user(UID,Uname,Upassword,Usign,UgameID,Usex):
    db = get_db()
    cursor = db.cursor()
    sql = "update userpeople SET Uname = '%s',Upassword = '%s', Usign = '%s', UgameID = '%s', Usex= '%s' WHERE UID = '%s'"%(Uname,Upassword,Usign,UgameID,Usex,UID)
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






def check_talk(UID):
    user=select_user(UID)
    if user[0][-1]:
        return True
    else:
        return False


def ReportComment(UIDoffer,UIDget,CID,Ctable):
    insert_Report(UIDoffer,UIDget,CID,Ctable)





def db_close():
    db = get_db()
    if db is not None:
        db.close()

if __name__ == "__main__":
    db_close()