import asyncio
import logging

from app.common.logger import setup_logging
from app.bootstrap.container import build_services
from app.common.background_tasks import periodic_balance_logger
from app.domain.split_strategies.factory import SplitType


class MenuDrivenInterface:
    def __init__(self, services):
        self.services = services
        self.running = True

    def display_main_menu(self):
        print("\n" + "="*50)
        print("Smart Group Expense Manager")
        print("="*50)
        print("1. User Management")
        print("2. Group Management")
        print("3. Expense Management")
        print("4. Settlement & Balances")
        print("5. Exit")
        print("="*50)

    def display_user_menu(self):
        print("\n--- User Management ---")
        print("1. Create User")
        print("2. List All Users")
        print("3. Back to Main Menu")

    def display_group_menu(self):
        print("\n--- Group Management ---")
        print("1. Create Group")
        print("2. Add Member to Group")
        print("3. Remove Member from Group")
        print("4. List Groups")
        print("5. Back to Main Menu")

    def display_expense_menu(self):
        print("\n--- Expense Management ---")
        print("1. Add Expense")
        print("2. List Group Expenses")
        print("3. Back to Main Menu")

    def display_settlement_menu(self):
        print("\n--- Settlement & Balances ---")
        print("1. View Group Balances")
        print("2. Settlement Suggestions")
        print("3. Back to Main Menu")

    # User Management
    def create_user(self):
        name = input("Enter user name: ").strip()
        if not name:
            print("❌ User name cannot be empty!")
            return

        email = input("Enter user email: ").strip()
        if not email:
            print("❌ Email cannot be empty!")
            return

        try:
            user = self.services["user"].create_user(name, email)
            print("✅ User created successfully!")
            print(f"   ID: {user.id}")
            print(f"   Name: {user.name}")
            print(f"   Email: {user.email}")
        except ValueError as e:
            print(f"❌ {e}")
        except Exception as e:
            print(f"❌ Error creating user: {e}")


    def list_users(self):
        try:
            users = self.services["user"].list_users()
            if not users:
                print("\nℹ️ No users found.")
                return

            print("\n--- All Users ---")
            for user in users:
                print(f"{user.id}. {user.name} ({user.email})")
        except Exception as e:
            print(f"❌ Error retrieving users: {e}")

    def user_menu(self):
        while True:
            self.display_user_menu()
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.create_user()
            elif choice == "2":
                self.list_users()
            elif choice == "3":
                break
            else:
                print("❌ Invalid choice. Please try again.")

    # Group Management
    def create_group(self):
        name = input("Enter group name: ").strip()
        if not name:
            print("❌ Group name cannot be empty!")
            return

        try:
            group = self.services["group"].create_group(name)
            print("✅ Group created successfully!")
            print(f"   ID: {group.id}")
            print(f"   Name: {group.name}")
        except Exception as e:
            print(f"❌ Error creating group: {e}")

    def add_member_to_group(self):
        try:
            groups = self.services["group"].list_groups()
            if not groups:
                print("\n❌ No groups available. Create a group first.")
                return

            users = self.services["user"].list_users()
            if not users:
                print("\n❌ No users available. Create users first.")
                return

            print("\n--- Available Groups ---")
            for group in groups:
                print(f"{group.id}. {group.name}")

            print("\n--- Available Users ---")
            for user in users:
                print(f"{user.id}. {user.name} ({user.email})")

            group_id = input("\nEnter group ID: ").strip()
            user_id = input("Enter user ID: ").strip()

            if not group_id or not user_id:
                print("❌ Group ID and User ID cannot be empty!")
                return

            self.services["group"].add_member(int(group_id), int(user_id))
            print("✅ Member added to group successfully!")
        except ValueError:
            print("❌ Invalid number format!")
        except Exception as e:
            print(f"❌ Error adding member: {e}")

    def remove_member_from_group(self):
        try:
            groups = self.services["group"].list_groups()
            if not groups:
                print("\n❌ No groups available.")
                return

            print("\n--- Available Groups ---")
            for group in groups:
                print(f"{group.id}. {group.name}")

            group_id = input("\nEnter group ID: ").strip()
            if not group_id:
                print("❌ Group ID cannot be empty!")
                return

            group_details = self.services["group"].get_group_details(int(group_id))
            if not group_details:
                print("❌ Group not found!")
                return

            if not group_details.members:
                print("\n❌ No members in this group.")
                return

            print(f"\n--- Members of {group_details.name} ---")
            for member in group_details.members:
                print(f"{member.id}. {member.name} ({member.email})")

            user_id = input("\nEnter user ID to remove: ").strip()
            if not user_id:
                print("❌ User ID cannot be empty!")
                return

            self.services["group"].remove_member(int(group_id), int(user_id))
            print("✅ Member removed from group successfully!")
        except ValueError:
            print("❌ Invalid number format!")
        except Exception as e:
            print(f"❌ Error removing member: {e}")

    def list_groups(self):
        try:
            groups = self.services["group"].list_groups()
        except Exception as e:
            print(f"❌ Error fetching groups: {e}")
            return

        if not groups:
            print("No groups have been created yet.")
            return

        print("\n--- Groups ---")
        for group in groups:
            print(f"{group.name} ({group.id})")
            try:
                details = self.services["group"].get_group_details(group.id)
                members = details.members
                if members:
                    for member in members:
                        print(f"   - {member.name} ({member.id})")
                else:
                    print("   (No members)")
            except Exception as e:
                print(f"   ⚠️ Unable to load members: {e}")

    def group_menu(self):
        while True:
            self.display_group_menu()
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.create_group()
            elif choice == "2":
                self.add_member_to_group()
            elif choice == "3":
                self.remove_member_from_group()
            elif choice == "4":
                self.list_groups()
            elif choice == "5":
                break
            else:
                print("❌ Invalid choice. Please try again.")

    # Expense Management
    def add_expense(self):
        try:
            groups = self.services["group"].list_groups()
            if not groups:
                print("\n❌ No groups available. Create a group first.")
                return

            users = self.services["user"].list_users()
            if not users:
                print("\n❌ No users available. Create users first.")
                return

            print("\n--- Available Groups ---")
            for group in groups:
                print(f"{group.id}. {group.name}")

            print("\n--- Available Users ---")
            for user in users:
                print(f"{user.id}. {user.name} ({user.email})")

            group_id = input("\nEnter group ID: ").strip()
            paid_by_id = input("Enter payer user ID: ").strip()
            amount = input("Enter expense amount: ").strip()
            participants_str = input("Enter participant IDs (comma-separated): ").strip()
            split_type = input("Enter split type (equal/percentage/custom): ").strip().lower()

            if not all([group_id, paid_by_id, amount, participants_str, split_type]):
                print("❌ All fields are required!")
                return

            participants = [int(uid.strip()) for uid in participants_str.split(",") if uid.strip()]

            split_data = None
            if split_type == "percentage":
                split_data = {}
                data_str = input("Enter split data (user_id:percentage, comma-separated): ").strip()
                for item in [x.strip() for x in data_str.split(",") if x.strip()]:
                    uid_str, pct_str = [p.strip() for p in item.split(":", 1)]
                    split_data[int(uid_str)] = float(pct_str)

            elif split_type == "custom":
                split_data = {}
                data_str = input("Enter split data (user_id:amount, comma-separated): ").strip()
                for item in [x.strip() for x in data_str.split(",") if x.strip()]:
                    uid_str, amt_str = [p.strip() for p in item.split(":", 1)]
                    split_data[int(uid_str)] = float(amt_str)

            expense = self.services["expense"].add_expense(
                group_id=int(group_id),
                paid_by_id=int(paid_by_id),
                participant_ids=participants,
                amount=float(amount),
                split_type=SplitType(split_type),
                split_data=split_data
            )

            print("\n✅ Expense added successfully!")
            print(f"   ID: {expense.id}")
            try:
                group = self.services["group"].get_group_details(int(group_id))
                print(f"   Group: {group.name} ({group.id})")
            except Exception:
                print(f"   Group ID: {group_id}")

            print(f"   Paid By: {expense.paid_by.name} ({expense.paid_by.id})")
            print(f"   Amount: {expense.amount:.2f}")
            print(f"   Split Type: {split_type}")

            if expense.participants:
                participants_label = ", ".join(
                    f"{u.name} ({u.id})" for u in expense.participants
                )
                print(f"   Participants: {participants_label}")

            print("   Shares:")
            for user, value in expense.split().items():
                print(f"      - {user.name} ({user.id}): {value:.2f}")
        except ValueError as e:
            print(f"❌ Invalid input format: {e}")
        except Exception as e:
            print(f"❌ Error adding expense: {e}")

    def expense_menu(self):
        while True:
            self.display_expense_menu()
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.add_expense()
            elif choice == "2":
                self.list_expenses()
            elif choice == "3":
                break
            else:
                print("❌ Invalid choice. Please try again.")

    def list_expenses(self):
        try:
            groups = self.services["group"].list_groups()
            if not groups:
                print("\n❌ No groups available.")
                return

            print("\n--- Available Groups ---")
            for group in groups:
                print(f"{group.id}. {group.name}")

            group_id = input("\nEnter group ID: ").strip()

            if not group_id:
                print("❌ Group ID cannot be empty!")
                return

            expenses = self.services["expense"].list_expenses(int(group_id))

            if not expenses:
                print("No expenses recorded for this group.")
                return

            group_details = self.services["group"].get_group_details(int(group_id))
            print(f"\n--- Expenses for {group_details.name} ---")
            for expense in expenses:
                print(f"\nID: {expense.id}")
                print(f"   Paid By: {expense.paid_by.name} ({expense.paid_by.id})")
                print(f"   Amount: {expense.amount:.2f}")
                split_type_display = expense.split_type.replace('SplitStrategy', '').replace('Strategy', '')
                print(f"   Split Type: {split_type_display}")
                if expense.participants:
                    participants_str = ", ".join(
                        f"{u.name} ({u.id})" for u in expense.participants
                    )
                    print(f"   Participants: {participants_str}")
                print("   Shares:")
                for user, value in expense.split().items():
                    print(f"      - {user.name} ({user.id}): {value:.2f}")
        except ValueError:
            print("❌ Invalid number format!")
        except Exception as e:
            print(f"❌ Error retrieving expenses: {e}")

    # Settlement & Balances
    def view_balances(self):
        try:
            groups = self.services["group"].list_groups()
            if not groups:
                print("\n❌ No groups available.")
                return

            print("\n--- Available Groups ---")
            for group in groups:
                print(f"{group.id}. {group.name}")

            group_id = input("\nEnter group ID: ").strip()

            if not group_id:
                print("❌ Group ID cannot be empty!")
                return

            group_details = self.services["group"].get_group_details(int(group_id))
            balances = self.services["settlement"].get_balances(int(group_id))

            if not balances:
                print("No balances found for this group.")
                return

            print(f"\n--- Balances for {group_details.name} ---")
            print(f"Group Members: {', '.join(f'{m.name} ({m.id})' for m in group_details.members)}")
            print("\nBalance Summary:")
            for user, balance in balances.items():
                balance_status = "owes" if balance < 0 else "is owed"
                print(f"   {user.name} ({user.id}): {abs(balance):.2f} {balance_status}")

        except ValueError:
            print("❌ Invalid number format!")
        except Exception as e:
            print(f"❌ Error retrieving balances: {e}")

    def settlement_menu(self):
        while True:
            self.display_settlement_menu()
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.view_balances()
            elif choice == "2":
                self.show_settlement_suggestions()
            elif choice == "3":
                break
            else:
                print("❌ Invalid choice. Please try again.")

    def show_settlement_suggestions(self):
        try:
            groups = self.services["group"].list_groups()
            if not groups:
                print("\n❌ No groups available.")
                return

            print("\n--- Available Groups ---")
            for group in groups:
                print(f"{group.id}. {group.name}")

            group_id = input("\nEnter group ID: ").strip()

            if not group_id:
                print("❌ Group ID cannot be empty!")
                return

            group_details = self.services["group"].get_group_details(int(group_id))
            suggestions = self.services["settlement"].get_settlement_suggestions(int(group_id))

            print(f"\n--- Settlement Suggestions for {group_details.name} ---")
            print(f"Group Members: {', '.join(f'{m.name} ({m.id})' for m in group_details.members)}")

            if not suggestions:
                print("\n✅ Everyone is settled up already!")
                return

            print("\nSuggested Payments:")
            for payer, receiver, amount in suggestions:
                print(f"   {payer.name} ({payer.id}) ➜ {receiver.name} ({receiver.id}): {amount:.2f}")
        except ValueError:
            print("❌ Invalid number format!")
        except Exception as e:
            print(f"❌ Error computing suggestions: {e}")

    # Main loop
    def run(self):
        while self.running:
            self.display_main_menu()
            choice = input("Select an option: ").strip()

            if choice == "1":
                self.user_menu()
            elif choice == "2":
                self.group_menu()
            elif choice == "3":
                self.expense_menu()
            elif choice == "4":
                self.settlement_menu()
            elif choice == "5":
                self.running = False
            else:
                print("❌ Invalid choice. Please try again.")


async def main_async():
    # logging.basicConfig(level=logging.INFO)

    services = build_services()

    asyncio.create_task(
        periodic_balance_logger(
            settlement_service=services["settlement"],
            group_repository=services["group_repo"],
            interval_seconds=30
        )
    )

    menu = MenuDrivenInterface(services)
    menu.run()


def main():
    setup_logging()
    asyncio.run(main_async())


if __name__ == "__main__":
    main()

