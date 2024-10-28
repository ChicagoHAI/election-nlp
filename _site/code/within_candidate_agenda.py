import json
from openai import OpenAI
import pandas as pd
import os
from pathlib import Path
import argparse
from utils import get_response, load_file, save_response


def create_user_prompt(relative_path,candidate,year_a,year_b):
    file_a = os.path.join(relative_path,candidate,f"{year_a}.txt")
    file_b = os.path.join(relative_path,candidate,f"{year_b}.txt")
    agenda_a = load_file(file_a)
    agenda_b = load_file(file_b)
    prompt = f"Candidate A's {year_a} Agenda:\n\n{agenda_a}\n\nCandidate A's {year_b} Agenda:\n\n{agenda_b}"
    return prompt
    
def post_process_response(response,candidate):
    response = response.replace("Candidate A",candidate.title())
    return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--office', type=str, required=True)
    parser.add_argument('--candidate', type=str, required=True)
    parser.add_argument('--years', nargs=2,type=str, required=True)
    args = parser.parse_args()
    office = args.office
    candidate = args.candidate
    year_a, year_b = args.years
    
    prompt_file = "../data/prompts/within_candidate_agenda.txt"
    system_prompt = load_file(prompt_file)

    rel_path = f"../data/candidate_positions/{office}"
    user_prompt = create_user_prompt(rel_path,candidate,year_a,year_b)
    response = get_response(system_prompt,user_prompt)
    response = post_process_response(response,candidate)
   
    out_path = f"../results/candidates/{office}_{candidate}_{year_a}_{year_b}.md"
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    save_response(response, out_path)

    print(response)




    



if __name__ == "__main__":
    main()