from bs4 import BeautifulSoup


def check_payload_in_script_tag(response_text, payload):
    soup = BeautifulSoup(response_text, 'html.parser')
    script_tags = soup.find_all('script')

    # Some payloads contain <script> within, like gb44d><script>alert(1)</script>axm7cgi45yi
    if payload.startswith("<script>"):
        payload = payload.strip("<script>").strip("</script>").strip("")

    # Check if Payload in Response Script Tags
    for script_tag in script_tags:
        if payload in script_tag.get_text():
            return True

    return False
