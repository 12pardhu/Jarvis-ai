memory = []

def store_memory(user, response):
    memory.append({
        "user": user,
        "assistant": response
    })

def get_context():
    context = ""
    for m in memory[-5:]:  # last 5 interactions
        context += f"User: {m['user']}\nAssistant: {m['assistant']}\n"
    return context