import time
import os
import openai
import subprocess
try:
    import readline
except ModuleNotFoundError:
    import pyreadline3 as readline

openai.api_key = os.environ.get("OPENAI_SDK")


def get_completions(text):
    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Complete the following command in a Windows Terminal: {text}",
        max_tokens=20,
        temperature=0.5,
    )

    return [choice.text for choice in completions.choices]

import time

last_call_time = time.time()

def completer(text, state):
    global last_call_time

    current_time = time.time()
    elapsed_time = current_time - last_call_time

    if elapsed_time < 1:
        return None

    last_call_time = current_time

    completions = get_completions(text)
    try:
        #remove any leading whitespace
        completions = [completion.lstrip() for completion in completions]

        return completions[state]
    except IndexError:
        return None

readline.set_completer(completer)
readline.set_completer_delims('\t')
readline.parse_and_bind("tab: complete")

while True:
    command = input("> ")
    if command.strip() == "exit":
        break
    
    if command.strip() == "":
        continue

    try:
        output = subprocess.run(command.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print(output.stdout.decode())
    except Exception as e:
        print(e)