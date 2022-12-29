from model.dbQuery import dbQuery

# https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
# https://tutswiki.com/read-write-config-files-in-python/

class Admin():
    def __init__(self):
        self.db = dbQuery()

    def identification(self, email, pwd):
        query = "SELECT name, email, role_id FROM user WHERE  email=%s AND password=%s"
        print(query)
        arg = (email, pwd)
        print(arg)
        return self.db.fetch(query, arg)

    def createUser(self,  name, lastname, email, pwd, role):
        query = 'INSERT INTO user (name, lastname, email, password, role_id) VALUES (%s, %s, %s, %s, %s)'
        arg = (name,lastname, email, pwd, role)
        return self.db.insert(query, arg)

    def updateUser(self):
        pass

    def deleteUser(self):
        pass

    def getRole(self):
        return self.db .fetch('SELECT id,name FROM role', '')
