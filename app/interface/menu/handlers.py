from typing import Dict, List, Optional

from app.services.user_service import UserService
from app.services.group_service import GroupService
from app.services.expense_service import ExpenseService
from app.services.settlement_service import SettlementService
from app.domain.split_strategies.factory import SplitType


class MenuHandlers:
    """
    Thin interface layer.
    One handler method == one service call.
    """

    def __init__(
        self,
        user_service: UserService,
        group_service: GroupService,
        expense_service: ExpenseService,
        settlement_service: SettlementService,
    ):
        self.user_service = user_service
        self.group_service = group_service
        self.expense_service = expense_service
        self.settlement_service = settlement_service

    # -------------------- USER --------------------

    def create_user(self, name: str) -> None:
        try:
            self.user_service.create_user(name)
            print("✅ User created successfully")
        except Exception as e:
            print(f"❌ Failed to create user: {e}")

    def list_users(self) -> None:
        try:
            users = self.user_service.list_users()
            if not users:
                print("ℹ️ No users found")
                return

            for user in users:
                print(f"- {user.id} | {user.name}")
        except Exception as e:
            print(f"❌ Failed to list users: {e}")

    # -------------------- GROUP --------------------

    def create_group(self, name: str) -> None:
        try:
            self.group_service.create_group(name)
            print("✅ Group created successfully")
        except Exception as e:
            print(f"❌ Failed to create group: {e}")

    def add_user_to_group(self, group_id: int, user_id: int) -> None:
        try:
            self.group_service.add_user_to_group(group_id, user_id)
            print("✅ User added to group")
        except Exception as e:
            print(f"❌ Failed to add user to group: {e}")

    def list_groups(self) -> None:
        try:
            groups = self.group_service.list_groups()
            if not groups:
                print("ℹ️ No groups found")
                return

            for group in groups:
                print(f"- {group.id} | {group.name}")
        except Exception as e:
            print(f"❌ Failed to list groups: {e}")

    def view_group_members(self, group_id: int) -> None:
        try:
            members = self.group_service.get_group_members(group_id)
            if not members:
                print("ℹ️ No members in this group")
                return

            for user in members:
                print(f"- {user.id} | {user.name}")
        except Exception as e:
            print(f"❌ Failed to fetch group members: {e}")



    # -------------------- EXPENSE --------------------

    def add_expense(
        self,
        group_id: int,
        paid_by_id: int,
        participant_ids: List[int],
        amount: float,
        split_type: str,
        split_data: Optional[Dict] = None,
    ) -> None:
        try:
            exp = self.expense_service.add_expense(
                group_id=group_id,
                paid_by_id=paid_by_id,
                participant_ids=participant_ids,
                amount=amount,
                split_type=SplitType(split_type),
                split_data=split_data,
            )
            print(f"✅ Expense added successfully (id={exp.id}, amount={exp.amount})")
        except Exception as e:
            print(f"❌ Failed to add expense: {e}")

    def list_expenses(self, group_id: int) -> None:
        try:
            expenses = self.expense_service.list_expenses(group_id)
            if not expenses:
                print("ℹ️ No expenses found")
                return

            for exp in expenses:
                print(f"- {exp.id} | {exp.amount:.2f} | paid by {exp.paid_by.name} ({exp.paid_by.id})")
        except Exception as e:
            print(f"❌ Failed to list expenses: {e}")

    # -------------------- SETTLEMENT --------------------

    def view_balances(self, group_id: int) -> None:
        try:
            balances = self.settlement_service.get_balances(group_id)
            if not balances:
                print("ℹ️ No balances available")
                return

            for user, amount in balances.items():
                # balances in your CLI are {User: float}
                print(f"- {user.name} ({user.id}): {amount:.2f}")
        except Exception as e:
            print(f"❌ Failed to compute balances: {e}")

    def generate_settlement(self, group_id: int) -> None:
        try:
            suggestions = self.settlement_service.get_settlement_suggestions(group_id)
            if not suggestions:
                print("ℹ️ No settlements required")
                return

            for payer, receiver, amount in suggestions:
                print(f"- {payer.name} pays {receiver.name} amount {amount:.2f}")
        except Exception as e:
            print(f"❌ Failed to generate settlement: {e}")