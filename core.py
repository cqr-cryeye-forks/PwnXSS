from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs, urlencode
from Log import *
from paths import TEMP_PATH_FOR_DATA
from payload_generator import generate_payloads_for_dirs, generate_payloads_for_params
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class Core:
    @staticmethod
    def check_connection(url, session_get):

        Log.info("Checking connection to: " + Y + url)

        try:
            response = session_get.get(url, timeout=15)

        except Exception as e:
            Log.high("Internal error: " + str(e))
            return False

        if response.status_code > 400:
            Log.info("Connection failed " + G + str(response.status_code))
            return False

        else:
            Log.info("Connection established " + G + str(response.status_code))

        return True

    @staticmethod
    def get_method(url, session_get):
        test = None
        query = urlparse(url).query

        if query == "":
            payloads = generate_payloads_for_dirs()

            for payload in payloads:
                Log.info("Checking Payload" + M + " " + payload)
                Log.info("Checking XSS (GET) for" + C + " " + "Directory...")

                if url.endswith("/"):
                    test = url + payload

                elif not url.endswith("/"):
                    test = url + "/" + payload

                try:

                    response = session_get.get(test, verify=False)

                    if payload in response.text or payload in session_get.get(test).text:
                        Log.high("Detected XSS (GET) at " + response.url)

                        with open(TEMP_PATH_FOR_DATA, "a") as file:
                            file.write(json.dumps({"url_xss": response.url, "method": "GET", "data": payload}) + "\n")

                except Exception as e:
                    Log.info(f"Connection Error with GET method for URL: {test} --> {e}")

        if query != "":
            payloads = generate_payloads_for_params()
            for payload in payloads:
                Log.info("Checking Payload" + M + " " + payload)

                query_payload = query.replace(query[query.find("=") + 1:len(query)], payload, 1)
                test = url.replace(query, query_payload, 1)

                query_all = url.replace(query, urlencode({x: payload for x in parse_qs(query)}))
                Log.info("Checking XSS (GET) for" + C + " " + "Params..." + query_all)

                if not url.startswith("mailto:") and not url.startswith("tel:"):

                    try:
                        response = session_get.get(test, verify=False)

                        if payload in response.text or payload in session_get.get(query_all).text:
                            Log.high("Detected XSS (GET) at " + response.url)

                            with open(TEMP_PATH_FOR_DATA, "a") as file:
                                file.write(json.dumps({"url_xss": response.url, "method": "GET",  "data": payload}) + "\n")

                    except Exception as e:
                        Log.info(f"Connection Error with GET method for URL: {test} --> {e}")

    @staticmethod
    def get_method_form(url, session_get):
        response_body = session_get.get(url, verify=False).text

        bsObj = BeautifulSoup(response_body, "html.parser")
        forms = bsObj.find_all("form", method=True)

        for form in forms:
            try:
                action = form["action"]
            except KeyError:
                action = url

            if form["method"].lower().strip() == "get":
                Log.warning("Target have form with GET method: " + C + urljoin(url, action))
                Log.info("Collecting form input key.....")

                payloads = generate_payloads_for_dirs() + generate_payloads_for_params()

                for payload in payloads:
                    keys = {}
                    for key in form.find_all(["input", "textarea"]):
                        try:
                            if key["type"] == "submit":
                                Log.info("Form key name: " + G + key["name"] + N + " value: " + G + "<Submit Confirm>")
                                keys.update({key["name"]: key["name"]})

                            else:
                                Log.info("Form key name: " + G + key["name"] + N + " value: " + G + payload)
                                keys.update({key["name"]: payload})

                        except Exception as e:
                            Log.info("Internal error: " + str(e))
                            try:
                                Log.info("Form key name: " + G + key["name"] + N + " value: " + G + payload)
                                keys.update({key["name"]: payload})
                            except KeyError as e:
                                Log.info("Internal error: " + str(e))

                    Log.info("Sending payload (GET) method...")

                    try:

                        req = session_get.get(urljoin(url, action), params=keys)

                        if payload in req.text:
                            Log.high("Detected XSS (GET) at " + urljoin(url, req.url))
                            Log.high("GET data: " + str(keys))

                            with open(TEMP_PATH_FOR_DATA, "a") as file:
                                file.write(json.dumps({"url_xss": req.url, "method": "GET", "data": str(keys)}) + "\n")

                    except Exception as e:
                        Log.info(f"Connection Error with GET form method for URL: {urljoin(url, action)} --> {e}")

    @staticmethod
    def post_method(url, session_get):
        response_body = session_get.get(url, verify=False).text

        bsObj = BeautifulSoup(response_body, "html.parser")
        forms = bsObj.find_all("form", method=True)

        for form in forms:
            try:
                action = form["action"]
            except KeyError:
                action = url

            if form["method"].lower().strip() == "post":
                Log.warning("Target have form with POST method: " + C + urljoin(url, action))
                Log.info("Collecting form input key.....")

                payloads = generate_payloads_for_params()

                for payload in payloads:

                    keys = {}
                    for key in form.find_all(["input", "textarea"]):
                        try:
                            if key["type"] == "submit":
                                Log.info("Form key name: " + G + key["name"] + N + " value: " + G + "<Submit Confirm>")
                                keys.update({key["name"]: key["name"]})

                            else:
                                Log.info("Form key name: " + G + key["name"] + N + " value: " + G + payload)
                                keys.update({key["name"]: payload})

                        except Exception as e:
                            Log.info("Internal error: " + str(e))

                    Log.info("Sending payload (POST) method...")

                    try:
                        req = session_get.post(urljoin(url, action), data=keys)

                        if payload in req.text:
                            Log.high("Detected XSS (POST) at " + urljoin(url, req.url))
                            Log.high("Post data: " + str(keys))

                            with open(TEMP_PATH_FOR_DATA, "a") as file:
                                file.write(json.dumps({"url_xss": req.url, "method": "POST", "data": str(keys)}) + "\n")

                    except Exception as e:
                        Log.info(f"Connection Error with POST method for URL: {urljoin(url, action)} --> {e}")



