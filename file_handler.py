file = open("test.txt", "w")

file.write("Hello Gaurav\n")
file.write("I am learning Python\n")
file.write("I am building Enterprise AI applications\n")

file.close()

 

with open("test.txt", "r") as file:

    content = file.read()

print(content)