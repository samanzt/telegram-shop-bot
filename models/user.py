from database.connection import get_connection


class User:

    def __init__(self, telegram_id, name, phone=None):
        self.telegram_id = telegram_id
        self.name = name
        self.phone = phone


    def save(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO users
            (telegram_id, name, phone)
            VALUES (?, ?, ?)
            """,
            (
                self.telegram_id,
                self.name,
                self.phone
            )
        )

        conn.commit()
        conn.close()


    @staticmethod
    def get_by_telegram_id(telegram_id):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE telegram_id = ?
            """,
            (telegram_id,)
        )

        user = cursor.fetchone()

        conn.close()

        return user

    @staticmethod
    def get_by_id(user_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM users
            WHERE telegram_id = ?
            """,
            (user_id,)
        )

        user = cursor.fetchone()

        conn.close()

        return user