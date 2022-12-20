from model.dbQuery import dbQuery

# https://dev.mysql.com/doc/connector-python/en/connector-python-api-mysqlcursor-execute.html
# https://tutswiki.com/read-write-config-files-in-python/

class Admin():
    def __init__(self):
        self.db = dbQuery()
        pass

    def createUser(self,  name, lastname, email, pwd, role):
        r = 'INSERT INTO user (name, lastname, email, password, role_id) VALUES (%s, %s, %s, %s, %s)'
        data = (name,lastname, email, pwd, role)
        return self.db.insert(r, data)

    def updateUser(self):
        pass

    def deleteUser(self):
        pass
