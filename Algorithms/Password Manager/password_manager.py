from codecs import encode, decode

# Open file and add a new username|password
def add():
    user = input('Account name: ')
    password = input('Password: ')
    
    with open('passwords.txt', 'a') as file:
        file.write(user + '|' + password + '\n')

# Display all username|password combinations in the file
def view():
    with open('passwords.txt', 'r') as file:
        for line in file.readlines():
            # Remove '\n' at the back of each line
            data = line.rstrip()
            user, password = data.split('|')
            print('Username: ' + user +  ',', 'Password: ' + password)

def main():
    while True:
        mode = input('Would you like to add a new password, view existing ones or quit (add/view/quit)?: ').lower()
        if mode == 'add':
            add()
        elif mode == 'view': 
            view() 
        elif mode == 'quit':
            print('Goodbye!')
            break 
        else: 
            print('Invalid input.')
            
main()