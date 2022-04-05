import requests
from requests.api import get

mobileNumber = input("Input mobile number: ")
pinNumber = input("Input 4 digit pin number: ")

validAccount = f"http://127.0.0.1:8000/api/accounts/{mobileNumber}-{pinNumber}"
accountGetResponse = requests.get(validAccount)

print(accountGetResponse.status_code)

if accountGetResponse.status_code == 200:
    print("Welcome")
    logout = True
    withdrawDone = True

    while logout and withdrawDone:
        print("1. View Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Logout")

        select = int(input("Select number: "))

        if select == 1:
            accountEndpoint = f"http://127.0.0.1:8000/api/accounts/{mobileNumber}-{pinNumber}"
            getResponse = requests.get(accountEndpoint)
            account = getResponse.json()
            print(f"Balance: {account['total_credits_earned']}")
        elif select == 2:
            depositEndpoint = "http://127.0.0.1:8000/api/deposit"
            bottleQuantity = int(input("Enter number of bottles: "))
            creditsEarned = bottleQuantity * 0.25

            data = {
                "mobile_number": f"+{mobileNumber}",
                "credits_earned": creditsEarned,
                "number_of_bottles": bottleQuantity
            }
            getResponse = requests.post(depositEndpoint, json=data)
            response = getResponse.json()
            print(f"You earned {response['credits_earned']} credits")
        elif select == 3:
            withdrawEndpoint = "http://127.0.0.1:8000/api/withdraw/"

            amount = int(input("Enter amount to withdraw: "))

            data = {
                "mobile_number": f"+{mobileNumber}",
                "pin_number": pinNumber,
                "amount": amount
            }
            get_response = requests.post(withdrawEndpoint, json=data)
            if get_response.status_code == 201:
                withdraw = get_response.json()
                print(f"You withdrawn {withdraw['amount']} credits")
                withdrawDone = False
                print("Thank you...")
            elif get_response.status_code == 400:
                # error = get_response.json()
                # print(error['Failed'])
                print("Insufficient balance")
        elif select == 4:
            logout = False
            print("Thank you...")
        else:
            print("Wrong Input")
else:
    print("Account not found")
