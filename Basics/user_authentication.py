user = ['Ansh', 'Jinay','Krish','Pratham']

while True:
    print("\nUser Management System")
    print("1. View users")
    print("2. Add user")
    print("3. Remove user")
    print("4. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        print("Registered users are: " )
        for i in user:
            print(i)
    
    elif choice == 2:
        name = input("Enter name: ")
        user.append(name)
        for i in user:
            print(i)

    elif choice == 3:
        name = input("Enter name to remove from list: ")
        if name in user:
            user.remove(name)

            for i in user:
                print(i)

    elif choice == 4:
        print("Exit the system..")
        break

    else: 
        print("Invalid input")
        break
        
                



