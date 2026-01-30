import asyncio
import logging
from uuid import UUID

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
        print("2. Back to Main Menu")

    def display_group_menu(self):
        print("\n--- Group Management ---")
        print("1. Create Group")
        print("2. Add Member to Group")
        print("3. Back to Main Menu")

    def display_expense_menu(self):
        print("\n--- Expense Management ---")
        print("1. Add Expense")
        print("2. Back to Main Menu")

    def display_settlement_menu(self):
        print("\n--- Settlement & Balances ---")
        print("1. View Group Balances")
        print("2. Back to Main Menu")

    # User Management
    def create_user(self):
        name = input("Enter user name: ").strip()
        if not name:
            print("❌ User name cannot be empty!")
            return
        
        try:
            user = self.services["user"].create_user(name)
            print(f"✅ User created successfully!")
            print(f"   ID: {user.id}")
            print(f"   Name: {user.name}")
        except Exception as e:
            print(f"❌ Error creating user: {e}")

    def user_menu(self):
        while True:
            self.display_user_menu()
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                self.create_user()
            elif choice == "2":
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
            print(f"✅ Group created successfully!")
            print(f"   ID: {group.id}")
            print(f"   Name: {group.name}")
        except Exception as e:
            print(f"❌ Error creating group: {e}")

    def add_member_to_group(self):
        group_id = input("Enter group ID: ").strip()
        user_id = input("Enter user ID: ").strip()
        
        if not group_id or not user_id:
            print("❌ Group ID and User ID cannot be empty!")
            return
        
        try:
            self.services["group"].add_member(UUID(group_id), UUID(user_id))
            print("✅ Member added to group successfully!")
        except ValueError:
            print("❌ Invalid UUID format!")
        except Exception as e:
            print(f"❌ Error adding member: {e}")

    def group_menu(self):
        while True:
            self.display_group_menu()
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                self.create_group()
            elif choice == "2":
                self.add_member_to_group()
            elif choice == "3":
                break
            else:
                print("❌ Invalid choice. Please try again.")

    # Expense Management
    def add_expense(self):
        try:
            group_id = input("Enter group ID: ").strip()
            paid_by_id = input("Enter payer user ID: ").strip()
            amount = input("Enter expense amount: ").strip()
            participants_str = input("Enter participant IDs (comma-separated): ").strip()
            split_type = input("Enter split type (equal/percentage/custom): ").strip()
            
            if not all([group_id, paid_by_id, amount, participants_str, split_type]):
                print("❌ All fields are required!")
                return
            
            participants = [UUID(uid.strip()) for uid in participants_str.split(",")]
            
            split_data = None
            if split_type == "percentage":
                split_data = {}
                data_str = input("Enter split data (user_id:percentage, comma-separated): ").strip()
                for item in data_str.split(","):
                    uid, value = item.split(":")
                    split_data[UUID(uid.strip())] = float(value.strip())
            elif split_type == "custom":
                split_data = {}
                data_str = input("Enter split data (user_id:amount, comma-separated): ").strip()
                for item in data_str.split(","):
                    uid, value = item.split(":")
                    split_data[UUID(uid.strip())] = float(value.strip())
            
            expense = self.services["expense"].add_expense(
                group_id=UUID(group_id),
                paid_by_id=UUID(paid_by_id),
                participant_ids=participants,
                amount=float(amount),
                split_type=SplitType(split_type),
                split_data=split_data
            )
            
            print(f"✅ Expense added successfully!")
            print(f"   ID: {expense.id}")
            print(f"   Amount: {expense.amount}")
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
                break
            else:
                print("❌ Invalid choice. Please try again.")

    # Settlement & Balances
    def view_balances(self):
        group_id = input("Enter group ID: ").strip()
        
        if not group_id:
            print("❌ Group ID cannot be empty!")
            return
        
        try:
            balances = self.services["settlement"].get_balances(UUID(group_id))
            
            if not balances:
                print("No balances found for this group.")
                return
            
            print("\n--- Group Balances ---")
            for user, balance in balances.items():
                status = "Owed" if balance > 0 else "Owes"
                print(f"  {user.name}: {status} {abs(balance):.2f}")
        except ValueError:
            print("❌ Invalid UUID format!")
        except Exception as e:
            print(f"❌ Error retrieving balances: {e}")

    def settlement_menu(self):
        while True:
            self.display_settlement_menu()
            choice = input("Select an option: ").strip()
            
            if choice == "1":
                self.view_balances()
            elif choice == "2":
                break
            else:
                print("❌ Invalid choice. Please try again.")

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
                print("👋 Goodbye!")
                self.running = False
            else:
                print("❌ Invalid choice. Please try again.")


async def main_async():
    logging.basicConfig(level=logging.INFO)

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

