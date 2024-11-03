from configparser import ConfigParser
from huggingface_hub import AsyncInferenceClient

config = ConfigParser()
config.read("config.ini")
hftoken = config['AI']['hftoken']
instructions = config['AI']['system']

# Make sure the client is async
client = AsyncInferenceClient(api_key=hftoken)


async def chat(prompt):
    messages = [
        {"role": "system", "content": instructions},
        {"role": "user", "content": prompt}
    ]

    # Use the async version of the API call
    completion = await client.chat.completions.create(
        model="Qwen/Qwen2.5-72B-Instruct",
        messages=messages,
        temperature=0.5,
        max_tokens=1024,
        top_p=0.7
    )

    return completion.choices[0].message.content
