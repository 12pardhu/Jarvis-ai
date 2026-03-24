from app.automation.system_control import execute_command, execute_multi_command
from app.services.assistant_service import process_query
from app.voice.language import detect_language, translate_from_english, translate_to_english

def route_command(command, *, session_id: str | None = None):

    # 🌍 Detect language
    lang = detect_language(command)

    # 🔁 Translate if needed
    if lang != "en":
        command = translate_to_english(command, source_lang=lang)

    command = command.lower().strip()

    print("ROUTER HIT:", command)

    # 🚀 MULTI-STEP SUPPORT
    if " and " in command:
        response = execute_multi_command(command)
    else:
        response = execute_command(command)

    # ⚡ If system handled → return immediately
    if response != "Command not found":
        if lang != "en":
            response = translate_from_english(response, target_lang=lang)
        return response

    # 🌐 WEBSITE NAVIGATION
    if command.startswith("go to "):
        import webbrowser

        site = command.replace("go to ", "").strip()
        url = f"https://{site}.com"

        webbrowser.open(url)
        return f"Opening {site}"
        
    # 🤖 BROWSER AUTOMATION (BROWSER-USE)
    if command.startswith("browse ") or command.startswith("web "):
        from app.automation.browser_agent import run_browser_task
        task = command.replace("browse to ", "").replace("browse ", "").replace("web ", "").strip()
        print(f"Starting browser agent for: {task}")
        response = run_browser_task(task)
        return response

    # 🔍 GOOGLE SEARCH
    if command.startswith("search "):
        import webbrowser

        query = command.replace("search ", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")

        return f"Searching {query}"

    # 🤖 AI FALLBACK
    try:
        response = process_query(command, session_id=session_id)
    except Exception as e:
        print("AI ERROR:", e)
        response = "AI is not responding"

    # 🔁 Translate back
    if lang != "en":
        response = translate_from_english(response, target_lang=lang)

    return response