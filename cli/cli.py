import requests

API_URL = "http://localhost:8000"


def main():
    while True:
        command = input("Enter your command (or type 'exit' to quit): ")
        if command.lower() == "exit":
            break

        response = requests.post(
            f"{API_URL}/process_command", json={"command": command}
        )
        print(response.json())


if __name__ == "__main__":
    main()
