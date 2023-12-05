def get_input(input_phrase):
    print(input_phrase)
    path = input()
    if path == '':
        print('You did not enter anything! Please try again.')
        path = get_input(input_phrase)
    if path == 'c' or path == 'cancel':
        return 'c'
    elif path == 'q' or path == 'quit':
        exit()
    return path

def main():
    answer = get_input('Enter the project name you would like to create, or the name of an existing project:')
    if answer == 'c':
        exit()
    if answer == 'y' or 'yes':
        print('yes')
    return

main()