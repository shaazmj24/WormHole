from app.repository.interface import TaskRepository , Task , UpdateTask , NewTask  
from app.database import get_connection

class PostgresTaskRepository(TaskRepository):

    def list_tasks(self, user_id: str) -> list[Task]:
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, title, done
                    FROM tasks 
                    WHERE user_id = %s 
                    ORDER BY id
                    """, 
                    (user_id,), 
                )

                rows = cursor.fetchall()

                return [
                    Task(
                        id=row[0],
                        title=row[1],
                        done=row[2],
                    )
                    for row in rows
                ]

        finally:
            conn.close()

    def get_task(self, id: int, user_id: str) -> Task:
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, title, done
                    FROM tasks
                    WHERE id = %s AND user_id = %s
                    """,
                    (id, user_id),
                )

                row = cursor.fetchone()

                if row is None:
                    raise LookupError("ID not found")

                return Task(
                    id=row[0],
                    title=row[1],
                    done=row[2],
                )

        finally:
            conn.close()

    def add_task(self, new_task: NewTask , user_id: str) -> Task:
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tasks (user_id, title, done)
                    VALUES (%s, %s, %s)
                    RETURNING id, title, done
                    """,
                    (
                        user_id,
                        new_task.title,
                        new_task.done,
                    ),
                )

                row = cursor.fetchone()
                conn.commit()

                return Task(
                    id=row[0],
                    title=row[1],
                    done=row[2],
                )

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close() 
            

    def replace_task(self, id: int, update: UpdateTask, user_id: str) -> Task:
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tasks
                    SET title = %s, done = %s
                    WHERE id = %s AND user_id = %s
                    RETURNING id, title, done
                    """,
                    (
                        update.title,
                        update.done,
                        id, 
                        user_id,
                    ),
                )

                row = cursor.fetchone()

                if row is None:
                    raise LookupError("ID not found")

                conn.commit()

                return Task(
                    id=row[0],
                    title=row[1],
                    done=row[2],
                )

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close() 
            

    def delete_task(self, id: int , user_id: str) -> None:
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM tasks
                    WHERE id = %s AND user_id = %s
                    RETURNING id
                    """,
                    (id, user_id),
                )

                row = cursor.fetchone()

                if row is None:
                    raise LookupError("ID not found")

                conn.commit()

        except Exception:
            conn.rollback()
            raise

        finally:
            conn.close()
            
            


