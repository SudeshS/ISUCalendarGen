class DatabaseConnection:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.connection = self.createConnection()


    def createConnection(self):
        pass


    def getConnection(self):
        return self.connection

    
    def closeConnection(self):
        pass

