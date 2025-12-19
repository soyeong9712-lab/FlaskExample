import pymysql
from pymysql import Error

class Database:
    def __init__(self):
        self.connection = None
        self.connect()

    def connect(self):
        """데이터베이스 연결 및 재연결 로직"""
        try:
            self.connection = pymysql.connect(
                host='mariadb',
                port=3306,
                database='test',
                user='root',
                password='a123',
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor,
                autocommit=True  # 자동으로 커밋하도록 설정
            )
            print("MariaDB에 성공적으로 연결되었습니다.")
        except Error as e:
            print(f"MariaDB 연결 오류: {e}")

    def is_connected(self):
        """연결 상태 확인 및 복구"""
        try:
            self.connection.ping(reconnect=True)
            return True
        except:
            return False

    def save_bmi_record(self, weight, height, bmi, category):
        try:
            if not self.is_connected():
                self.connect()
                
            with self.connection.cursor() as cursor:
                query = "INSERT INTO bmi_records (weight, height, bmi, category) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (weight, height, bmi, category))
            # autocommit=True 설정으로 self.connection.commit() 생략 가능
            print("데이터 저장 성공!")
            return True
        except Error as e:
            print(f"저장 오류: {e}")
            return False

    def get_bmi_records(self, limit=10):
        try:
            if not self.is_connected():
                self.connect()
                
            with self.connection.cursor() as cursor:
                query = "SELECT * FROM bmi_records ORDER BY created_at DESC LIMIT %s"
                cursor.execute(query, (limit,))
                return cursor.fetchall()
        except Error as e:
            print(f"조회 오류: {e}")
            return []