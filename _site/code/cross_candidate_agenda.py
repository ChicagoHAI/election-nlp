import json
from openai import OpenAI
import pandas as pd
import os
from pathlib import Path
import argparse
from utils import get_response, load_file, save_response


def create_user_prompt(relative_path,cand_a,cand_b,year):
    file_a = os.path.join(relative_path,cand_a,f"{year}.txt")
    file_b = os.path.join(relative_path,cand_b,f"{year}.txt")

    agenda_a = load_file(file_a)
    agenda_b = load_file(file_b)

    prompt = f"Candidate A's Agenda:\n\n{agenda_a}\n\nCandidate B's Agenda:\n\n{agenda_b}"
    return prompt
    
def post_process_response(response,cand_a,cand_b):
    response = response.replace("Candidate A",cand_a.title())
    response = response.replace("Candidate B",cand_b.title())
    return response


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--office', type=str, required=True)
    parser.add_argument('--candidates', nargs=2, type=str, required=True)
    parser.add_argument('--year', type=str, required=True)
    args = parser.parse_args()
    candidates = args.candidates
    year = args.year
    office = args.office

    cand_a = candidates[0]
    cand_b = candidates[1]

    prompt_file = "../data/prompts/cross_candidate_agenda.txt"
    system_prompt = load_file(prompt_file)

    rel_path = f"../data/candidate_positions/{office}"
    user_prompt = create_user_prompt(rel_path,cand_a,cand_b,year)
    response = get_response(system_prompt,user_prompt)
    response = post_process_response(response,cand_a,cand_b)
   
    out_path = f"../results/candidates/{office}_{year}_{cand_a}_{cand_b}.md"
    Path(out_path).parent.mkdir(parents=True, exist_ok=True)
    save_response(response, out_path)


    



if __name__ == "__main__":
    main()