# text-generation-webui
import requests

import response_commands


def send_message(lines, context, global_state):
    input_str = response_commands.replace_names("\n".join(lines), global_state)
    global_state.messages.append({"role": "user", "content": input_str})
    total_tokens = len(context.split()) + sum(len(m['content'].split()) for m in global_state.messages)
    while total_tokens > global_state.MAX_TOKENS - global_state.RESPONSE_TOKENS:
        global_state.messages.pop(1)
        total_tokens = len(context.split()) + sum(len(m['content'].split()) for m in global_state.messages)

    # Slip the attitude in
    messages_to_send = global_state.messages[:]
    messages_to_send.append({"role": "system", "content": f"Please generate your next response as if your "
                                                          f"attitude is {global_state.attitude}"})

    content_list = [msg["content"] for msg in messages_to_send]

    prompt = "\n".join(content_list)
    if global_state.args.assistant:
        prompt = prompt + "\n" + global_state.args.assistant + ":"
    else:
        prompt = prompt + "\nassistant: "

    if global_state.args.verbose:
        print(f"prompt: {prompt}")
    request = {
        'prompt': prompt,
        'max_new_tokens': global_state.RESPONSE_TOKENS,
        'do_sample': True,
        'temperature': global_state.args.temperature,
        'top_p': 0.5,
        'typical_p': 1,
        'repetition_penalty': 1.2,
        'top_k': 40,
        'min_length': 0,
        'no_repeat_ngram_size': 0,
        'num_beams': 1,
        'penalty_alpha': 0,
        'length_penalty': 1,
        'early_stopping': False,
        'seed': -1,
        'add_bos_token': True,
        'truncation_length': global_state.MAX_TOKENS,
        'ban_eos_token': False,
        'skip_special_tokens': True,
        'stopping_strings': ["\n"]
    }

    response = requests.post("http://localhost:5000/api/v1/generate", json=request)

    if response.status_code == 200:
        result = response.json()['results'][0]['text']
        global_state.messages.append({"role": "assistant", "content": result})
        print(f"result: {result}")
        return result
    else:
        return "There was an error communicating with the text-generation-webui. {}".format(response)
