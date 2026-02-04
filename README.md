Smart Group Expense Manager
===========================

A overview of a Python CLI that manages shared expenses. The entire stack runs inside Podman containers on **WSL (Ubuntu) for Windows**.

Project Overview
----------------
# What the project does
- Provides a menu driven CLI to create users/groups, log expenses, compute balances, and generate settlement suggestions.

# Why it is useful
- Replaces error prone spreadsheets for roommates, trips, and small teams.
- Keeps balances transparent, everyone can see what they owe or are owed.

# Key CLI menu features
- Clear separation of User, Group, Expense, and Settlement flows.
- Equal, percentage, and custom split strategies.
- logging to `logs/app.log`.
- Balance view (positive = owed, negative = owes) and settlement suggestions (“A pays B”).


Tech Stack
----------
- **Python 3.11** – CLI and domain logic.
- **Podman** – container runtime inside WSL.
- **podman-compose** – orchestrates app + MySQL services.
- **MySQL 8** – persistent store for all data.
- **WSL (Ubuntu)** – Linux layer running on Windows hardware.



Project Architecture
--------------------
```
smart_group_expense_manager/
├─ app/
│  ├─ bootstrap/
│  │  └─ container.py          # Wires repositories + services (dependency injection)
│  ├─ common/
│  │  ├─ logger.py             # Logging setup (console + file)
│  │  ├─ background_tasks.py   # Async periodic balance logger
│  │  └─ config.py             # DB config / env loading
│  ├─ domain/
│  │  ├─ entities/             # User, Group, Expense models
│  │  ├─ repositories/         # Repository interfaces (abstractions)
│  │  ├─ split_strategies/     # equal/custom/percentage + factory
│  │  └─ domain_services/      # Settlement calculator
│  ├─ persistence/
│  │  └─ mysql/                # MySQL implementations of repositories
│  ├─ services/
│  │  ├─ user_service.py       # User use‑cases
│  │  ├─ group_service.py      # Group & membership use‑cases
│  │  ├─ expense_service.py    # Expense creation + list
│  │  └─ settlement_service.py # Balances + settlement suggestions
│  └─ interface/
│     ├─ cli.py                # CLI entry point + main menu loop
│     └─ menu/handlers.py      # Thin handlers that call services
├─ docker/
│  ├─ Dockerfile               # Python image with deps
│  ├─ docker-compose.yml       # app + mysql services
│  └─ db/init.sql              # DB schema bootstrap
├─ tests/
│  ├─ split_strategies/        # Strategy unit tests
│  ├─ domain_services/         # Settlement calculator tests
│  └─ services/                # Service layer tests
└─ README.md
```


- **Entry point**: `app/interface/cli.py` builds services via `app/bootstrap/container.py` then runs `MenuDrivenInterface`.
- **CLI flow**: main loop → submenus → handler methods → service layer → repositories → MySQL.

Prerequisites
-------------
- Windows 10/11 with **WSL (Ubuntu)** enabled.
- Inside WSL: `sudo apt install podman podman-compose` 
- Python 3.11 if you plan to run tests outside containers.


Run Project (WSL)
-------------------------------
1. **Enter WSL and locate the project**
  ```bash
  wsl
  cd /mnt/c/Users/Sumanthrn/smart_group_expense_manager
  ```
2. **Reset previous containers/volumes**
  ```bash
  cd docker
  podman-compose down -v
  ```
3. **Build the CLI image**
  ```bash
  podman-compose build app
  ```
  
4. **Start MySQL (runs db/init.sql on fresh volume)**
  ```bash
  podman-compose up -d mysql
  ```
5. **Verify schema**
  ```bash
  podman exec -it expense_mysql mysql -uappuser -papppass expense_manager
  ```
  
6. **Run the interactive CLI**
  ```bash
  podman-compose run --rm app
  ```
  Choose menu option `5` to exit; `--rm` cleans up the one-off CLI container.

How the CLI Menu Works
----------------------
Top-level menu (rendered each loop):
```
==================================================
Smart Group Expense Manager
==================================================
1. User Management
2. Group Management
3. Expense Management
4. Settlement & Balances
5. Exit
==================================================
```
1. **User Management** – Create users, list them, return to main.
2. **Group Management** – Create groups, add/remove members, list groups with members.
3. **Expense Management** – Add expenses (equal/percentage/custom), list expenses per group.
4. **Settlement and Balances** – View net balance per user and settlement suggestions.

Example input/output flow:
```
Main -> 1 -> 1 -> "Alice"   # prints  User created with ID: 1
Main -> 1 -> 1 -> "Bob"     # ID: 2
Main -> 2 -> 1 -> "Trip"    # Group ID printed
Main -> 2 -> 2 -> (Group 1, User 1)   # " Member added"
Main -> 3 -> 1 -> equal split expense # shows participants + shares
Main -> 4 -> 1 -> balances (Alice: -30, Bob: 80, Charlie: -50)
Main -> 4 -> 2 -> settlement suggestions ("Alice ➜ Bob: 30", etc.)

```

Database Details
----------------
- `docker/db/init.sql` drops tables in dependency order and recreates: `users`, `expense_groups`, `group_members`, `expenses`, `expense_splits`.
- Podman volume `mysql_data` holds persistent MySQL files.
- Inspect data:
  ```bash
  podman exec -it expense_mysql mysql -uappuser -papppass expense_manager
  ```
  Run queries like `SHOW TABLES;` or `SELECT * FROM expense_splits;`.


Design Principles
-----------------
### SOLID 
- **S — Single Responsibility Principle (SRP)**  
  - Each service focuses on one use case:  
    `app/services/user_service.py`, `group_service.py`, `expense_service.py`, `settlement_service.py`  
  - Each repository handles only DB concerns for its aggregate:  
    `app/persistence/mysql/user_repo_mysql.py`, `group_repo_mysql.py`, `expense_repo_mysql.py`  
  - CLI files only handle input/output:  
    `app/interface/cli.py`, `app/interface/menu/handlers.py`

- **O — Open/Closed Principle (OCP)**  
  - New split logic can be added without modifying the core flow:  
    `app/domain/split_strategies/base.py` + `factory.py`  
  - New strategies (e.g., weighted) only require a new class under  
    `app/domain/split_strategies/` and a factory mapping.

- **L — Liskov Substitution Principle (LSP)**  
  - All split strategies implement the same interface, so any strategy can replace another:  
    `SplitStrategy` (base) → `EqualSplitStrategy`, `CustomSplitStrategy`, `PercentageSplitStrategy`.

- **I — Interface Segregation Principle (ISP)**  
  - Repository interfaces are small and focused:  
    `app/domain/repositories/user_repository.py`, `group_repository.py`, `expense_repository.py`.

- **D — Dependency Inversion Principle (DIP)**  
  - Services depend on abstract repositories, not concrete MySQL classes.  
    Implementations are injected via `app/bootstrap/container.py`.

### Design Patterns 
- **Strategy Pattern**  
  - For expense splits:  
    `app/domain/split_strategies/` (equal/custom/percentage)  
  - Used by `ExpenseService` when applying a split.

- **Factory Pattern**  
  - `SplitStrategyFactory` selects the right strategy based on user input:  
    `app/domain/split_strategies/factory.py`

- **Repository Pattern**  
  - Encapsulates DB queries and hides MySQL details:  
    `app/persistence/mysql/*_repo_mysql.py`

- **Dependency Injection**  
  - Services and repositories are wired in one place:  
    `app/bootstrap/container.py`  
  - Keeps `cli.py` independent of database implementations.


Common Commands
---------------
- Cleanup stack + volume: `podman-compose down -v`
- Start MySQL only: `podman-compose up -d mysql`
- Run CLI: `podman-compose run --rm app`
- List containers/images: `podman ps -a`, `podman images`
- Inspect volumes: `podman volume ls`


Future Enhancements
-------------------
- **Travel (multi‑currency)**: Useful for international trips where people pay in different currencies. The app can convert and settle in one currency.




