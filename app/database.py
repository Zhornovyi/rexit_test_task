import csv
import sqlite3


class Database:
    def __init__(self, db_name="clients.db", source="data.csv"):
        self.rows_count = 0
        self.con = sqlite3.connect(db_name, check_same_thread=False)
        self.cur = self.con.cursor()
        self.create_table()
        self.load_data(source)
        self.rows_count = self.cur.execute(
            "SELECT COUNT(*) FROM clients;").fetchone()[0]
    
    def create_table(self):
        self.cur.execute("""DROP TABLE IF EXISTS clients;""")
        self.cur.execute("""
        CREATE TABLE clients (
            id INTEGER PRIMARY KEY,
            category TEXT NOT NULL,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            email TEXT NOT NULL,
            gender TEXT NOT NULL,
            birthdate NUMERIC NOT NULL
        );""")

    def load_data(self, filename):
        with open(filename, 'r') as f:
            reader = csv.reader(f)
            next(reader)
            self.cur.executemany(
                """INSERT INTO clients 
            (category, firstname, lastname, email, gender, birthdate)
            VALUES (?, ?, ?, ?, ?, ?);""", reader
            )
            self.con.commit()
            
    
    def fetch_rows(self, page=None, limit=None, filters=None):
        query = """ SELECT * FROM clients """
        params = []
        if filters:
            query += "WHERE " + " AND ".join([f['query'] for f in filters.values()])
            
            for key, f  in filters.items():
                if key == "age_range":
                    params.extend(f['value'])
                else:
                    params.append(f['value'])
                                
        if page and limit:
            query += " LIMIT ? OFFSET ?"
            params.extend([limit, (page - 1) * limit])
       
        query+=";"
        self.cur.execute(query, tuple(params))
        rows = self.cur.fetchall()
        return rows
    
    @staticmethod
    def get_filters(category: str = None, 
                gender: str = None, 
                birthdate: str = None, 
                age: int = None, 
                start_age: int = None,
                end_age: int = None):
        filters = {}
        if category:
            filters['category'] = {'value': category.lower(),
                                'query': 'category = ?'}
        if gender and gender.lower() in ['male', 'female']:
            filters['gender'] = {'value': gender.lower(),
                                'query': 'gender = ?'}
        if birthdate:
            filters['birthdate'] = {'value': birthdate,
                                'query': 'birthdate = ?'}
        if age:
            filters['age'] = {'value': age,
                            'query': "(strftime('%Y', date('now')) - strftime('%Y', birthdate)) = ?"}
        
        if start_age and end_age and not age:
            filters['age_range'] = {'value': (start_age, end_age),
                                    "query": "(strftime('%Y', date('now')) - strftime('%Y', birthdate)) BETWEEN ? AND ?"}
            
        return filters
    
    def close(self):
        self.con.commit()
        self.con.close()
     