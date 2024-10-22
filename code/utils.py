from openai import OpenAI




def load_file(prompt_file):
    with open(prompt_file, 'r') as f:
        prompt = f.read()
    return prompt


def get_response(system_prompt, user_prompt):
    client = OpenAI()
    completion = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        temperature=0,
        top_p = 0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
    )
    return completion.choices[0].message.content

def save_response(response, output_file):
    with open(output_file, 'w') as f:
        f.write(response)
    