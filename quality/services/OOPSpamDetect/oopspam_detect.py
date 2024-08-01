import requests


def oopspam_detector(text):
	oopspam_apikey = "skJJ9c9qB65gvZSX6Yw4H7OPUwM79y5iS1xKh0Uj"  # Your API key
	if oopspam_apikey == "":
		print("Please add OOPSpam API key!")
		raise NameError

	url = "https://api.oopspam.com/v1/spamdetection"

	payload = {
		"checkForLength": True,
		"urlFriendly": False,
		"content": text
	}
	headers = {
		"content-type": "application/json",
		"X-Api-Key": oopspam_apikey
	}

	response = requests.post(url, json=payload, headers=headers)

	return response.json()


if __name__ == '__main__':
	result = oopspam_detector("hello")
