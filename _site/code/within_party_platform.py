import json
from openai import OpenAI
import pandas as pd
import os
from pathlib import Path
import argparse
from utils import get_response, load_file, save_response


def create_user_prompt(relative_path,party,years):
    filenames = [os.path.join(relative_path,party,f"{year}.txt") for year in years]
    platforms = [load_file(f) for f in filenames]
    prompt = ""
    for year, platform in zip(years, platforms):
        prompt += f"Party A's {year} Platform:\n\n{platform}\n"
    return prompt.strip('\n')
    
def post_process_response(response,party):
    name_map  = {}
    name_map['democrat'] = 'the Democratic Party'
    name_map['republican'] = 'the Republican Party'
    # If the party name precedes a colon in the line of text, replace it with just the party name
    response = response.replace(f"Party A:",f"{party.title()}:")
    response = response.replace(f"Party A",f"{name_map[party]}")
    return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--level', type=str, required=True)
    parser.add_argument('--party', type=str, required=True)
    parser.add_argument('--years', nargs='+',type=str, required=True)
    args = parser.parse_args()
    level = args.level
    party = args.party
    years = args.years
    
    prompt_file = "../data/prompts/within_party_platform.txt"
    system_prompt = load_file(prompt_file)
    print(system_prompt)

    rel_path = f"../data/party_platforms/{level}"
    user_prompt = create_user_prompt(rel_path,party,years)
    response = get_response(system_prompt,user_prompt)
    response = post_process_response(response,party)
    
    year_str = "_".join(years)
    out_path = f"../results/parties/{level}_{party}_{year_str}.md"
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    save_response(response, out_path)

    print(response)








    



if __name__ == "__main__":
    main()