
while True:
	string = input("Enter a string: ")
	if len(string) > 16:
		print("String is too long")
		print("Lower by {} characters".format(len(string)-16))