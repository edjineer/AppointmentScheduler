import requests


def saveSwagger():
    url = "http://localhost:5000/apispec_1.json"
    outputFile = "docs/swagger.json"
    response = requests.get(url)
    if response.status_code == 200:
        with open(outputFile, "w") as file:
            file.write(response.text)
        print(f"API Documentation saved to {outputFile}")
    else:
        print(
            f"Failed to fetch Swagger documentation. Status code: {response.status_code}"
        )


if __name__ == "__main__":
    saveSwagger()
