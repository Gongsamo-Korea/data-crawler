import mysql.connector

# Set up the MySQL connection parameters
config = {
  'user': 'gonsamo_dev',
  'password': '-dN_p]M*Q\i4',
  'host': 'gongsamo-dev-rds-2a.cx02ihqfn9bx.ap-northeast-2.rds.amazonaws.com',
  'database': 'gongsamo_dev',
  #'port' : 33064,
  'charset': 'utf8mb4', 
  'collation': 'utf8mb4_general_ci',
  'raise_on_warnings': True

}


class dbConnect: 
    def __init__(self):
        # Connect to the MySQL server
        try:
            self.mydb = mysql.connector.connect(**config)
            print("Connected to MySQL server!")
        except mysql.connector.Error as err:
            print(f"Error connecting to MySQL server: {err}")
            exit(1)

       
        self.c = self.mydb.cursor(buffered=True)
       # cur.execute("USE archewiki")

        # 커서 획득
        #self.c = connection.cursor()
        

    def insertArchiveData(self, title, issue_number, issue_date, table_of_content, content):    
        self.c.execute("INSERT INTO article (title, issue_number, issue_date, table_of_content, content) VALUES(%s, %s, %s, %s, %s)", (title, issue_number, issue_date, table_of_content, content))

        # Check if the insert query was executed successfully
        if self.c.rowcount > 0:
            print("Insert query executed successfully.")
        else:
            print("Insert query did not affect any rows.")

        self.mydb.commit()
        

            
    def update_table_of_content(self, table_of_content, article_id):
        self.c.execute("UPDATE article SET table_of_content = %s where article_id = %s", (table_of_content, article_id))
        # Check if the insert query was executed successfully
        if self.c.rowcount > 0:
            print("update query executed successfully.")
        else:
            print("update query did not affect any rows.")

        self.mydb.commit()
        
    def update_content(self, content, article_id):
        self.c.execute("UPDATE article SET content = %s where article_id = %s", (content, article_id))
        # Check if the insert query was executed successfully
        if self.c.rowcount > 0:
            print("update query executed successfully.")
        else:
            print("update query did not affect any rows.")

        self.mydb.commit()

    def update_issue_date(self, issue_date, article_id):
        self.c.execute("UPDATE article SET issue_date = %s where article_id = %s", (issue_date, article_id))

        if self.c.rowcount > 0:
            print("update query executed successfully.")
        else:
            print("update query did not affect any rows.")

        self.mydb.commit()

    def retreive_article_id(self, issue_number):
        self.c.execute("SELECT article_id FROM article WHERE issue_number = %s", (issue_number, ))
        result = self.c.fetchone()
        if not result: 
            return None
        return result[0]

    def insert_tags_to_tag_table(self, tags_list):
        result_list = []
        
        for tag in tags_list: 
            select_query = "SELECT tag_id FROM tag WHERE tag_name = %s"
            self.c.execute(select_query, (tag,))
            is_exist = self.c.fetchone()
            if is_exist is None:
                self.c.execute("INSERT INTO tag (tag_name) VALUES (%s)", (tag,)) 
                self.c.execute(select_query, (tag,))
                tag_id = self.c.fetchone()
                result_list.append(tag_id[0])
            else : 
                result_list.append(is_exist[0])
        
        self.mydb.commit()
    
        return result_list


    def insert_tags_id_to_tag_article_table(self, tag_id_list, article_id):
        for tag_id in tag_id_list:
            # 이미 태그가 지정되있는지 확인 
            self.c.execute("SELECT count(*) FROM article_tag WHERE article_id = %s AND tag_id =%s", (article_id, tag_id, ))
            #result = self.c.rowcount
            result = self.c.fetchone()
            if result[0] == 0 :
                self.c.execute("INSERT INTO article_tag (article_id, tag_id) VALUES (%s, %s)", (article_id, tag_id))
            
        self.mydb.commit()

    def closeDB(self):
        self.c.close()
        self.mydb.close()


