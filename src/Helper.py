class Helper:
    
    def formatProperties(self, properties):
        
        query = "{"
        
        for key,val in properties.items():      
            query += key
            query += ":'"
            query += val + "',"
        query = query[:-1] + "}"
        
        return query