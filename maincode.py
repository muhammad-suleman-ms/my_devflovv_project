import psycopg2
from tabulate import tabulate

def connect():
    return psycopg2.connect(
        dbname="newdb",
        user="suleman",
        password="008808",
        host="localhost",
        port="5432"
    )

def create_user(conn, name, phone_number, address, email):
    with conn.cursor() as cur:
        cur.execute(
            "INSERT INTO users (name, phone_number, address, email) VALUES (%s, %s, %s, %s)",
            (name, phone_number, address, email)
        )
        conn.commit()

def del_user_by_email(conn, email):
    with conn.cursor() as cur:
        cur.execute(
            "DELETE FROM users WHERE email = %s", (email,)
        )
        return cur

def update_user(conn, name, phone_number, address, email):
    with conn.cursor() as cur:
        cur.execute(
            "UPDATE users SET name = %s, phone_number = %s, address = %s WHERE email = %s",
            (name, phone_number, address, email)
        )
        conn.commit()

def get_all_users(conn):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users")
        return cur.fetchall()
 
def delete_user_by_email(conn, email):
    with conn.cursor() as cur:
         cur.execute("DELETE FROM users WHERE email = %s", (email,))
         conn.commit()   

def main():
    conn = connect()
    print(conn)
    
    while True:
        choice = input("Enter 1 to add new user, 2 to update existing user, 3 to show all users,Enter 4 to delete user from email , or 0 to exit: ")
        
        if choice == '1':
            name = input("Enter name: ")
            phone_number = input("Enter phone number: ")
            address = input("Enter address: ")
            email = input("Enter email: ")
            
            create_user(conn, name, phone_number, address, email)
            print("User added successfully!")
        
        elif choice == '2':
            email = input("Enter email of the user to update: ")
            user = get_user_by_email(conn, email)
            
            if user:
                print("Current user data:")
                print(tabulate([user[1:]], headers=["Name", "Phone Number", "Address", "Email"]))
                
                name = input("Enter new name (leave blank to keep current): ") or user[1]
                phone_number = input("Enter new phone number (leave blank to keep current): ") or user[2]
                address = input("Enter new address (leave blank to keep current): ") or user[3]
                
                update_user(conn, name, phone_number, address, email)
                print("User updated successfully!")
            else:
                print("User not found!")
        
        elif choice == '3':
            users = get_all_users(conn)
            if users:
                print("All users:")
                print(tabulate(users, headers=["ID", "Name", "Phone Number", "Address", "Email"]))
            else:
                print("No users found!")
                
        elif choice == '4':
            email = input("Enter the email of the user you want t Delete From tha Database : ")
            users = del_user_by_email(conn,email)
            if users:
                delete_user_by_email(conn,email)
                print("User Deleted Sucessfully:")  
               
            else:
                print("No users found!")        
        
        elif choice == '0':
            break
        
        else:
            print("Invalid choice! Please try again.")
    
    conn.close()

if __name__ == "__main__":
    main()
