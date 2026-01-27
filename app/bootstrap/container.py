from app.persistence.mysql.user_repo_mysql import UserRepositoryMySQL
from app.persistence.mysql.group_repo_mysql import GroupRepositoryMySQL
from app.persistence.mysql.expense_repo_mysql import ExpenseRepositoryMySQL

from app.services.user_service import UserService
from app.services.group_service import GroupService
from app.services.expense_service import ExpenseService
from app.services.settlement_service import SettlementService

from app.domain.domain_services.settlement_calculator import SettlementCalculator

from app.common.config import load_database_config
from app.persistence.mysql.db import MySQLDatabase



def build_services():
    db_config = load_database_config()
    db = MySQLDatabase(db_config)

    user_repo = UserRepositoryMySQL(db)
    group_repo = GroupRepositoryMySQL(db)
    expense_repo = ExpenseRepositoryMySQL(db)

    return {
        "user": UserService(user_repo),
        "group": GroupService(group_repo, user_repo),
        "expense": ExpenseService(expense_repo, group_repo, user_repo),
        "settlement": SettlementService(
            group_repo,
            SettlementCalculator()
        ),
        "group_repo": group_repo,
    }


