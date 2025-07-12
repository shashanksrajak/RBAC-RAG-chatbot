from agents.graph import chatbot_graph


def chatbot_service(access_level: str, question: str):
    initial_state = {
        "access_level": access_level,
        "question": question
    }
    chatbot_agent = chatbot_graph()
    output = chatbot_agent.invoke(initial_state)

    print("User Question: ", question)
    print("Access Level: ", access_level)

    print(output)

    if output:
        return output["answer"]
