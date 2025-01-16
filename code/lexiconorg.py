import re
import os
import csv
# Text input such that: 
"""text = Speaker: Speaker 1 (00:07): \n
    Text: Ladies and gentlemen,\n
    ------\n
    Speaker: Rachel Scott (01:10):\n
    Text: NABJ. Mic’s on. There we go. \n
    Text: (01:55)As journalists, we use opportunities \n
    ------\n
    Speaker: Donald Trump (02:32):\n
    Text: Hello.\n
    ------\n
    Speaker: Rachel Scott (02:47):\n
    Text: Hi, Mr. Trump, Rachel Scott, ABC. Thank you.\n
    ------\n
    Speaker: Donald Trump (02:49):\n
    Text: How are you? How are you?\n
    ------\n
    Speaker: Rachel Scott (02:55):\n
    Text: Mr. President, we so appreciate \n
    ------\n
    Speaker: Donald Trump (03:49):\
    Text: Well, first of all, I don’t think I’ve \n
    Text: (04:54)And let me go a step further.\n
    ------\n
    Speaker: Rachel Scott (05:23):\n
    Text: Mr. President-\n
    ------"""
#becomes 
"""Speaker 1, 00:07, "Ladies and gentlemen,"
    Rachel Scott, 01:10, "NABJ. Mic’s on. There we go."
    Rachel Scott, 01:55, "As journalists, we use opportunities"
    Donald Trump, 02:32, "Hello."
    Rachel Scott, 02:47, "Hi, Mr. Trump, Rachel Scott, ABC. Thank you."
    Donald Trump, 02:49, "How are you? How are you?"
    Rachel Scott, 02:55, "Mr. President, we so appreciate"
    Donald Trump, 03:49, "Well, first of all, I don’t think I’ve"
    Donald Trump, 04:54, "And let me go a step further."
    Rachel Scott, 5:23, "Mr. President-"

"""


# Regular expression to match each section
def format_transcript(text):
    # Regular expression to capture speaker, timestamp, and text lines
    pattern = r"Speaker: ([\w\s]+) \((\d{2}:\d{2})\):\s*((?:Text:.*?(?=(Text:|------|\nSpeaker:|\Z)))+)"

    # Extract matches
    matches = re.findall(pattern, text, re.DOTALL)
    output = []

    for speaker, _, dialogue, _ in matches:
        # Split the dialogue into individual Text lines
        text_lines = dialogue.splitlines()
        
        for line in text_lines:
            if line.startswith("Text:"):
                # Extract the timestamp from the line
                timestamp_match = re.search(r'\((\d{2}:\d{2}(?::\d{2})?)\)', line)
                if timestamp_match:
                    timestamp = timestamp_match.group(1)  # Get the timestamp

                    # Clean up the line, remove the inline timestamp and excess whitespace
                    cleaned_line = re.sub(r"Text:\s*|\(.*?\)", "", line).strip()
                    output.append([speaker.strip(), timestamp.strip(), cleaned_line])

    return output
    



for i, filename in enumerate(os.listdir("harris/harrisspeeches/txt")):

    # Detect encoding

    with open(os.path.join("harris/harrisspeeches/txt", filename), 'r') as file:
        text = file.read()

    
    

    namefile = filename[:-4]
    # Write to CSV
    with open(f'harris/harrisspeeches/csv/{namefile}.csv', 'w', newline='') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(['Speaker', 'Timestamp', 'Text'])  # Header
        writer.writerows(format_transcript(text))

    print(f"file {namefile} created")
