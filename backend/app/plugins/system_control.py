import webbrowser
import os

def run(command: str):

    command = command.lower()

    if "open youtube" in command:
        webbrowser.open("https://youtube.com")
        return "Opening YouTube"

    if "open google" in command:
        webbrowser.open("https://google.com")
        return "Opening Google"

    if "open chrome" in command:
        os.system("open -a 'Google Chrome'")
        return "Opening Chrome"

    if "open vscode" in command:
        os.system("open -a 'Visual Studio Code'")
        return "Opening VS Code"

    return None