import pymysql
import datetime

now = datetime.datetime.now()

class DatabaseMaria:
    _instance = None  #

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
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
    
    def send_operating_conditions(self, dry_number):
        try:
            with self.connect_db() as conn:
                with conn.cursor() as cur:
                    sql = '''
                    SELECT 
                        *
                    FROM
                        recipe_table rt 
                    WHERE 
                        dry_number = %s;
                    '''
                    cur.execute(sql,(dry_number))
                    result = cur.fetchall()
                    return result
        except Exception as e:
            print("예외 : ", str(e))
        return

    def delete_dryer_num(self, dryer_ip):
        try:
            with self.connect_db() as conn:
                with conn.cursor() as cur:
                    sql = '''
                    UPDATE 
                        dryer_number 
                    SET
                        dryer_status = 0
                    WHERE
                        dryer_ipaddress = %s;
                    '''
                    cur.execute(sql,(dryer_ip))
                    conn.commit()
        except Exception as e:
            print("예외 : ", str(e))
        return

    def setting_dryer_num(self, dryer_ip):
        print(dryer_ip,"----dryer_ip")
        try:
            with self.connect_db() as conn:
                with conn.cursor() as cur:
                    sql = '''
                    UPDATE 
                        dryer_number 
                    SET
                        dryer_status = 1
                    WHERE
                        dryer_ipaddress = %s;
                    '''
                    cur.execute(sql,(dryer_ip))
                    conn.commit()
        except Exception as e:
            print("예외 : ", str(e))
        return

    def get_dryer_connection_list(self):
        try:
            with self.connect_db() as conn:
                with conn.cursor() as cur:
                    sql = '''
                    SELECT 
                        dryer_number ,
                        dryer_ipaddress ,
                        last_access_date ,
                        dryer_status 
                    FROM 
                        dryer_number
                    WHERE 
                        dryer_status = 1;
                    '''
                    cur.execute(sql,)
                    result = cur.fetchall()
                    return result
        except Exception as e:
            print("예외 : ", str(e))
        return

    def add_stage_list(self,dryNumber, addTemp, addHum, addTime):
        try:
            with self.connect_db() as conn:
                with conn.cursor() as cur:
                    sql = '''
                    INSERT INTO 
                    cesdatabase.recipe_table 
                    (dry_number, 
                    stage_number, 
                    uptime, 
                    set_temperature, 
                    set_humidity, 
                    numbering, 
                    registration_date, 
                    modification_date)
                    VALUES
                    (%s,
                    1,
                    %s,
                    %s,
                    %s,
                    1,
                    CURDATE(),
                    CURDATE());
                    '''
                    cur.execute(sql, (dryNumber,addTime, addTemp, addHum))
                    conn.commit()
        except Exception as e:
            print("예외 : ", str(e))
        return

    def delete_stageNum(self, stageNum):
        try:
            with self.connect_db() as conn:
                with conn.cursor() as cur:
                    sql = '''
                    DELETE  
                    FROM 
                        recipe_table 
                    WHERE 
                        recipe_number  = %s ;
                    '''
                    cur.execute(sql, (stageNum,))
                    conn.commit()
        except Exception as e:
            print("예외 : ", str(e))
        return

    def modify_stage(self, stageNum, temp, hum, time):
        try:
            with self.connect_db() as conn:
                with conn.cursor() as cur:
                    sql = '''
                    UPDATE 
                        recipe_table  
                    SET
                        set_temperature = %s,
                        set_humidity = %s, 
                        uptime = %s,
                        modification_date = CURDATE()
                    WHERE 
                        recipe_number = %s;
                    '''
                    cur.execute(sql, (temp, hum, time, stageNum,))
                    conn.commit()
        except Exception as e:
            print("예외 : ", str(e))
        return

    def get_detail_recipe_list(self, selectNum:int):
        try:
            with self.connect_db() as conn:
                with conn.cursor() as cur:
                    sql = '''
                    SELECT 
                        rt.recipe_number , 
                        rt.dry_number ,
                        rt.numbering,
                        dt.dried_product_name,
                        rt.set_temperature ,
                        rt.set_humidity ,
                        rt.uptime 
                    FROM 
                        recipe_table rt 
                        INNER JOIN drying_table dt 
                        on rt.dry_number = dt.dry_number 
                    WHERE rt.dry_number = %s;
                    '''
                    cur.execute(sql, (selectNum,))
                    detailRecipeStage_list = cur.fetchall()
                    detailRecipeList = list(detailRecipeStage_list)
                    return detailRecipeList
        except Exception as e:
            print("예외 : ", str(e))

    def add_dry_name(self, add_name, dryer_number):
        try:
            with self.connect_db() as conn:
                with conn.cursor() as cur:
                    sql = '''
                        INSERT INTO 
                        cesdatabase.drying_table(dried_product_name, 
                                            registration_date, 
                                            modification_date,
                                            dryer_number)
                        VALUES(%s, 
                            curdate(), 
                            curdate(),
                            %s);
                    '''
                    cur.execute(sql, (add_name,dryer_number))
                    conn.commit()
        except Exception as e:
            print("예외 : ", str(e))


    def delete_dry_name(self, delete_num):
        try:
            with self.connect_db() as conn:
                with conn.cursor() as cur:
                    sql1 = '''
                        DELETE  
                        FROM 
                            recipe_table
                        WHERE 
                            dry_number = %s;
                    '''
                    cur.execute(sql1, (delete_num,))
                    sql = '''
                        DELETE  
                        FROM 
                            drying_table
                        WHERE 
                            dry_number = %s;
                    '''
                    cur.execute(sql, (delete_num,))
                    conn.commit()
        except Exception as e:
            print("예외 : ", str(e))

    def modify_dry_name(self, select_num, input_modify):
        try:
            with self.connect_db() as conn:
                with conn.cursor() as cur:
                    sql = '''
                        UPDATE 
                            drying_table 
                        SET
                            dried_product_name = %s,
                            modification_date = CURTIME()
                        WHERE 
                            dry_number = %s
                    '''
                    cur.execute(sql, (input_modify, select_num))
                    conn.commit()
        except Exception as e:
            print("예외 : ", str(e))

    def get_dry_menulist(self, dryer_number):
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
                    WHERE
                        dryer_number = %s;
                    '''
                    cur.execute(sql,(dryer_number))
                    result = cur.fetchall()
                    print(result,"result")
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
                            SEC_TO_TIME(SUM(uptime)) AS total_uptime
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
    