import sys, wikipedia, re, requests

ESC = "\x1B"

color_code = lambda code, bold = False: f"{ESC}[{int(bold)};{code}m"

def log(color: str, content: str, logfile) -> None:
    print(color + content)
    logfile.write(content + "\n")
    logfile.flush()

def main() -> None:
    pageid: int = int(input("[>] Starting ID: "))

    if input(f"[>] Are you sure you want to start with ID-{pageid} (Y/N): ")[0].lower() == "n":
        log(color_code(31), "[!] Exiting...", logs)
        sys.exit(0)

    database = open("./data.txt", "a")
    logs = open("./logs.txt", "a")

    while True:
        log(color_code(34), f"[.] Loading page: ID-{pageid};", logs)
        
        try:        
            page: wikipedia.WikipediaPage = wikipedia.page(pageid=pageid)
            content: str = \
                re.sub(
                    "[ ]{2,}", " ", 
                    re.sub(
                        "[==].*[==]", "", 
                        page.content.split("== See also ==")[0]
                    ).replace("\n", " ")
                )

            log(color_code(32), f"[+] Success;", logs)
            log(color_code(33), f"    Got data of {len(page.content)} Bytes;", logs)

            database.write(content)

        except wikipedia.exceptions.PageError:
            log(color_code(31), f"[-] Page not found: ID-{pageid};", logs)

        except AttributeError:
            log(color_code(31), f"[!] Failed loading page: ID-{pageid};", logs)
        
        except requests.exceptions.ConnectionError:
            log(color_code(31), f"[!] Connection error;", logs)
            pageid -= 1
        
        except KeyboardInterrupt:
            log(color_code(31), "\n\n[!] Keyboard interrupt;\n\n", open("./logs.txt", "a"))
            sys.exit(1)            

        except:
            log(color_code(31), f"[!] Unknown error;", logs)

        pageid += 1

if __name__ == "__main__":
    try: 
        main()
    except KeyboardInterrupt:
        log(color_code(31), "\n\n[!] Keyboard interrupt;\n\n", open("./logs.txt", "a"))
        sys.exit(1)