from app.repository.interface import TaskRepository , Task , UpdateTask , NewTask  
from app.database import get_connection

class PostgresTaskRepository(TaskRepository):

    def list_tasks(self) -> list[Task]:
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, title, done
                    FROM tasks
                    ORDER BY id
                    """
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

    def get_task(self, id: int) -> Task:
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT id, title, done
                    FROM tasks
                    WHERE id = %s
                    """,
                    (id,),
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

    def add_task(self, new_task: NewTask) -> Task:
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO tasks (title, done)
                    VALUES (%s, %s)
                    RETURNING id, title, done
                    """,
                    (
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

    def replace_task(self, id: int, update: UpdateTask) -> Task:
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE tasks
                    SET title = %s, done = %s
                    WHERE id = %s
                    RETURNING id, title, done
                    """,
                    (
                        update.title,
                        update.done,
                        id,
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

    def delete_task(self, id: int) -> None:
        conn = get_connection()

        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    DELETE FROM tasks
                    WHERE id = %s
                    RETURNING id
                    """,
                    (id,),
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
            
            


