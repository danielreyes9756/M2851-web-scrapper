from src.logic.scrapper import scrape_hot_questions


def main():
    while True:
        print("Choose an option:")
        print("1. Extract popular questions from Stack Exchange")
        print("2. Exit")

        choice = input("Choose a number based on the previous list: ")

        if choice == '1':
            print("Extracting popular questions...")
            scrape_hot_questions()
        elif choice == '2':
            print("Exiting...")
            break
        else:
            print("No valid option. Try again!")


if __name__ == '__main__':
    main()
