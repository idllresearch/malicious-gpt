import requests
import re


def validate_html(html_content):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; W3C Validation Bot)",
        "Content-Type": "text/html; charset=utf-8",
    }
    response = requests.post("https://validator.w3.org/nu/?out=json", headers=headers, data=html_content.encode('utf-8'))
    
    # The API returns the results in a structured format, so you can process them as needed
    # Here, we're just printing the response for demonstration
    print(response)
    json_response = response.json()
    judgements = [x['type'] for x in json_response["messages"]]
    error_messages = [x['message'] for x in json_response["messages"] if x['type'] == "error"]
    for error_message in error_messages:
        print(error_message)
    if "error" in judgements:
        return False, error_messages
    else:
        return True, error_messages


if __name__ == '__main__':
    sample_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Test Page</title>
    </head>
    <body>
        <h1>Welcome to the Test Page</h1>
        <p>This is a paragraph.</p>
    </body>
    </html>
    """
    x = re.findall(r"<html>[\s\S]*</html>", sample_html)[0]
    print(x)
    validate_html(sample_html)
