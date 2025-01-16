from bs4 import BeautifulSoup
import requests

urls = [ "https://www.rev.com/blog/transcripts/trump-rally-in-latrobe-pennsylvania", 
"https://www.rev.com/blog/transcripts/harris-and-trump-speak-at-memorial-dinner", 
"https://www.rev.com/blog/transcripts/trump-rally-in-detroit-michigan", 
"https://www.rev.com/blog/transcripts/trump-town-hall-on-univision", 
"https://www.rev.com/blog/transcripts/trump-town-hall-in-pennsylvania", 
"https://www.rev.com/blog/transcripts/trump-rally-in-atlanta-georgia", 
"https://www.rev.com/blog/transcripts/trump-speaks-in-chicago", 
"https://www.rev.com/blog/transcripts/trump-rally-at-coachella", 
"https://www.rev.com/blog/transcripts/trump-rally-in-reno-nevada", 
"https://www.rev.com/blog/transcripts/trump-speaks-at-event-in-detroit-michigan", 
"https://www.rev.com/blog/transcripts/trump-attends-hispanic-roundtable", 
"https://www.rev.com/blog/transcripts/trump-rally-in-reading-pennsylvania", 
"https://www.rev.com/blog/transcripts/trump-rally-in-scranton-pennsylvania", 
"https://www.rev.com/blog/transcripts/trump-speaks-at-october-7th-event", 
"https://www.rev.com/blog/transcripts/trump-rally-in-juneau-wisconsin", 
"https://www.rev.com/blog/transcripts/trump-town-hall-in-north-carolina", 
"https://www.rev.com/blog/transcripts/trump-and-musk-speak-at-butler-rally", 
"https://www.rev.com/blog/transcripts/trump-rally-before-vp-debate", 
"https://www.rev.com/blog/transcripts/trump-speaks-in-erie-pa", 
"https://www.rev.com/blog/transcripts/trump-holds-event-in-wisconsin", 
"https://www.rev.com/blog/transcripts/trump-holds-press-conference-in-nyc", 
"https://www.rev.com/blog/transcripts/trump-rally-in-walker-michigan", 
"https://www.rev.com/blog/transcripts/trump-makes-campaign-stop-in-north-carolina", 
"https://www.rev.com/blog/transcripts/trump-rally-in-georgia", 
"https://www.rev.com/blog/transcripts/trump-rally-in-north-carolina-2", 
"https://www.rev.com/blog/transcripts/trump-speaks-to-jewish-group-in-washington", 
"https://www.rev.com/blog/transcripts/donald-trump-rally-on-9-18-24-in-uniondale", 
"https://www.rev.com/blog/transcripts/trump-rally-in-las-vegas", 
"https://www.rev.com/blog/transcripts/donald-trump-takes-questions-from-reporters", 
"https://www.rev.com/blog/transcripts/donald-trump-rally-in-arizona", 
"https://www.rev.com/blog/transcripts/trump-speaks-at-fraternal-order-of-police-meeting", 
"https://www.rev.com/blog/transcripts/trump-rally-in-wisconsin", 
"https://www.rev.com/blog/transcripts/trump-speaks-after-appeal-arguement", 
"https://www.rev.com/blog/transcripts/trump-speaks-at-national-guard-conference-in-detroit", 
"https://www.rev.com/blog/transcripts/trump-speaks-at-turning-point-rally-in-glendale-arizona", 
"https://www.rev.com/blog/transcripts/donald-trump-speaks-at-the-southern-border", 
"https://www.rev.com/blog/transcripts/vance-and-trump-rally-in-asheboro-nc", 
"https://www.rev.com/blog/transcripts/trump-holds-news-conference-at-mar-a-lago", 
"https://www.rev.com/blog/transcripts/trump-and-vance-speak-at-atlanta-rally", 
"https://www.rev.com/blog/transcripts/trump-addresses-national-association-of-black-journalists", 
"https://www.rev.com/blog/transcripts/trump-rally-in-grand-rapids-michigan", 
"https://www.rev.com/blog/transcripts/trump-rally-in-florida-on-7-09-24", 
]

# Step 1: Define the URL of the webpage you want to load
for i, page in enumerate(urls):
    # Step 2: Set a User-Agent header to mimic a browser
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
    }

    # Step 3: Fetch the webpage with headers
    response = requests.get(page, headers=headers)

	# Check if the request was successful (status code 200)
    if response.status_code == 200:
		# Step 3: Parse the HTML content with BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        output = []

        #fl-main-content > div.fl-builder-content.fl-builder-content-8994.fl-builder-global-templates-locked > div > div > div > div.fl-col-group.fl-node-5de91b000a942 > div > div > div.fl-module.fl-module-heading.fl-node-5de91b000a7b8 > div > h1
        section = soup.find("div", {"data-node": "5de91b000a942"})
        date = section.find('p').text.strip()
        title = section.find('h1', class_='fl-heading').find('span').text.strip()
        # Start from the specific container with id="transcription"
        transcription_section = soup.find('div', id='transcription')

        if transcription_section:
            # Find all <p> tags within the transcription section
            speaker_tags = transcription_section.find_all('p')

            for speaker_tag in speaker_tags:
                
                # Extract the speaker text
                speaker_text = speaker_tag.get_text(strip=True)

                # Get the next sibling <div> which contains the associated text
                text_div = speaker_tag.find_next_sibling('div')
                if text_div:
                    # Collect all text paragraphs inside this <div>
                    text_content = [p.get_text(strip=True) for p in text_div.find_all('p')]
                    
                    # Append speaker and all associated text as a tuple
                    output.append((speaker_text, text_content))

        # Print or write extracted speakers and texts
        firstfew = title.split()
        firstfew = "".join(firstfew[:2])
        with open(f"trumpspeeches/{date}-{firstfew}.txt", "a") as file:
            for speaker, texts in output:
                print(f"Speaker: {speaker}", file=file)
                for text in texts:
                    print(f"Text: {text}", file=file)
                print("------", file=file)
        print(i)

    else:
        print(f'Failed to retrieve the webpage. Status code: {response.status_code}')



