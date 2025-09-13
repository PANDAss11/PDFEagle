import sys
import os
import pyfiglet
from pdfrw import PdfReader, PdfWriter, PdfDict, PdfName, PdfString
from colorama import Fore, Style, init

init(autoreset=True)

def banner():
    fig = pyfiglet.figlet_format("PDFEagle", font="slant")
    print(Fore.CYAN + fig + Style.RESET_ALL)
    print(Fore.YELLOW + "Interactive PDF JavaScript injector (OpenAction)" + Style.RESET_ALL)
    print(Fore.MAGENTA + "Made By: panda_big_money\n" + Style.RESET_ALL)
    print(Fore.WHITE + "Paste your JavaScript then end with a line containing only: EOF\n" + Style.RESET_ALL)

def ask_pdf():
    while True:
        path = input(Fore.CYAN + "📄 Enter path to the PDF you want to inject JS into: " + Style.RESET_ALL).strip('"').strip("'")
        if os.path.isfile(path):
            return os.path.abspath(path)
        print(Fore.RED + "✘ File not found. Try again." + Style.RESET_ALL)

def ask_js():
    print(Fore.CYAN + "⌨ Paste your JavaScript below. End with a line containing only: EOF" + Style.RESET_ALL)
    lines = []
    while True:
        line = input()
        if line.strip() == "EOF":
            break
        lines.append(line)
    return "\n".join(lines).strip()

def inject_js(input_pdf, js_code):
    try:
        trailer = PdfReader(input_pdf)
        js_action = PdfDict(S=PdfName.JavaScript, JS=PdfString.encode(js_code))
        trailer.Root.OpenAction = js_action
        out_file = os.path.splitext(input_pdf)[0] + "-injected.pdf"
        PdfWriter(out_file, trailer=trailer).write()
        return True, out_file, None
    except Exception as ex:
        return False, None, ex

def main():
    banner()
    input_pdf = ask_pdf()
    js_code = ask_js()
    print(Fore.YELLOW + "\n⚡ Injecting JavaScript into PDF..." + Style.RESET_ALL)
    ok, out_file, err = inject_js(input_pdf, js_code)
    if ok:
        print(Fore.GREEN + f"\n[ ✔ ] Done — saved to: {out_file}" + Style.RESET_ALL)
        print(Fore.MAGENTA + "" + Style.RESET_ALL)
    else:
        print(Fore.RED + f"\n[✘] Injection failed: {err}" + Style.RESET_ALL)
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n⏹ Interrupted by user. Exiting." + Style.RESET_ALL)
        sys.exit(2)
