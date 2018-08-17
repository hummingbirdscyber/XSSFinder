import requests
from bs4 import BeautifulSoup
from termcolor import colored
from time import time


def links_to_page(url):  # Every link in the page.
    set_for_links = set()
    try:
        if(TOR == True): #Using TOR
            if ("https://" not in url and "http://" not in url):
                r = session.get("http://{}".format(url))
                first_url = "http://{}".format(url)
            else:
                first_url = url
                r = session.get(url)
        else:
            if ("https://" not in url and "http://" not in url):
                r = requests.get("http://{}".format(url))
                first_url = "http://{}".format(url)
            else:
                first_url = url
                r = requests.get(url)
    except Exception as e:
        print(e)
        pass
    soup = BeautifulSoup(r.text, "html.parser")
    links = soup.find_all("a")

    if ("https://" in url or "http://" in url):
        url = url.split("//")[1]
        if ("www." in url):
            url = url.split("www.")[1]
        if ("/" in url):
            url = url.split("/")[0]
            # Get the 'domain.com'

    for i in links:
        actual_url = i.get("href")
        url_in_tag = str(i.get("href"))
        if ("https://" in url_in_tag or "http://" in url_in_tag):
            url_in_tag = url_in_tag.split("//")[1]
            if ("www." in url_in_tag):
                url_in_tag = url_in_tag.split("www.")[1]
            if ("/" in url_in_tag):
                url_in_tag = url_in_tag.split("/")[0]
                # Get the 'domain.com'
        if (url in url_in_tag):
            set_for_links.add(actual_url)

        try:
            if (url_in_tag[0] == "."):  # To example: #blog, #homepage
                actual_url = first_url + url_in_tag[1:]  # example.com#homepage
                set_for_links.add(actual_url)
            elif(url_in_tag[0] != "/" and url[-1] != "/"):
                actual_url = first_url + "/" + url_in_tag  # example.com#homepage
                set_for_links.add(actual_url)
            elif(url_in_tag[0] == "/" and url[-1] == "/"):
                actual_url = first_url + url_in_tag[1:]  # example.com#homepage
                set_for_links.add(actual_url)
            else:
                actual_url = first_url + url_in_tag  # example.com#homepage
                set_for_links.add(actual_url)
        except:
            pass

    return set_for_links


def how_many_forms(url):  # Getting information. How many forms in there?
    print("Request is sending..")
    links = links_to_page(url)
    number_of_forms = {}  # Which page has got how many forms?
    for i in links:
        r = requests.get(i)
        soup = BeautifulSoup(r.text, "html.parser")
        form = soup.find_all("form")
        number_of_forms.update({i: len(form)})  # Add into dict pair of forms and pages
    return number_of_forms  # Return the pair of pages and forms


def get_inputs(url):
    '''Shows the all input boxes in the given url.'''
    try:
        if(TOR == True): #Using TOR
            if ("https://" not in url and "http://" not in url):
                r = session.get("http://{}".format(url))
            else:
                r = session.get(url)
        else:
            if ("https://" not in url and "http://" not in url):
                r = requests.get("http://{}".format(url))
            else:
                r = requests.get(url)
    except Exception as e:
        print(e)
        pass

    soup = BeautifulSoup(r.content, "html.parser")
    list_of_inputs = []
    for i in soup.find_all("input"):
        list_of_inputs.append(i)

    return list_of_inputs

def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session

def find_xss(url):
    xss_flag = False
    try:
        if ("https://" not in url and "http://" not in url):
            url = "http://{}".format(url)
    except Exception as e:
        print(e)
        pass

    print(colored("Payloads are being prepared..", "blue"))
    print(colored("Request is sending to site {}".format(url), "blue"))

    inputs = get_inputs(url) #Get input boxes
    if(len(inputs) == 0):
        return -1
    print(colored("Finding input box in the page..", "blue"))
    start = time()
    for pyld in payload:
        try:
            for i in inputs:
                name = str(i.get("name"))
                if(TOR == True): #Using TOR
                    r = session.get(url + "?" + name + "=" + pyld)  # New query for input box.
                else:
                    r = requests.get(url + "?" + name + "=" + pyld) #New query for input box.
                if(pyld in str(r.content,"utf-8")):
                    xss_flag = True
                    print()
                    print(colored("[+]FOUND -> Payload:{}".format(pyld),"red"))
                    end = time()
                    ctime = end - start  # Total Time
                    print(colored("Vulnerable URL -> {}".format(url),"red"))
                    print(colored("Vulnerable Input Box-> {}".format(i),"red"))
                    if(xss_flag):
                        print()
                        print(colored("Time:{} Seconds".format(ctime), "white"))
                        return 1 #We found XSS
                else:
                    print(colored("[-]NOT FOUND -> Payload:{}".format(pyld),"green"))
        except Exception as e:
            print(e)
            pass


def payloads(file):
    with open(file, "r") as f:
        payloads = f.read().splitlines()
    return payloads  # Return the list of payloads.


if __name__ == '__main__':
    intro = '''
        #    #  ####   ####     ###### # #    # #####  ###### #####  
         #  #  #      #         #      # ##   # #    # #      #    # 
          ##    ####   ####     #####  # # #  # #    # #####  #    # 
          ##        #      #    #      # #  # # #    # #      #####  
         #  #  #    # #    #    #      # #   ## #    # #      #   #  
        #    #  ####   ####     #      # #    # #####  ###### #    #

        Author : Fatih Çelik
        E-Mail : fcelik.ft@gmail.com
        ------------------------------------------------------------
    '''
    print(colored(intro, "red"))
    print()

    choices = '''
    1)Quick Scan -> [Scan only given url.]
    2)Intensive Scan -> [Scan all links in the page that doesnt directed to the outside of the page.]
    3)Quick Scan -> [Scan only given url.] {USING TOR}
    4)Intensive Scan -> [Scan all links in the page that doesnt directed to the outside of the page.] {USING TOR}
    5)Get all links in the page that doesnt directed to the outside of the page
    6)How many forms in the url -> [Scan all links in the page that doesnt directed to the outside of the page.]
    7)Get the input box
    '''
    try:
        print(choices)
        choice = input("-->")
        TOR = False
        if (choice == "1"):
            url = input("What is the url -> ")
            file = input("Payloads' file name -> ")
            payload = payloads(file)
            result = find_xss(url)
            if (result == -1):
                print("This page doesnt have any input box to attack.")
            else:
                print(colored(40 * "-", "red"))
        elif (choice == "2"):
            url = input("What is the url -> ")
            file = input("Payloads' file name -> ")
            payload = payloads(file)
            links = links_to_page(url)
            for link in links:
                try:
                    result = find_xss(link)
                    if(result == -1):
                        print("This page doesnt have any input box to attack.")
                        if (test == "0"):
                            exit(0)
                        print(colored(40 * "-", "red"))
                    elif(result == 1):
                        test = input("Do you want to test other links in the page:(1->Continue or 0->Stop) (Default:1)") or "1"
                        if(test == "0"):
                            exit(0)
                        print(colored(40 * "-", "red"))
                    else:
                        print(colored(40 * "-", "red"))
                except Exception as e:
                    print(e)
                    pass
        elif (choice == "3"):
            TOR = True
            session = get_tor_session()
            url = input("What is the url -> ")
            file = input("Payloads' file name -> ")
            print("Current IP -> {}".format(requests.get("http://httpbin.org/ip").json()["origin"]))
            print("Connecting to TOR..")
            print("New IP -> {}".format(session.get("http://httpbin.org/ip").json()["origin"]))
            payload = payloads(file)
            result = find_xss(url)
            if (result == -1):
                print("This page doesnt have any input box to attack.")
            else:
                print(colored(40 * "-", "red"))
        elif (choice == "4"):
            TOR = True
            session = get_tor_session()
            url = input("What is the url -> ")
            file = input("Payloads' file name -> ")
            print(colored("Current IP -> {}".format(requests.get("http://httpbin.org/ip").json()["origin"]),"green"))
            print("Connecting to TOR..")
            print(colored("New IP -> {}".format(session.get("http://httpbin.org/ip").json()["origin"]),"red"))
            payload = payloads(file)
            links = links_to_page(url)
            for link in links:
                try:
                    result = find_xss(link)
                    if (result == -1):
                        print("This page doesnt have any input box to attack.")
                        if (test == "0"):
                            exit(0)
                        print(colored(40 * "-", "red"))
                    elif (result == 1):
                        test = input(
                            "Do you want to test other links in the page:(1->Continue or 0->Stop) (Default:1)") or "1"
                        if (test == "0"):
                            exit(0)
                        print(colored(40 * "-", "red"))
                    else:
                        print(colored(40 * "-", "red"))
                except Exception as e:
                    print(e)
                    pass
        elif (choice == "5"):
            url = input("What is the url -> ")
            links = links_to_page(url)
            for i in links:
                print(i)
        elif (choice == "6"):
            url = input("What is the url -> ")
            forms = how_many_forms(url)
            for i, j in forms.items():
                print(i, "->", j, "form(s)")
        elif (choice == "7"):
            url = input("What is the url -> ")
            inputs = get_inputs(url)
            for i in inputs:
                print(i)
        else:
            print("Wrong parameter!")
            exit(1)
    except KeyboardInterrupt:
        print("Bye Bye..")
