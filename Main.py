import json
import hashlib
from json import JSONEncoder


class Item:
    def __init__(self, name, description, price, available=True):
        self.name = name
        self.description = description
        self.price = price
        self.available = available

    def to_dict(self):
        return {
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'available': self.available
        }


class User:
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = hashlib.sha256(password.encode()).hexdigest()  # Hash the password
        self.rented_items = []

    def rent_item(self, item):
        self.rented_items.append(item)

    def return_item(self, item):
        if item in self.rented_items:
            self.rented_items.remove(item)
            print(f"Item '{item.name}' returned successfully.")
        else:
            print("You haven't rented this item.")

    def update_profile(self, email=None, password=None):
        if email:
            self.email = email
        if password:
            self.password = hashlib.sha256(password.encode()).hexdigest()


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Item):
            return obj.__dict__
        elif isinstance(obj, User):
            return obj.__dict__
        return super().default(obj)


class RentalService:
    def __init__(self):
        self.items = []
        self.users = []
        self.logged_in_user = None
        self.admin_password = "admin123"

    def add_item(self, item):
        self.items.append(item)

    def list_items(self):
        print("\nAvailable Items:")
        for i, item in enumerate(self.items, start=1):
            print(f"{i}. {item.name} - ${item.price} ({'Available' if item.available else 'Not Available'})")
            print(f"Description: {item.description}")

    def rent_item(self, item_index):
        if self.logged_in_user:
            if 0 < item_index <= len(self.items):
                item = self.items[item_index - 1]
                if item.available:
                    item.available = False
                    self.logged_in_user.rent_item(item)
                    print(f"Congratulations, {self.logged_in_user.username}! You have rented {item.name}.")
                    print("Please return the item within 7 days.")
                else:
                    print("Sorry, this item is not available for rent.")
            else:
                print("Invalid item index.")
        else:
            print("Please log in to rent items.")

    def return_item(self, item_index):
        if self.logged_in_user:
            if 0 < item_index <= len(self.logged_in_user.rented_items):
                returned_item = self.logged_in_user.rented_items.pop(item_index - 1)
                returned_item.available = True
                self.items.append(returned_item)
                print(f"Item '{returned_item.name}' returned successfully.")
            else:
                print("Invalid item index.")
        else:
            print("Please log in to return items.")

    def sign_up(self, username, email, password):
        if not any(user.username == username for user in self.users):
            self.users.append(User(username, email, password))
            print("Sign up successful. Please log in.")
        else:
            print("Username already exists. Please choose another username.")

    def login(self, username, password):
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        for user in self.users:
            if user.username == username and user.password == hashed_password:
                self.logged_in_user = user
                print("Login successful.")
                return
        print("Invalid username or password.")

    def save_data(self):
        with open('items.json', 'w') as f:
            json.dump(self.items, f, cls=CustomJSONEncoder)
        with open('users.json', 'w') as f:
            json.dump(self.users, f, cls=CustomJSONEncoder)

    def load_data(self):
        try:
            with open('items.json', 'r') as f:
                data = json.load(f)
                self.items = [Item(item['name'], item['description'], item['price'], item['available']) for item in
                              data]
            with open('users.json', 'r') as f:
                data = json.load(f)
                self.users = [User(user['username'], user['email'], user['password']) for user in data]
        except (FileNotFoundError, json.JSONDecodeError):
            # Handle the case where the file is empty or contains invalid JSON data
            # For example, you can initialize self.items and self.users as empty lists
            self.items = []
            self.users = []

    def view_rented_items(self):
        if self.logged_in_user:
            print("\nRented Items:")
            for i, item in enumerate(self.logged_in_user.rented_items, start=1):
                print(f"{i}. {item.name} - ${item.price} ({item.description})")
        else:
            print("Please log in to view rented items.")

    def view_profile(self):
        if self.logged_in_user:
            print(f"\nUsername: {self.logged_in_user.username}")
            print(f"Email: {self.logged_in_user.email}")
        else:
            print("Please log in to view profile.")

    def update_profile(self, email=None, password=None):
        if self.logged_in_user:
            self.logged_in_user.update_profile(email, password)
            print("Profile updated successfully.")
        else:
            print("Please log in to update profile.")

    def delete_account(self):
        if self.logged_in_user:
            self.users.remove(self.logged_in_user)
            self.logged_in_user = None
            print("Account deleted successfully.")
        else:
            print("Please log in to delete account.")

    def admin_dashboard(self):
        admin_password = input("\nPlease enter admin password: ")
        if admin_password == "admin123":
            print("\nAdmin Dashboard:")
            print("1. View All Users")
            print("2. Delete User Account")
            choice = input("Enter your choice: ")
            if choice == '1':
                print("\nAll Users:")
                for user in self.users:
                    print(f"Username: {user.username}, Email: {user.email}")
            elif choice == '2':
                username = input("Enter the username of the account you want to delete: ")
                user_to_delete = next((user for user in self.users if user.username == username), None)
                if user_to_delete:
                    self.users.remove(user_to_delete)
                    print(f"User '{username}' account deleted successfully.")
                else:
                    print("User not found.")
            else:
                print("Invalid choice.")

        else:
            print("Admin access denied.")


def main():
    rental_service = RentalService()
    rental_service.load_data()

    while True:
        print("\n1. Sign Up")
        print("2. Log In")
        print("3. Add Item")
        print("4. List Items")
        print("5. Rent Item")
        print("6. Return Item")
        print("7. View Rented Items")
        print("8. View Profile")
        print("9. Update Profile")
        print("10. Delete Account")
        print("11. Admin Dashboard")
        print("12. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            print("\nSign Up:")
            username = input("Enter username: ")
            email = input("Enter email: ")
            password = input("Enter password: ")
            rental_service.sign_up(username, email, password)

        elif choice == '2':
            print("\nLog In:")
            username = input("Enter username: ")
            password = input("Enter password: ")
            rental_service.login(username, password)

        elif choice == '3':
            print("\nAdd Item:")
            if rental_service.logged_in_user:
                name = input("Enter item name: ")
                description = input("Enter item description: ")
                price = float(input("Enter item price: "))
                item = Item(name, description, price)
                rental_service.add_item(item)
                rental_service.save_data()
                print("Item added successfully.")
            else:
                print("Please log in to add items.")

        elif choice == '4':
            print("\nList Items:")
            rental_service.list_items()

        elif choice == '5':
            print("\nRent Item:")
            if rental_service.logged_in_user:
                rental_service.list_items()
                item_index = int(input("Enter the index of the item you want to rent: "))
                rental_service.rent_item(item_index)
                rental_service.save_data()
            else:
                print("Please log in to rent items.")

        elif choice == '6':
            print("\nReturn Item:")
            if rental_service.logged_in_user:
                rental_service.view_rented_items()
                item_index = int(input("Enter the index of the item you want to return: "))
                rental_service.return_item(item_index)
                rental_service.save_data()
            else:
                print("Please log in to return items.")

        elif choice == '7':
            print("\nView Rented Items:")
            rental_service.view_rented_items()

        elif choice == '8':
            print("\nView Profile:")
            rental_service.view_profile()

        elif choice == '9':
            print("\nUpdate Profile:")
            email = input("Enter new email (leave blank to keep current): ")
            password = input("Enter new password (leave blank to keep current): ")
            rental_service.update_profile(email, password)
            rental_service.save_data()

        elif choice == '10':
            print("\nDelete Account:")
            rental_service.delete_account()
            rental_service.save_data()

        elif choice == '11':
            print("\nAdmin Dashboard:")
            rental_service.admin_dashboard()
            rental_service.save_data()

        elif choice == '12':
            print("Thank you for using our service. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
