import json
from openai import OpenAI
import pandas as pd
import os
from pathlib import Path
import argparse
from utils import get_response, load_file, save_response


def create_user_prompt(relative_path,party_a,party_b,year):
    file_a = os.path.join(relative_path,party_a,f"{year}.txt")
    file_b = os.path.join(relative_path,party_b,f"{year}.txt")

    platform_a = load_file(file_a)
    platform_b = load_file(file_b)

    prompt = f"Party A's Platform:\n\n{platform_a}\n\Party B's Platform:\n\n{platform_b}"
    return prompt
    
def post_process_response(response,party_a,party_b):
    name_map  = {}
    name_map['democrat'] = 'the Democratic Party'
    name_map['republican'] = 'the Republican Party'
    # If the party name precedes a colon in the line of text, replace it with just the party name
    response = response.replace(f"Party A:",f"{party_a.title()}:")
    response = response.replace(f"Party B:",f"{party_b.title()}:")
    response = response.replace(f"Party A",f"{name_map[party_a]}")
    response = response.replace(f"Party B",f"{name_map[party_b]}")
    return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--level', type=str, required=True)
    parser.add_argument('--parties', nargs=2, type=str, required=True)
    parser.add_argument('--year', type=str, required=True)
    args = parser.parse_args()
    parties = args.parties
    year = args.year
    level = args.level

    party_a = parties[0]
    party_b = parties[1]

    prompt_file = "../data/prompts/cross_party_platform.txt"
    system_prompt = load_file(prompt_file)

    rel_path = f"../data/party_platforms/{level}"
    user_prompt = create_user_prompt(rel_path,party_a,party_b,year)
    response = get_response(system_prompt,user_prompt)
    response = post_process_response(response,party_a,party_b)
   
    out_path = f"../results/parties/{level}_{year}_{party_a}_{party_b}.md"
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    save_response(response, out_path)


    



if __name__ == "__main__":
    main()