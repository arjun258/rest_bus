import mysql.connector as sqltor
import time
conn = sqltor.connect(
    host="localhost",        
    user="root",             
    password="arjun@1602",
    database="rest_bus" 
)

if conn.is_connected():
    print("Connected to MySQL database!")

# Create a cursor to run SQL commands
cursor = conn.cursor()
cust_name = ""
current_billid = None

conn.commit()
def sleep():
     time.sleep(0)

def check_item_in_menu(item_srno):
     global cursor
     menu_sr = []
     cursor.execute("select serial_number, item from menu")
     menu = cursor.fetchall()
     for i in menu:
          menu_sr.append(i[0])
     if item_srno.isdigit():
        if int(item_srno) in menu_sr:
            return True
        else: print("Dish doesn't exist in menu. Please enter the correct serial number.")
     else: print("Please enter an integer.")
    
def place_order(sr_no):
     global cursor,current_billid
     ## creating a list of all srno of dish
     menu_sr = []
     cursor.execute("select serial_number,item from menu")
     menu = cursor.fetchall()
     for i in menu:
          menu_sr.append(i[0])

     ## checking if its a existing bill or a new bill is to be created 
     if current_billid == None:
        ## creating order of customer
        ## initializing strings for item names and item serial numbers
        item_srno_string = ""
        item_name_string = ""

        ##adding values to the above strings 
        for i in sr_no:

            item_srno_string += f"{str(i).strip()},"
            
            # fetching item name as per item srno and making string of item names
        for i in sr_no:
            for k in menu:
                if k[0] == int(i):
                    item_name_string += f"{k[1].strip()},"
                
            ## pushing all values to database 
        cursor.execute("insert into pre_bill (cust_name,item_id,item_name) values(%s,%s,%s)",(cust_name,item_srno_string,item_name_string,))
        conn.commit()
        ## updating the variable current bill id
        current_billid = cursor.lastrowid
        
     else:
        ## fetching strings of item names and item serial numbers
        cursor.execute(f"select item_id from pre_bill where billid = {current_billid}")
        item_srno_string = cursor.fetchone()
        cursor.execute(f"select item_name from pre_bill where billid = {current_billid}")
        item_name_string = cursor.fetchone()

        new_item_name_string = item_name_string[0]
        new_item_srno_string = item_srno_string[0]
        ##adding values to the above strings 
        for i in sr_no:
            new_item_srno_string += f"{str(i).strip()},"
            
            # fetching item name as per item srno and making string of item names
            for k in menu:
                if k[0] == int(i):
                    new_item_name_string += f"{k[1].strip()},"
                
        ## clearing the existing item name and item id strings and then pushing the new values 

        cursor.execute(f"update pre_bill set item_id = NULL,item_name = NULL where billid = {current_billid}")
        conn.commit()
        cursor.execute( "UPDATE pre_bill SET item_id = %s, item_name = %s WHERE billid = %s",(new_item_srno_string, new_item_name_string, current_billid))
        conn.commit()
           
def order():
      
      cust_order_list  = []
      print("""Provided below is our menu. Please take a look at it and order your food by entering the serial numbers of the dishes.\n""")
      cursor.execute("SELECT * FROM menu")
      rows = cursor.fetchall()
      cursor.execute("SELECT item, amt_ordered FROM menu where amt_ordered !=0 ORDER BY amt_ordered DESC LIMIT 1")
      bestseller = cursor.fetchone()
      cursor.execute("SELECT item, rating FROM menu WHERE rating IS NOT NULL ORDER BY rating DESC LIMIT 1")
      high_rated = cursor.fetchone()
      sleep()

      
      print("\n" + "="*80)
      print(f"{'Sr':<5} {'Item':<25} {'Amount':<10} {'Category':<15} {'Rating':<10}")
      print("="*80)
      for row in rows:
        serial = row[0]
        item = row[1]
        amount = row[2]
        category = row[4]
        rating = row[3] if row[3] else "N/A"
        print(f"{serial:<5} {item:<25} ₹{amount:<9} {category:<15} {rating:<10}")
      print("="*80)

      print("\n" + "HIGHLIGHTS ".center(80, "="))
      print(f"{'':30} {'SrNo':<30} {'Name':<10}")
      print("-"*80)
      if bestseller:
        print(f"{'Bestseller:':<30} {bestseller[1]:<30} {bestseller[0]}")
      else:
          print(f"{'Bestseller:':<30} NA")
      if high_rated:
        print(f"{'Highest Rated:':<30} {high_rated[1]:<30} {high_rated[0]}")
      else:
          print(f"{'Highest Rated:':<30} NA")
      print("="*80 + "\n")


      while True:
            cust_order = input("Please enter the serial number of the dish you would like to order: ")
            if check_item_in_menu(cust_order) == True:
                cust_order_list.append(cust_order)
                choice = input("Would you like to order more? (yes/no): ")
                if choice.lower() == "no":
                    place_order(cust_order_list)
                    print("Your order has been placed! Thank you.")
                    break
                

def ask_rating():
    global cursor,conn,current_billid
    
    def push_item_rating(rating,srno):
        cursor.execute("select rating_list from menu where serial_number = %s",(srno,))
        rating_list = cursor.fetchone()
        rating_string = ""

        if rating_list[0] == None:
            rating_string += f"{rating.strip()},"
        else:
            rating_string = rating_list[0].strip()+f"{rating.strip()},"

        #updating the average rating of the dish
        rating_list = rating_string.strip(',').split(',')
        sum_rating = 0 
        for i in rating_list:
            sum_rating += int(i)
        item_avgrating = sum_rating/len(rating_list)
            
        #pushing everything to database
        cursor.execute("update menu set rating_list = NULL where serial_number = %s",(srno,))
        cursor.execute("UPDATE menu SET rating_list = %s, rating = %s WHERE serial_number = %s",(rating_string,item_avgrating,srno))
        conn.commit()

        
    def check_rating (value):
        if value.isdigit() and int(value) >= 0 and int(value) <= 5:
            return True 
        else:
            print("Please provide a valid integer rating between 0 and 5.")
            return False
    def item_rating():
        # fetching srno of all items ordered as well as fetching the menu 
        cursor.execute(f"select item_id from pre_bill where billid = %s",(current_billid,))
        items_ordered = cursor.fetchall()
        cursor.execute("select serial_number, item from menu")
        menu = cursor.fetchall()
        list_items = items_ordered[0][0].strip(',').split(',')

        for i in list_items:
            for k in menu:
                if int(i) == k[0]:
                    while True:
                        rating = input(f"How would you rate the {k[1]}? (0-5): ")
                        if check_rating(rating):
                            push_item_rating(rating,i)
                            break
                        
        
        
    print('\nPlease answer the following questions by providing an integer rating between 0 and 5, where 0 is the lowest and 5 is the highest.\n')
    while True:
        overall_rating = input("How would you rate your overall experience at our restaurant? (0-5): ")
        if check_rating(overall_rating):
            item_rating()
            cursor.execute("UPDATE final_bill SET rating = %s WHERE billid = %s",(overall_rating,current_billid,))
            conn.commit()
            break
    
def gen_final_bill():
    global current_billid,cursor,conn
    amount = 0 
    def amt_ordered_updater(item_sr):
        cursor.execute("update menu set amt_ordered = amt_ordered + 1 where serial_number = %s",(item_sr,))

    ## calculating amount 
    cursor.execute(f"select item_id,item_name,cust_name from pre_bill where billid = %s",(current_billid,))
    items_ordered = cursor.fetchall()
    cursor.execute("select serial_number, amount from menu")
    menu = cursor.fetchall()

    ## creating list of srno of items ordered by customer
    list_items = items_ordered[0][0].strip(',').split(',')

    ## calculating amount
    for i in list_items:
        amt_ordered_updater(i)
        for k in menu:
            if int(i) == k[0]:
                amount += k[1]
    # creating the final bill.
    cursor.execute("insert into final_bill (billid, amount,date,item_name,cust_name) values(%s,%s,curdate(),%s,%s)",(current_billid,amount,items_ordered[0][1],items_ordered[0][2]))
    conn.commit()
    print(f"Sure! Your bill amount is ₹{amount}.")
    

## Management dashboard functions 

def display_all_orders():
    global cursor,conn
    cursor.execute("select * from final_bill")
    order_data = cursor.fetchall()
    print("\n" + "="*100)
    print(f"{'Bill ID':<10} {'Amount':<10} {'Rating':<10} {'Date':<15} {'Customer Name':<20} {'Items':<30}")
    print("="*100)  
    for row in order_data:
        billid = row[0]
        amount = row[1] if row[1] else "N/A"
        rating = row[2] if row[2] else "N/A"
        date = row[3] if row[3] else "N/A"
        cust_name = row[4] if row[4] else "N/A"
        item_name = row[5] if row[5] else "N/A"
        print(f"{billid:<10} {amount:<10} {rating:<10} {str(date):<15} {cust_name:<20} {item_name:<30}")
    print("="*100 + "\n")

def edit_menu():
    def menu_print():
        print("""Provided below is the current menu. What would you like to do?\n""")
        cursor.execute("SELECT * FROM menu")
        rows = cursor.fetchall()
        sleep()

        print("\n" + "="*80)
        print(f"{'Sr':<5} {'Item':<25} {'Amount':<10} {'Category':<15} {'Rating':<10}")
        print("="*80)
        for row in rows:
            serial = row[0]
            item = row[1]
            amount = row[2]
            category = row[4]
            rating = row[3] if row[3] else "N/A"
            print(f"{serial:<5} {item:<25} ₹{amount:<9} {category:<15} {rating:<10}")
        print("="*80)
    
    menu_print()

    while True:
        print("\n1. Add Item \n2. Remove Item \n3. Edit Item \n4. Go to Main Management Menu")

        try:
            edit_menu_choice = int(input("Enter your choice: "))
            
            if edit_menu_choice == 1:
                # Add Item
                while True:
                    item_name = input("Enter item name: ")
                    amount = int(input("Enter amount: "))
                    category = input("Enter category: ")
                    
                    cursor.execute("INSERT INTO menu (item, amount, category) VALUES (%s, %s, %s)", 
                                (item_name, amount, category))
                    conn.commit()
                    print(f"{item_name} has been added to the menu!")
                    menu_print()
                    add_item_choice = input("Would you like to add more items? (yes/no): ")
                    if add_item_choice.lower() == "no":
                        break

            elif edit_menu_choice == 2:
                # Remove Item
                while True:
                    srno = input("Enter the serial number of the item to delete: ")
                    
                    if check_item_in_menu(srno):
                        cursor.execute("DELETE FROM menu WHERE serial_number = %s", (int(srno),))
                        conn.commit()
                        print(f"Item with serial number {srno} has been deleted!")
                        menu_print()
                        delete_item_choice = input("Would you like to delete more items? (yes/no): ")
                        if delete_item_choice.lower() == "no":
                            break
                    else:
                        print("Item not found in menu.")
                        break

            elif edit_menu_choice == 3:
                # Edit Item
                while True:
                    srno = input("Enter the serial number of the item to edit: ")
                    
                    if check_item_in_menu(srno):
                        while True:
                            print("\nWhat would you like to edit?")
                            print("1. Item Name\n2. Amount\n3. Category")
                            edit_choice = int(input("Enter your choice: "))
                            
                            if edit_choice == 1:
                                new_name = input("Enter new item name: ")
                                cursor.execute("UPDATE menu SET item = %s WHERE serial_number = %s", 
                                            (new_name, int(srno)))
                                conn.commit()
                                print(f"Item name updated successfully!")
                                menu_print()
                                
                            elif edit_choice == 2:
                                new_amount = int(input("Enter new amount: "))
                                cursor.execute("UPDATE menu SET amount = %s WHERE serial_number = %s", 
                                            (new_amount, int(srno)))
                                conn.commit()
                                print(f"Amount updated successfully!")
                                menu_print()
                                
                            elif edit_choice == 3:
                                new_category = input("Enter new category: ")
                                cursor.execute("UPDATE menu SET category = %s WHERE serial_number = %s", 
                                            (new_category, int(srno)))
                                conn.commit()
                                print(f"Category updated successfully!")
                                menu_print()

                            else:
                                print("Invalid choice!")
                            
                            edit_item_choice = input("Would you like to edit more details of the current item? (yes/no): ")
                            if edit_item_choice.lower() == "no":
                                break
                    else:
                        print("Item not found in menu.")
                        break
                    
                    edit_another_item = input("Would you like to edit details of any other item? (yes/no): ")
                    if edit_another_item.lower() == "no":
                        break

            elif edit_menu_choice == 4:
                print("Returning to main management menu...")
                break

            else:
                print("Invalid choice! Please enter 1, 2, 3, or 4.")
            
        except ValueError:
            print("Please enter a valid integer as choice.")

def see_food_rating():
    print("\n" + "="*60)
    print("FOOD RATINGS")
    print("="*60)
    
    cursor.execute("SELECT serial_number, item, rating FROM menu ORDER BY rating DESC")
    rows = cursor.fetchall()
    
    print(f"{'Sr':<10} {'Item':<30} {'Rating':<10}")
    print("-"*60)
    
    for row in rows:
        serial = row[0]
        item = row[1]
        rating = row[2] if row[2] else "N/A"
        print(f"{serial:<10} {item:<30} {rating:<10}")
    
    print("="*60 + "\n")
      
def general_stats():
    print("\n" + "="*80)
    print("GENERAL STATISTICS".center(80))
    print("="*80)
    
    # Total Orders
    cursor.execute("SELECT COUNT(*) FROM final_bill")
    total_orders = cursor.fetchone()[0]
    
    # Total Revenue
    cursor.execute("SELECT SUM(amount) FROM final_bill")
    total_revenue = cursor.fetchone()[0]
    total_revenue = total_revenue if total_revenue else 0
    
    # Average Order Value
    avg_order_value = total_revenue / total_orders if total_orders > 0 else 0
    
    # Bestseller (highest ordered dish)
    cursor.execute("SELECT item, amt_ordered FROM menu where amt_ordered !=0 ORDER BY amt_ordered DESC LIMIT 1")
    bestseller = cursor.fetchone()
    
    # Highest Rated Dish
    cursor.execute("SELECT item, rating FROM menu WHERE rating IS NOT NULL ORDER BY rating DESC LIMIT 1")
    highest_rated = cursor.fetchone()
    
    # Average Rating across all dishes
    cursor.execute("SELECT AVG(rating) FROM menu WHERE rating IS NOT NULL")
    avg_rating = cursor.fetchone()[0]
    avg_rating = round(avg_rating, 2) if avg_rating else "N/A"
    
    # Average Customer Satisfaction (from final_bill ratings)
    cursor.execute("SELECT AVG(rating) FROM final_bill WHERE rating IS NOT NULL")
    avg_customer_rating = cursor.fetchone()[0]
    avg_customer_rating = round(avg_customer_rating, 2) if avg_customer_rating else "N/A"
    
    # Total Menu Items
    cursor.execute("SELECT COUNT(*) FROM menu")
    total_menu_items = cursor.fetchone()[0]
    
    # Display Stats
    print(f"\n{'Metric':<40} {'Value':<20}")
    print("-"*80)
    print(f"{'Total Orders:':<40} {total_orders}")
    print(f"{'Total Revenue:':<40} ₹{total_revenue}")
    print(f"{'Average Order Value:':<40} ₹{round(avg_order_value, 2)}")
    print(f"{'Total Menu Items:':<40} {total_menu_items}")
    print(f"{'Average Food Rating:':<40} {avg_rating}/5")
    print(f"{'Average Customer Satisfaction:':<40} {avg_customer_rating}/5")
    
    if bestseller:
        print(f"{'Bestseller:':<40} {bestseller[0]} ({bestseller[1]} orders)")
    
    if highest_rated:
        print(f"{'Highest Rated Dish:':<40} {highest_rated[0]} ({highest_rated[1]}/5)")
    
    print("="*80 + "\n")

def show_dish_order_count():
    print("\n" + "="*80)
    print("DISH ORDER STATISTICS".center(80))
    print("="*80)
    
    cursor.execute("SELECT serial_number, item, amt_ordered FROM menu ORDER BY amt_ordered DESC")
    rows = cursor.fetchall()
    
    print(f"\n{'Sr':<10} {'Dish Name':<40} {'Times Ordered':<20}")
    print("-"*80)
    
    total_items_ordered = 0
    for row in rows:
        serial = row[0]
        item = row[1]
        amt_ordered = row[2] if row[2] else 0
        total_items_ordered += amt_ordered
        
        print(f"{serial:<10} {item:<40} {amt_ordered:<20}")
    
    print("-"*80)
    print(f"{'TOTAL ITEMS ORDERED:':<50} {total_items_ordered:<20}")
    print("="*80 + "\n")


def python_menu ():
    global cust_name,gen_final_bill,current_billid
    print("""\nWelcome to our Restaurant!\n""")
    while True:
        print("1. Customer Dashboard \n2. Management Dashboard \n3. Exit Program")

        try:
            dash_choice = int(input("Please enter your choice (1, 2, or 3): "))
            if dash_choice == 1 :
                try:
                    cust_name = input("May we know your name? ")
                except ValueError:
                    print("Please enter name as a string.")
                while True:
                    print("\n1. Order \n2. Bill Please \n 3. Return to Previous Menu")
                    try:
                        choice = int(input("Enter your choice: "))
                    except ValueError:
                        print("Please enter an integer as choice.")
                    if choice == 1:
                        order()
                    elif choice == 2:
                        if current_billid != None:
                            gen_final_bill()
                            while True:
                                pay_confirm = input("Please let me know when you have paid the amount (type 'paid'): ")
                                if pay_confirm.lower() == "paid":
                                    rating_consent = input("Would you like to provide us some feedback or rating? (yes/no): ")
                                    if rating_consent.lower() == "yes":
                                        ask_rating()
                                        print("Thank you for visiting! Please visit again.")
                                        current_billid = None
                                        return
                                    else:
                                        print("Thank you for visiting! Please visit again.")
                                        current_billid = None
                                        return
                        else:
                            print("Please order first.")
                    elif choice == 3 :
                        break
            elif dash_choice == 2:
                    
                    print("\nWelcome to the Management Dashboard of the restaurant. What would you like to do?\n")
                    while True:
                        print("1. Display All Orders \n2. Edit Menu \n3. See Food Ratings \n4. General Statistics \n5. Show Amount of Dishes Ordered \n6. Go to Previous Menu \n7. Exit Program")
                        try:
                            manage_choice = int(input("Enter your choice: "))

                            if manage_choice == 1:
                                display_all_orders()
                            elif manage_choice == 2:
                                edit_menu()
                            elif manage_choice == 3:
                                see_food_rating()
                            elif manage_choice == 4:
                                general_stats()
                            elif manage_choice == 5 :
                                show_dish_order_count()
                                
                            elif manage_choice == 6:
                                break
                            elif manage_choice == 7:
                                return
                            else:
                                print("Invalid choice! Please enter a number between 1-7.")
                        except ValueError:
                            print("Please enter an integer as choice.")
            elif dash_choice == 3 :
                print("Thank you for using our Restaurant Management System!")
                return

        except ValueError:
            print("Please enter an integer as choice.")
                        
                        
python_menu()
