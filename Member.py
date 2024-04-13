import mysql.connector

class DatabaseConnection:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Sharon1597536987410',
            database="WellRead"
        )
        self.cursor = self.conn.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

class Member:
    def __init__(self, name, email, phone, membership_type, membership_start_date, id=None):
        self.id = id
        self.name = name
        self.email = email
        self.phone = phone
        self.membership_type = membership_type
        self.membership_start_date = membership_start_date

class DatabaseManager:
    @staticmethod
    def add_member(member):
        if isinstance(member, Member):
            with DatabaseConnection() as db:
                db.cursor.execute("INSERT INTO Members (Name, Email, Phone, MembershipType, MembershipStartDate) VALUES (%s, %s, %s, %s, %s)",
                                  (member.name, member.email, member.phone, member.membership_type, member.membership_start_date))

    @staticmethod
    def get_members():
        with DatabaseConnection() as db:
            db.cursor.execute("SELECT * FROM Members")
            members = db.cursor.fetchall()
            return [Member(id=id, name=name, email=email, phone=phone, membership_type=membership_type, membership_start_date=membership_start_date)
                    for id, name, email, phone, membership_type, membership_start_date in members]

    @staticmethod
    def update_member(member):
        if isinstance(member, Member):
            with DatabaseConnection() as db:
                db.cursor.execute(
                    "UPDATE Members SET Name = %s, Email = %s, Phone = %s, MembershipType = %s, MembershipStartDate = %s WHERE MembersId = %s",
                    (member.name, member.email, member.phone, member.membership_type, member.membership_start_date,
                     member.id))
                db.commit()  # Commit changes to the database

    @staticmethod
    def delete_member(member_id):
        with DatabaseConnection() as db:
            db.cursor.execute("DELETE FROM Members WHERE MembersId = %s", (member_id,))

    @staticmethod
    def search_members(query):
        with DatabaseConnection() as db:
            db.cursor.execute(
                "SELECT * FROM Members WHERE Name LIKE %s OR Email LIKE %s OR Phone LIKE %s OR MembershipType LIKE %s OR MembershipStartDate LIKE %s",
                ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
            members = db.cursor.fetchall()
            return [Member(id=id, name=name, email=email, phone=phone, membership_type=membership_type, membership_start_date=membership_start_date)
                    for id, name, email, phone, membership_type, membership_start_date in members]
