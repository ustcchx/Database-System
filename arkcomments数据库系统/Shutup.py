from asyncio.windows_events import NULL
import imp
from unittest import result
import pymysql
import time
import datetime
def get_db():
    try:
        db = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="wakd2008", db="arkcomments", charset = "utf8")
    except:
        db = None

    return db

#展示所有禁言情况
def search_ALLShutup():
    db = get_db()
    cursor = db.cursor()
    sql = "select * from Shutup "
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

#查询禁言截止时间，user能操作
def select_Shutup(UID):
    db = get_db()
    cursor = db.cursor()
    sql = "select EndTime from Shutup WHERE UID='%s'"(UID)
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

def insert_Shutup(UID,EndTime):
    db = get_db()
    cursor = db.cursor()
    sql="INSERT INTO Shutup VALUES('%s','%s')"(UID,EndTime)
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

def delete_Shutup(UID):
    db = get_db()
    cursor = db.cursor()
    sql = "DELETE FROM Shutup WHERE UID = '%s'"%(UID)
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

