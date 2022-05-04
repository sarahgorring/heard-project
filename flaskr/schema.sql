DROP TABLE IF EXISTS expense_tracker;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS budget;
DROP TABLE IF EXISTS expense;

CREATE TABLE expense_tracker (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  family_tracker_name TEXT NOT NULL
);

CREATE TABLE user (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  tracker_id INTEGER NOt NULL,
  name TEXT NOT NULL,
  parent BOOLEAN NOT NULL,
  FOREIGN KEY (tracker_id) REFERENCES expense_tracker (id)
);

CREATE TABLE budget (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  user_id INTEGER NOT NULL,
  owner_id INTEGER,
  start_date TIMESTAMP NOT NULL,
  end_date TIMESTAMP NOT NULL,
  category TEXT,
  total INTEGER NOT NULL,
  amount_spent NOT NULL DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (owner_id) REFERENCES user (id)
);

CREATE TABLE expense (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  budget_id INTEGER,
  category TEXT,
  amount INTEGER NOT NULL,
  expense_date  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  approval_status BOOLEAN,
  FOREIGN KEY (user_id) REFERENCES user (id),
  FOREIGN KEY (budget_id) REFERENCES budget (id)

);
