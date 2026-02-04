-- Re-runnable init (drops in dependency order)
DROP TABLE IF EXISTS expense_splits;
DROP TABLE IF EXISTS expenses;
DROP TABLE IF EXISTS group_members;
DROP TABLE IF EXISTS expense_groups;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE KEY uniq_user_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE expense_groups (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  name VARCHAR(100) NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE group_members (
  group_id INT UNSIGNED NOT NULL,
  user_id INT UNSIGNED NOT NULL,
  PRIMARY KEY (group_id, user_id),
  CONSTRAINT fk_group_members_group
    FOREIGN KEY (group_id) REFERENCES expense_groups(id) ON DELETE CASCADE,
  CONSTRAINT fk_group_members_user
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Expenses include description + date (required by spec)
-- ...existing code...

CREATE TABLE expenses (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  group_id INT UNSIGNED NOT NULL,
  paid_by INT UNSIGNED NOT NULL,
  amount DECIMAL(10,2) NOT NULL,

  -- ✅ required by your code today
  split_type VARCHAR(80) NOT NULL,

  -- ✅ required by spec, but keep defaults so current code doesn't break
  description VARCHAR(255) NOT NULL DEFAULT '',
  expense_date DATE NOT NULL DEFAULT (CURRENT_DATE),

  PRIMARY KEY (id),
  CONSTRAINT fk_expenses_group
    FOREIGN KEY (group_id) REFERENCES expense_groups(id) ON DELETE CASCADE,
  CONSTRAINT fk_expenses_paid_by
    FOREIGN KEY (paid_by) REFERENCES users(id) ON DELETE RESTRICT,
  INDEX idx_expenses_group_date (group_id, expense_date),
  INDEX idx_expenses_paid_by (paid_by)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ...existing code...

-- Split rows: who owes how much for a given expense
CREATE TABLE expense_splits (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT,
  expense_id INT UNSIGNED NOT NULL,
  user_id INT UNSIGNED NOT NULL,
  amount DECIMAL(10,2) NOT NULL,
  PRIMARY KEY (id),
  CONSTRAINT fk_splits_expense
    FOREIGN KEY (expense_id) REFERENCES expenses(id) ON DELETE CASCADE,
  CONSTRAINT fk_splits_user
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  UNIQUE KEY uniq_expense_user (expense_id, user_id),
  INDEX idx_splits_user (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
