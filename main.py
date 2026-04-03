from core.sessions import Session

def main():
    question = input("Enter deliberation question: ")
    session = Session()
    session.run(question)

if __name__ == "__main__":
    main()
