#Real world application using control structures
# Assignment2 : Create a E-commerce that checks inputs like subtotal, discount, 
# and tax to calculate the final price of a product. 
# Include the coupon code for discount and tax rate for the calculation.
# Use nested conditions to handle different scenarios such as valid/invalid 
# coupon codes,
# different tax rates based on location, and various discount levels based on 
# the subtotal amount.
# Implement login system for the e-commerce platform that checks user credentials
#  and in the system, there are three types of users: Admin, Customers, and Cashiers.
#  Each user has his password and different access levels. 
# Admin can access all features, Customers can


def check_location(location):
    match location:
        case "Uganda":
            return 0.18
        case "Kenya":
            return 0.16
        case "Tanzania":
            return 0.18
        case "Rwanda":
            return 0.18  
        case _:
            print("Country not supported. No location discount applied")
            return 0.0   

def check_coupon_code(coupon_code):

    match coupon_code:
        case "CU435x":
            return 0.1
        case "Yu234C":
            return 0.4
        case "TY3345x":
            return 0.7  
        case _:
            print("Invalid coupon code. No coupon discount applied")
            return 0.0    


def compute_grand_total(subtotal, location, coupon_code):        
    coupon_discount = check_coupon_code(coupon_code) * subtotal
    discounted_subtotal = subtotal - coupon_discount
    
    tax_rate = check_location(location)
    tax_amount = discounted_subtotal * tax_rate
    
    grand_total = discounted_subtotal + tax_amount
    
    receipt = f"""
==================================================
Subtotal: {subtotal}/=
Coupon Discount: {coupon_discount}
Tax: {tax_amount}
GRAND TOTAL: {grand_total}


    """

    print(receipt)


def login_system():
    print("Welcome to Ecommerce price calculator. Authenticate to continue")

   
    users = {
        "Cashier" : "password"
    }

    max_attempts = 3
    attempts = 0

    while attempts < max_attempts:
         username = input("Enter your username: ")
         password = input("Enter your password: ")

         if username in users:
             if users[username] == password:
                 print(f"Welcome, {username} \n")

                 
                 subtotal = float(input("Enter subtotal: "))
                 coupon_code = input("Enter coupon code: ")
                 location = input("Enter your country: ").capitalize()
                 compute_grand_total(subtotal, location, coupon_code)
         else:
            attempts += 1         
            print(f"Attempt {attempts} of {max_attempts}")
            print("Maximum login attempts reached. Access denied.")
            
            print("Username not found")


       
             
login_system()








         
        




