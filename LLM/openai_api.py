# openai_api.py
import response_commands
import openai
import logging
import time

RETRY_DELAY_SECONDS = 5
MAX_RETRIES = 3


def send_request(input_str, messages_to_send, global_state):
    for retry in range(MAX_RETRIES):
        try:
            response = openai.ChatCompletion.create(
                model=global_state.args.model,
                messages=messages_to_send,
                temperature=global_state.args.temperature
            )
            # If no exception is raised, break out of the retry loop
            break
        except openai.OpenAIError as e:
            # Check if the exception message indicates that the model is overloaded
            if "model is currently overloaded" in str(e):
                if retry < MAX_RETRIES - 1:  # Don't sleep on last retry
                    time.sleep(RETRY_DELAY_SECONDS)
                    continue
            # If the exception is not due to an overloaded model, or we've hit the maximum number of retries,
            # re-raise the exception
            raise
    else:
        # We only get here if we've exhausted our retries
        logging.error(f"Request: {input_str}\nError: Model overloaded\n")
        print(f"Error: Model overloaded")
        return "Sorry, the model is currently overloaded. Please try again later."

    # Process the response
    new_response = response_commands.process_response(response['choices'][0]['message']['content'], global_state)
    global_state.messages.append({"role": "assistant", "content": new_response})
    return new_response


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

    if global_state.verbose:
        print(f"Input text: \n{messages_to_send}")

    return send_request(input_str, messages_to_send, global_state)
