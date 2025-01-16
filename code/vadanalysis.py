# Split each line into words (either from tokenization or just whitespace)
import pandas as pd
import os

def get_kamala(loc, filename, filetype):
    #chatgpt edited code - check over

    # Read the input CSV file
    file_path = os.path.join(loc, f"{filename}{filetype}")
    file = pd.read_csv(file_path)
    
    # Use a list to collect rows for "Kamala Harris" or "Kamala"
    filtered_rows = []
    for _, row in file.iterrows():
        if row["Speaker"] in ["Kamala Harris", "Kamala"]:
            filtered_rows.append([row["Speaker"], row["Text"]])
    
    # Convert the list to a DataFrame once at the end
    arr = pd.DataFrame(filtered_rows, columns=["Speaker", "line"])
    
    # Ensure the output directory exists
    output_dir = os.path.join(loc, "csvsplit")
    os.makedirs(output_dir, exist_ok=True)
    
    # Save the filtered data as a new CSV file
    output_path = os.path.join(output_dir, f"{filename}_SOLO.csv")
    arr.to_csv(output_path, index=False)
    print(f"Filtered CSV saved to: {output_path}")

def load_valfile(tsv_path):
    """
    Load the valence-arousal-dominance values from a TSV file into a DataFrame.
    Assumes the TSV file has columns: 'word', 'valence', 'arousal', 'dominance'.
    """
    valfile = pd.read_csv(tsv_path, sep='\t')
    #print(valfile.columns)
    #print(valfile.head)
    valfile = valfile.set_index('word')  # Set 'word' as the index for fast lookup
    #print(valfile.head)
    return valfile


def value_in_dict(valfile, word):
    """
    Retrieve valence, arousal, and dominance scores for a word from the loaded TSV DataFrame.
    """
    word = word.strip().lower()
    #print(word)
    #print(valfile.index)
    if word in valfile.index:
        ans = valfile.loc[word].to_dict()
        #print(ans)
    else:
        ans = None  # Return None if the word is not found
    
    return ans



def split_into_words(line):
    return line.split()

# Convert all to lowercase, remove punctuation.
def clean_up(line):
    # Remove punctuation using str.translate and str.maketrans
    #translator = str.maketrans('', '', string.punctuation)
    
    # Split the line into words, clean each word, and return as a list
    words = line.split(' ')
    cleaned_words = []
    for word in words: 
        cleaned_words.append(word.strip().lower())
    return cleaned_words

# For each word, look up if it’s in the sentiment dictionary


# Calculate the average sentiment/emotion score per line (averaged over all words that have an associated score)
def calculate_scores(valfile, words):
    """
    Calculate average valence, arousal, and dominance for a list of words.
    """
    scores = []
    for word in words:
        if value_in_dict(valfile, word) is not None:
            scores.append(value_in_dict(valfile, word))
    #scores = [value_in_dict(valfile, word) for word in words if value_in_dict(valfile, word) is not None]
    if not scores:
        return (None, None, None)
    
    df = pd.DataFrame(scores)
    return df['valence'].mean(), df['arousal'].mean(), df['dominance'].mean()

def avg_line(valfile, line):
    """
    Calculate average sentiment/emotion scores for a single line.
    """
    words = clean_up(line)
    return calculate_scores(valfile, words)

def avg_speech(valfile, speech):
    """
    Calculate average sentiment/emotion scores for an entire speech.
    """
    all_words = []
    for line in speech:
        words = split_into_words(clean_up(line))
        all_words.extend(words)
    return calculate_scores(valfile, all_words)

def process_csv(valfile_path, input_csv, output_csv):
    """
    Process a CSV file to compute line-level and speech-level scores.
    valfile_path: Path to the TSV file with valence, arousal, and dominance scores.
    """
    # Load the valfile as a DataFrame
    valfile = load_valfile(valfile_path)
    # Read the input CSV file
    data = pd.read_csv(input_csv)
    # Ensure required columns exist
    assert 'line' in data.columns, "The input CSV must have a 'line' column."

    # Process line-level scores
    #print(data.columns)
    data['v'], data['a'], data['d'] = 0, 0, 0
    for index, row in data.iterrows():
        #print(avg_line(valfile, row['line']))
        data['v'][index], data['a'][index], data['d'][index] = avg_line(valfile, row['line'])
    
    # Save the output
    data.to_csv(output_csv, index=False)
    print(f"Processed CSV saved to: {output_csv}")

def process_csv(valfile_path, input_csv, output_csv):
    """
    Process a CSV file to compute line-level and speech-level scores.
    valfile_path: Path to the TSV file with valence, arousal, and dominance scores.
    """
    # Load the valfile as a DataFrame
    valfile = load_valfile(valfile_path)
    # Read the input CSV file
    data = pd.read_csv(input_csv)
    # Ensure required columns exist
    assert 'line' in data.columns, "The input CSV must have a 'line' column."

    # Process line-level scores
    #print(data.columns)
    data['v'], data['a'], data['d'] = 0, 0, 0
    for index, row in data.iterrows():
        #print(avg_line(valfile, row['line']))
        data['v'][index], data['a'][index], data['d'][index] = avg_line(valfile, row['line'])
    
    # Save the output
    data.to_csv(output_csv, index=False)
    print(f"Processed CSV saved to: {output_csv}")

# Process speech-level scores (assumes lines are grouped into speeches)
def whole_speech(valfile_path, input_csv, output_csv):
    # Load the valfile as a DataFrame
    valfile = load_valfile(valfile_path)
    # Read the input CSV file
    data = pd.read_csv(input_csv)
    assert 'line' in data.columns, "The input CSV must have a 'line' column."

    new = []
    # Process line-level scores
    #print(data.columns)
    for index, row in data.iterrows():
        for word in row['line'].split():
            k = value_in_dict(valfile, word)
            if k:
                new.append([word, k])
    
    final = pd.DataFrame(new, columns = ['word', 'vad'])
    # Save the output
    final.to_csv(output_csv, index=False)
    print(f"Processed CSV saved to: {output_csv}")            


# Do each speech individually
#lets look at one speech: 
# 


files = [
    "Apr 9, 2024-VPHarris",
    "Aug 12, 2024-Harrisand",
    "Aug 12, 2024-KamalaHarris",
    "Aug 19, 2024-Bidenand",
    "Aug 19, 2024-KamalaHarris",
    "Aug 20, 2024-HarrisEnergizes",
    "Aug 23, 2024-KamalaHarris",
    "Aug 29, 2024-Harrisand",
    "Aug 6, 2024-KamalaHarris",
    "Aug 7, 2024-Harrisand",
    "Aug 8, 2024-Harrisand",
    "Dec 21, 2023-VicePresident",
    "Feb 18, 2024-VicePresident",
    "Feb 26, 2024-PresidentBiden",
    "Jul 22, 2024-BidenDrops",
    "Jul 23, 2024-HarrisSpeaks",
    "Jul 26, 2023-Proclamationto",
    "Jun 13, 2023-VicePresident",
    "Jun 26, 2023-VicePresident",
    "Jun 27, 2023-BidenDiscusses",
    "Jun 7, 2023-VicePresident",
    "Mar 26, 2024-KamalaHarris",
    "May 2, 2023-Bidenand",
    "May 30, 2024-Bidenand",
    "Oct 1, 2024-HarrisRally",
    "Oct 13, 2024-HarrisSpeaks",
    "Oct 17, 2024-HarrisSpeaks",
    "Oct 17, 2024-KamalaHarris",
    "Oct 21, 2024-HarrisRally",
    "Oct 21, 2024-Harrisand",
    "Oct 21, 2024-ObamaCampaigns",
    "Oct 22, 2024-HarrisSpeaks",
    "Oct 22, 2024-UsherCampaign",
    "Oct 24, 2024-HarrisEvent",
    "Oct 24, 2024-Obamaand",
    "Oct 7, 2024-HarrisRally",
    "Oct 8, 2024-KamalaHarris:",
    "Sep 1, 2024-KamalaHarris",
    "Sep 10, 2024-Trumpvs",
    "Sep 11, 2024-Harrisvs",
    "Sep 15, 2024-HarrisRally",
    "Sep 18, 2024-KamalaHarris",
    "Sep 26, 2024-HarrisSpeech",
    "Sep 3, 2024-Harrisand",
    "Sep 30, 2024-HarrisInterview",
    "Sep 30, 2024-HarrisSpeaks"
]

valfile = "NRC-VAD-Lexicon/NRC-VAD-Lexicon.txt"
loc = 'harris/harrisspeeches/csv/'
type = '.csv'
"""for filename in files:
    #get_kamala(loc, filename, type)

    process_csv(
        "NRC-VAD-Lexicon/NRC-VAD-Lexicon.tsv",
        f"{loc}csvsplit/{filename}_SOLO.csv",
        f"harris/values/{filename}_VAD.csv"
    )"""
whole_speech(
        "NRC-VAD-Lexicon/NRC-VAD-Lexicon.tsv",
        "harris/harrisspeeches/csv/Sep 30, 2024-HarrisSpeaks.csv",
        "harris/harrisspeeches/totalscore.csv"
    )

# analyses (at speech level) - trajectory throughout the campaign
# analyses (at line level) - trajectory in affect throughout a speech

