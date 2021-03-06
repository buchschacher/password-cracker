# Library for csv file io
import csv
# For random number generation
# https://cryptography.io/en/latest/random-numbers/
import os
# Library for hashBackend (openssl)
# https://cryptography.io/en/latest/hazmat/backends/
from cryptography.hazmat.backends import openssl
# Lirary for Hash functions like SHA-2 family, SHA-3 family, Blake2, and MD5
# https://cryptography.io/en/latest/hazmat/primitives/
from cryptography.hazmat.primitives import hashes

# Returns a random lowercase character using os.urandom
def get_rand_lowercase():
	# rand_int is geneated the same was as length but with the range 97 - 122
	# this range specifies the ascii values for lowercase letter in decimal
	rand_int = int.from_bytes(os.urandom(1), byteorder="big")
	rand_int = rand_int % (122 - 97 + 1) + 97
	# convert rand_int to a char to get random character
	return chr(rand_int)

# Returns a string with a length in range(min_length, max_length)
# length is randomly generated but within specified range
def get_random_string(min_length, max_length):
	# empty string that will hold random characters and will eventually be returned
	return_str = ""
	# randomly generated byte which is then converted to an int
	length = int.from_bytes(os.urandom(1), byteorder="big")
	# modify length to be within the range(min_length, max_length)
	length = length % (max_length - min_length + 1) + min_length

	for i in range(length):
		# get a random lowercase character
		rand_char = get_rand_lowercase()
		# append the random character to the return string
		return_str = return_str + rand_char
	return return_str

def login():
	fname = select_file()
	f = open(fname, "r")
	username = input("Username: ")
	password = input("Password: ")

	# find if the user name is in the library
	user_found = False
	stored_users = csv_file_to_list_of_lists(fname)
	for user in stored_users:
		if user[0] == username:
			# check input against plaintext
			print("\n" + username + " found in " + fname)
			if fname == "accounts0.txt":
				# output user data
				print("stored password: " + user[1])
				# check input password against plaintext password
				if user[1] == password:
					print("Login SUCCESS")
				else:
					print("Login FAIL")
				return
			# check input against password hash
			elif fname == "accounts1.txt":
				# hash input password
				byte_password = password.encode("ascii")
				digest = hashes.Hash(hashes.SHA256(), backend=openssl.backend)
				digest.update(byte_password)
				hash_password = digest.finalize()
				hash_password = hash_password.hex()
				# output user data
				print("stored hash: " + user[1])
				print("input hash: " + hash_password)
				# check input hash against stored hash
				if user[1] == hash_password:
					print("Login SUCCESS")
				else:
					print("Login FAIL")
				return
			# check input against salted password hash
			elif fname == "accounts2.txt":
				# hash input password + salt
				salted_password = password + user[2]
				byte_salted_password = salted_password.encode("ascii")
				digest = hashes.Hash(hashes.SHA256(), backend=openssl.backend)
				digest.update(byte_salted_password)
				hash_salted_password = digest.finalize()
				hash_salted_password = hash_salted_password.hex()
				# output data
				print("stored salted hash: " + user[1])
				print("stored salt: " + user[2])
				print("input salted hash: " + hash_salted_password)
				# check input salted hash against stored salted hash
				if user[1] == hash_salted_password:
					print("Login SUCCESS")
				else:
					print("Login FAIL")
				return
	print(username + " not found in " + fname)

def add_user():
	fname = select_file()
	f = open(fname, "a+")
	username = ""
	password = ""

	# ask user for a valid username for the account
	while True:
		username = input("Enter a username of up to 8 alphanumeric characters: ")

		user_found = False
		stored_users = csv_file_to_list_of_lists(fname)
		for user in stored_users:
			if user[0] == username:
				user_found = True
				break

		if user_found:
			print("User already exists")
		elif len(username) <= 8 and len(username) and username.isalnum():
			break
		else:
			print("Invalid username")
	# ask user for a valid password for the account
	while True:
		password = input(f"Enter a password of 3 to 8 lowercase letters for {username}: ")
		if len(password) >= 3 and len(password) <= 8 and password.isalpha() and password.islower():
			break
		print("Invalid password")


	if fname == "accounts0.txt":
		print("Creating ading new user to accounts0.txt:")
		print("user: " + username)
		print("password: " + password)
		f.write(username + "," + password + "\n")
	elif fname == "accounts1.txt":
		byte_password = password.encode("ascii")
		digest = hashes.Hash(hashes.SHA256(), backend=openssl.backend)
		digest.update(byte_password)
		hash_password = digest.finalize()
		hash_password = hash_password.hex()
		f.write(username + "," + hash_password + "\n")
		print("Creating ading new user to accounts1.txt:")
		print("user: " + username)
		print("hash: " + hash_password)
	elif fname == "accounts2.txt":
		salt = get_random_string(1, 1)
		salted_password = password + salt
		byte_salted_password = salted_password.encode("ascii")
		digest = hashes.Hash(hashes.SHA256(), backend=openssl.backend)
		digest.update(byte_salted_password)
		hash_salted_password = digest.finalize()
		hash_salted_password = hash_salted_password.hex()
		f.write(username + "," + hash_salted_password + "," + salt + "\n")
		print("Creating ading new user to accounts2.txt:")
		print("user: " + username)
		print("hash: " + hash_salted_password)
		print("salt: " + salt)

def csv_file_to_list_of_lists(file_name):
		csv_file = open(file_name, 'r')
		csv_reader = csv.reader(csv_file, delimiter=",")
		data = []
		for row in csv_reader:
				data.append(row)
		return data
# prompt user with menu to select which file to use
def select_file():
	while True:
		num = input("\nEnter the number of the file you would like to use:\n1) Plaintext password\n2) Hashed password\n3) Hashed password + salt\n\0) Back\n")
		if num == "1":
			return "accounts0.txt"
		elif num == "2":
			return "accounts1.txt"
		elif num == "3":
			return "accounts2.txt"
		else:
			print("Invalid input")

# prompt user to choose an action
def task1menu():
	while True:
		action = input("Select an action to preform:\n1) Login\n2) Add account\n0) Quit\n")
		if action == "1":
			login()
		elif action == "2":
			add_user()
		elif action == "0":
			return
		else:
			print("Invalid input")

if __name__ == "__main__":
	task1menu()
