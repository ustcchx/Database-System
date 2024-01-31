from asyncio.windows_events import NULL
import imp
import pymysql
import time
import datetime
def get_db():
    try:
        db = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="wakd2008", db="arkcomments", charset = "utf8")
    except:
        db = None

    return db
#8个特征    
#OID int AI PK 
#Oname varchar(10) 
#Oprofession varchar(10) 
#Ostar int 
#Olife int 
#Oattack int 
#Orecovery int 
#Omagic int

#查找所有干员单位
def search_ALLOperator():
    db = get_db()
    cursor = db.cursor()
    sql = "select * from Operator "
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

#根据ID查找
def select_Operator(OID):
    db = get_db()
    cursor = db.cursor()
    sql = "select * from Operator WHERE OID='%s'"%(OID)
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

def select_Operatorname(Oname):
    db = get_db()
    cursor = db.cursor()
    sql = "select * from Operator WHERE Oname LIKE %s"
    try:
   # 执行sql语句
        print(sql)
        cursor.execute(sql, ('%' + Oname + '%',))
        results = cursor.fetchall()
        print(results)
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

    return results

def insert_Operator(Oname,Oprofession,Ostar,Olife,Oattack,Orecovery,Omagic):
    db = get_db()
    cursor = db.cursor()
    if len(search_ALLOperator())<1:
        OID=10001
    else:
        OID=NULL
    sql = "INSERT INTO operator VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"%(OID,Oname,Oprofession,Ostar,Olife,Oattack,Orecovery,Omagic)
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


def delete_Operator(OID):
    db = get_db()
    cursor = db.cursor()
    sql1='SET FOREIGN_KEY_CHECKS=0'
    sql = "DELETE FROM operator WHERE OID = '%s'"%(OID)
    sql2='SET FOREIGN_KEY_CHECKS=1'
    try:
   # 执行sql语句
        print(sql)
        cursor.execute(sql1)
        cursor.execute(sql)
        cursor.execute(sql2)
        # 执行sql语句
        db.commit()
        return '操作成功'
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

def update_Operator(OID,Oname,Oprofession,Ostar,Olife,Oattack,Orecovery,Omagic):
    db = get_db()
    cursor = db.cursor()
    sql = "UPDATE operator SET Oname = '%s',Oprofession = '%s',Ostar = '%s',Olife = '%s',\
    Oattack = '%s',Orecovery = '%s',Omagic = '%s' WHERE OID = '%s'"%(Oname,Oprofession,Ostar,Olife,Oattack,Orecovery,Omagic,OID)
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

def db_close():
    db = get_db()
    if db is not None:
        db.close()

if __name__ == "__main__":
    db_close()





def db_close():
    db = get_db()
    if db is not None:
        db.close()

if __name__ == "__main__":
    db_close()