from py2neo import Graph
from Helper import Helper


class Neo4jConnection:
    
    '''
    Get BOLT URL, username, pwd
    Create Session.
    Run queries through session.
    '''
    
    def __init__(self):
        self.uri = "bolt://localhost:7687"
        self.user = "neo4j"
        self.password = "neo4jneo4j"
        self.graph = None
        
    def connect(self):
        
        self.graph = Graph(self.uri, auth=(self.user, self.password))
        return self.graph
    
    def run(self, query):
        
        try:
            return self.graph.run(query)
        except:
            print("Invalid Query!")
            return -1
        

class File:
    
    def __init__(self, name: str, date_created, date_modified, file_format):
        
        self.properties = {}
        self.properties['name'] = name
        self.properties['date_created'] = date_created
        self.properties['date_modified'] = date_modified
        self.properties['file_format'] = file_format
        self.type = "Files"
        self.Help = Helper()
        
    def getProperties(self):
        
        return self.Help.formatProperties(self.properties)
        
        
class Keyword:
    
    def __init__(self, name, relationship):
        
        self.properties = {}
        self.properties['name'] = name
        self.relationship = relationship
        self.type = 'Keywords'
        self.Help = Helper()
        
    def getProperties(self):
        return self.Help.formatProperties(self.properties)
    
    def getRelationship(self):
        return self.relationship
        

class Nodes:
    
    def __init__(self, conn):
        self.conn = conn

    def delete(self, node: str, properties: str):
        
        query = "MATCH (m:" + node + " " + properties + ") DETACH DELETE m"
        return query

    def create(self, node: str, properties: str):
        
        query = "CREATE (n:" + node + " " + properties + ")"
        return query
    
    def update(self, node: str, properties: str):
        
        return self.delete(node, properties) + " " + self.create(node, properties)

    def check(self, node: str, properties: str):
        return 
    
    def connect_nodes(self, node1, node2, relationship):
        
        query = "MATCH (n1:" + node1.type + node1.getProperties() + "),"
        query += "(n2:" + node2.type + node2.getProperties() + ") "
        query += "CREATE (n1) - [:" + relationship + "] -> (n2)"
    
        return query
        
        