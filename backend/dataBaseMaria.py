import pymysql
import datetime

now = datetime.datetime.now()

class DatabaseMaria:
    def __init__(self, host, port, user, password, db, charset):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.charset = charset

    def connect_db(self):
        conn = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            db=self.db,
            charset=self.charset
        )
        return conn
    
    def get_dry_menulist(self):
        try:
            with self.connect_db() as conn:
                with conn.cursor() as cur:
                    sql = '''
                    SELECT 
                        dry_number,
                        dried_product_name,
                        modification_date
                    FROM 
                        drying_table
                    '''
                    cur.execute(sql,)
                    result = cur.fetchall()
                    return result
        except Exception as e:
            print("예외  : ", str(e));
    
    def get_detail_recipe(self, recipe_num):
        try:
            with self.connect_db() as conn:
                with conn.cursor() as cur:
                    sql = '''
                        SELECT 
                            dt.dried_product_name ,
                            rt.dry_number, SUM(numbering) AS total_stage_number,
                            SEC_TO_TIME(SUM(TIME_TO_SEC(uptime))) AS total_uptime
                        FROM recipe_table rt 
                        JOIN drying_table dt 
                        ON dt.dry_number = rt.dry_number  
                        WHERE dt.dry_number = %s
                        GROUP BY dt.dry_number;
                        '''
                    cur.execute(sql, recipe_num)
                    result = cur.fetchall()
                    return result
        except Exception as e:
            print("예외  : ", str(e));
    