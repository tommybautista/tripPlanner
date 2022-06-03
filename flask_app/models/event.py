from datetime import date
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash


class Event:
    db_name = 'trip_planner2'

    def __init__(self,db_data):
        self.id = db_data['id']
        self.date = db_data['date']
        self.breakfast = db_data['breakfast']        
        self.morning = db_data['morning']
        self.lunch = db_data['lunch']        
        self.afternoon = db_data['afternoon']
        self.dinner = db_data['dinner']        
        self.evening = db_data['evening']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']


    @classmethod
    def save(cls,data):
        query = "INSERT INTO events (date, breakfast, morning, lunch, afternoon, dinner, evening, user_id) VALUES (%(date)s, %(breakfast)s, %(morning)s, %(lunch)s, %(afternoon)s, %(dinner)s, %(evening)s, %(user_id)s);"
        return connectToMySQL(cls.db_name).query_db(query, data)  

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM events;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_events = []
        for row in results:
            all_events.append( cls(row) )
        return all_events
    

    @classmethod
    def update(cls, data):
        query = 'UPDATE events SET breakfast = %(breakfast)s, morning = %(morning)s, lunch = %(lunch)s, afternoon = %(afternoon)s, dinner = %(dinner)s, evening = %(evening)s WHERE id = %(id)s;'
        return connectToMySQL(cls.db_name).query_db(query, data)


    @classmethod
    def destroy(cls,data):
        query  = "DELETE FROM events WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query, data)

    # @classmethod
    # def get_one(cls, data):
    #     query = 'SELECT * FROM events WHERE id = %(id)s;'
    #     results =  connectToMySQL(cls.db_name).query_db(query, data)
    #     if len(results) < 1:
    #         return False
    #     return cls(results[0])

    @classmethod
    def get_events_by_user(cls, data):
        query = 'SELECT * FROM events WHERE user_id = %(id)s ORDER BY date ASC;'
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        all_events = []
        for row in results:
            all_events.append(cls(row))
            if len(all_events) < 1:
                return False
        return all_events

    @classmethod
    def get_one(cls, data):
        query = 'SELECT * FROM events WHERE id = %(id)s;'
        results =  connectToMySQL(cls.db_name).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
    

