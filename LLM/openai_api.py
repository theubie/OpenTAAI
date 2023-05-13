# openai_api.py
import response_commands
import openai
import logging


def send_message(lines, context, global_state):
    input_str = response_commands.replace_names("\n".join(lines), global_state)
    global_state.messages.append({"role": "user", "content": input_str})
    total_tokens = len(context.split()) + sum(len(m['content'].split()) for m in global_state.messages)

    while total_tokens > global_state.MAX_TOKENS - global_state.RESPONSE_TOKENS:
        global_state.messages.pop(1)
        total_tokens = len(context.split()) + sum(len(m['content'].split()) for m in global_state.messages)

    # Slip the attitude in
    messages_to_send = global_state.messages[:]
    r_string = global_state.relevant_string()
    messages_to_send.insert(1, {"role": "system", "content": r_string})
    messages_to_send.append({"role": "system", "content": f"Please generate your next response as if your "
                                                          f"attitude is {global_state.attitude}"})

    # OpenAI api key
    openai.api_key = global_state.api_key.strip()

    try:

        if global_state.verbose:
            print(f"Input text: \n{messages_to_send}")
        response = openai.ChatCompletion.create(
            model=global_state.args.model,
            messages=messages_to_send,
            temperature=global_state.args.temperature
        )
        logging.info(f"Request: {input_str}\nResponse: {response}\n")
    except openai.OpenAIError as e:
        logging.error(f"Request: {input_str}\nError: {e}\n")
        print(f"Error: {e}")
        return "Sorry, an error occurred while processing your request. Please try again later."
    else:
        new_response = response_commands.process_response(response['choices'][0]['message']['content'], global_state)
        global_state.messages.append({"role": "assistant", "content": new_response})
        return new_response
