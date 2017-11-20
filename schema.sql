DROP TABLE IF EXISTS student;
DROP TABLE IF EXISTS quiz;
DROP TABLE IF EXISTS result;

CREATE TABLE student (
  id INTEGER PRIMARY KEY,
  f_name TEXT,
  l_name TEXT
);

CREATE TABLE quiz (
  id INTEGER PRIMARY KEY,
  subject TEXT,
  num_qs INTEGER,
  quizdate TEXT
);

CREATE TABLE result (
  id INTEGER PRIMARY KEY,
  student_id INTEGER,
  quiz_id INTEGER,
  score INTEGER,
  FOREIGN KEY (student_id) REFERENCES student(id),
  FOREIGN KEY (quiz_id) REFERENCES quiz(id)
);