import pymysql.cursors
import pymysql
from decouple import config
import os,logging,datetime


logger = logging.Logger('catch_all')

try:
    connection = pymysql.connect(host=config("DB_HOST"),
                             user=config("DB_USERNAME"),
                             password=config("DB_PASSWORD"),
                             db=config("DB_DATABASE"),
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    db = connection.cursor()
except (Exception) as error:
    print("Error while connecting to MySQL", error)
finally:
    pass

#This Class is Used to Perform CRUD Operations for a Table
class table:
    def __init__(self, tableName):
        try:
            schema = getSchemas()
            dictTables = []
            for row in schema:
                dictTables.append(row['TABLE_NAME'])
            if not tableName in dictTables:
                raise TypeError("Invalid Table Name Object")
            self.tableName = tableName
        except Exception as e:
            logger.error('Error: ' + str(e))
            
#Get All the Cloumns of the Selected Table Object 
    def getTableSchema(self,):
        try:
            db.execute("SELECT column_name,data_type FROM information_schema.columns  where table_name='%s' order by ordinal_position asc" % self.tableName)
            rst = db.fetchall()
            dictRow = []
            for rw in rst:
                dictRow.append(dict(rw))
            return dictRow
        except (Exception, pymysql.DatabaseError) as ex:
            logger.error('Error: ' + str(ex))
    
    #Get The Last Row in a Table Object
    def getLatest(self):
        try:
            db.execute("select *from %s order by id desc" % self.tableName)
            rst = dict(db.fetchone())
            return rst
        except (Exception, pymysql.DatabaseError) as ex:
            logger.error('Error: ' + str(ex))
    
     #Get One Columns Row in a Table Object
    def getOne(self,qryStr):
        try:
            rst = {}
            sqlStr = f"select {qryStr['column']} from {self.tableName} where {qryStr['where']}"
            db.execute(sqlStr)
            rst = db.fetchone()
            if rst is None:
                return False
            else:
               return dict(rst)
        except (Exception, pymysql.DatabaseError) as ex:
            logger.error('Error: ' + str(ex))
    
    def getRow(self,qryStr):
        try:
            rst = {}
            sqlStr = f"select * from {self.tableName} where {qryStr['where']}"
            db.execute(sqlStr)
            rst = db.fetchone()
            if rst is None:
                return False
            else:
               return dict(rst)
        except (Exception, pymysql.DatabaseError) as ex:
            logger.error('Error: ' + str(ex))
            
    #Get All Records From a Table
    def getAll(self):
        try:
            db.execute("select *from %s order by id asc" % self.tableName)
            rst = db.fetchall()
            return rst
        except (Exception, pymysql.DatabaseError) as ex:
            logger.error('Error: ' + str(ex))
    
    #Get Delete from Table Object
    def delete(self,where = []):
        rows_deleted = 0
        try:
           pars = "1=1"
           for param in where.keys():
                pars += f" and {param} = '{where[param]}'"
           sqlStr = f"delete from {self.tableName} where {pars}"
           db.execute(sqlStr)
           connection.commit()
           rows_deleted = db.rowcount
        except (Exception, pymysql.DatabaseError) as ex:
            logger.error('Error: ' + str(ex))
        
        return (rows_deleted,"Records Deleted")
    
    def exist(self,checkFld = []):
        sqlStr = f"SELECT EXISTS(SELECT 1 FROM {self.tableName} WHERE {checkFld[0]} = '{checkFld[1]}')"
        try:
            db.execute(sqlStr)
            return db.fetchone()
        except (Exception, pymysql.DatabaseError) as ex:
            logger.error('Error: ' + str(ex))
    #Insert Single Record
    def create(self,postData = []):
        curtime = datetime.datetime.now()
        postData['created_at'] = curtime.isoformat()
        postData['updated_at'] = curtime.isoformat()
        rowsAffected = 0
        try:
            flds = tuple((postData.keys()))
            tableFlds = ",".join([str(s) for s in flds])
            vals = tuple((postData.values()))
            sqlStr = f"insert into {self.tableName} ({tableFlds}) values {vals}".format(tableFlds,vals)
            db.execute(sqlStr)
            connection.commit()
            rowsAffected = db.rowcount
            
            return {'RowsAffected' : rowsAffected}
        except (Exception, pymysql.DatabaseError) as ex:
            logger.error('Error: ' + str(ex))

     #Update Record
    def update(self,postData = [], where = {}):
        curtime = datetime.datetime.now()
        postData['updated_at'] = curtime.isoformat()
        rowsAffected = 0
        try:
            pars = [' id = 0']
            if len(where) != 0:
                pars.pop(0)
            for param in where:
                pars.append(f"{param} = '{where[param]}'")
            whereStr = " and ".join([w for w in pars])
            upstr = [];
            for s in postData:
                upstr.append(f" {s} = '{postData[s]}'")
            upFlds = ",".join([g for g in upstr])
            sqlStr = f"update {self.tableName} set {upFlds} where {whereStr}".format(upFlds,whereStr)
            db.execute(sqlStr)
            connection.commit()
            rowsAffected = db.rowcount
            return (rowsAffected,' Rows Affected')
        except (Exception, pymysql.DatabaseError) as ex:
            logger.error('Error: ' + str(ex))
    
     #Insert Multiple Records
    def insert(self,postData = []):
        rowsAffected = 0
        try:
            vals = []
            for d in postData:
                vals.append(tuple(d.values()))

            flds = ",".join(map(str, postData[0]))
            tableFlds =  ",".join(map(str, vals))

            sqlStr = f"INSERT INTO {self.tableName} ({flds}) VALUES {tableFlds}"
            db.execute(sqlStr)
            connection.commit()
            rowsAffected = db.rowcount
            return (rowsAffected,' Rows Affected')
        except (Exception, pymysql.DatabaseError) as ex:
            logger.error('Error: ' + str(ex))

#Get Currentlt Connected Database
def getdbName():
    return config("DB_DATABASE")

# Get All Database Tables
def getSchemas():
    try:
        sqlStr = "SELECT table_name,table_type FROM information_schema.tables  where table_schema='%s'" % config("DB_DATABASE")
        db.execute(sqlStr)
        rst = db.fetchall()
        dictRow = []
        for rw in rst:
            dictRow.append(dict(rw))
        return dictRow
    except (Exception, pymysql.DatabaseError) as err:
        logger.error('Error: ' + str(err))

#Remove Reserve Table Fields from Insert Dictonary
def rsvFields(dictFields = []):
    rsvFields = ["id","created_at","updated_at"]
    try:
        for rsv in rsvFields:
            if rsv in dictFields:
                del dictFields[rsv]
    except (Exception) as ex:
            logger.error('Error: ' + str(ex))
    return dictFields