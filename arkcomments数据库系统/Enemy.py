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
#EID int AI PK 
#Ename varchar(10) 
#Ekind varchar(10) 
#Elevel varchar(10) 
#Eaction varchar(10) 
#Eattack char(1) 
#Erecovery char(1) 
#Emagic char(1)

#查找所有敌方单位
def search_ALLEnemy():
    db = get_db()
    cursor = db.cursor()
    sql = "select * from enemy "
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
def select_Enemy(EID):
    db = get_db()
    cursor = db.cursor()
    sql = "select * from enemy WHERE EID='%s'"%(EID)
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

def select_Enemyname(Ename):
    db = get_db()
    cursor = db.cursor()
    sql = "select * from Enemy WHERE Ename LIKE %s"
    try:
   # 执行sql语句
        print(sql)
        cursor.execute(sql, ('%' + Ename + '%',))
        results = cursor.fetchall()
        print(results)
        # 执行sql语句
        db.commit()
    except:
        # 发生错误时回滚
        db.rollback()
    cursor.close()

    return results

def insert_Enemy(Ename,Ekind,Elevel,Eendure,Eattack,Erecovery,Emagic):
    db = get_db()
    cursor = db.cursor()
    if len(search_ALLEnemy())<1:
        EID=10001
    else:
        EID=NULL
    sql = "INSERT INTO enemy VALUES('%s','%s','%s','%s','%s','%s','%s','%s')"%(EID,Ename,Ekind,Elevel,Eendure,Eattack,Erecovery,Emagic)
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


def delete_Enemy(EID):
    db = get_db()
    cursor = db.cursor()
    sql1='SET FOREIGN_KEY_CHECKS=0'
    sql = "DELETE FROM enemy WHERE EID = '%s'"%(EID)
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

def update_Enemy(EID,Ename,Ekind,Elevel,Eendure,Eattack,Erecovery,Emagic):
    db = get_db()
    cursor = db.cursor()
    sql = "UPDATE enemy SET Ename = '%s',Ekind = '%s',Elevel = '%s',Eendure = '%s',\
    Eattack = '%s',Erecovery = '%s',Emagic = '%s' WHERE EID = '%s'"%(Ename,Ekind,Elevel,Eendure,Eattack,Erecovery,Emagic,EID)
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
