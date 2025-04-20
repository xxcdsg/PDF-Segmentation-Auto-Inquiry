def build_messages(user_input):
    return [{
            "role": "user",
            "content": user_input
        }]

def extend_messages(user_input,output,messages,other = "assistant"):
    messages.append({"role": other, "content": output})
    messages.append({"role": "user", "content": user_input})
    return messages