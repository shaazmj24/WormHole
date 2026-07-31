--- this init.sql generates / intializes table (file) which gets stored inside task_db (database)

CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    done BOOLEAN NOT NULL DEFAULT FALSE
);


INSERT INTO tasks (title, done)
SELECT 'Learn Docker', FALSE
WHERE NOT EXISTS (
    SELECT 1 FROM tasks
);


