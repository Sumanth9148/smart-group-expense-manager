CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

CREATE TABLE expense_groups (
    id CHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);


CREATE TABLE IF NOT EXISTS group_members (
    group_id CHAR(36),
    user_id CHAR(36),
    PRIMARY KEY (group_id, user_id),
    FOREIGN KEY (group_id) REFERENCES expense_groups(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS expenses (
    id CHAR(36) PRIMARY KEY,
    group_id CHAR(36) NOT NULL,
    paid_by CHAR(36) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    split_type VARCHAR(20) NOT NULL,
    FOREIGN KEY (group_id) REFERENCES expense_groups(id),
    FOREIGN KEY (paid_by) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS expense_splits (
    expense_id CHAR(36),
    user_id CHAR(36),
    amount DECIMAL(10,2),
    percentage DECIMAL(5,2),
    PRIMARY KEY (expense_id, user_id),
    FOREIGN KEY (expense_id) REFERENCES expenses(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
