import requests


def oopspam_detector(text):
	url = "https://api.oopspam.com/v1/spamdetection"

	payload = {
		"checkForLength": True,
		"urlFriendly": False,
		"content": text
	}
	headers = {
		"content-type": "application/json",
		"X-Api-Key": "XXX"  # Your API key
	}

	response = requests.post(url, json=payload, headers=headers)

	return response.json()


if __name__ == '__main__':
	result = oopspam_detector("hello")
	print(result)
