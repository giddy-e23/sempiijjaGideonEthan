def add(number_one, number_two):
	return number_one + number_two


def subtract(number_one, number_two):
	return number_one - number_two


def multiply(number_one, number_two):
	return number_one * number_two


def divide(number_one, number_two):
	if number_two == 0:
		return "Cannot divide by zero"
	return number_one / number_two


def calculator():
	while True:
		print("\n===== Menu-Driven Calculator =====")
		print("1. Add")
		print("2. Subtract")
		print("3. Multiply")
		print("4. Divide")
		print("5. Exit")
		print("===================================")

		choice = input("Enter your choice (1-5): ")

		if choice == "5":
			print("Thank you for using the calculator. Goodbye!")
			break

		if choice not in ["1", "2", "3", "4"]:
			print("Invalid choice. Please try again.")
			continue

		try:
			number_one = float(input("Enter first number: "))
			number_two = float(input("Enter second number: "))
		except ValueError:
			print("Invalid input. Please enter valid numbers.")
			continue

		if choice == "1":
			result = add(number_one, number_two)
			print(f"Result: {number_one} + {number_two} = {result}")
		elif choice == "2":
			result = subtract(number_one, number_two)
			print(f"Result: {number_one} - {number_two} = {result}")
		elif choice == "3":
			result = multiply(number_one, number_two)
			print(f"Result: {number_one} * {number_two} = {result}")
		elif choice == "4":
			result = divide(number_one, number_two)
			print(f"Result: {number_one} / {number_two} = {result}")



calculator()
