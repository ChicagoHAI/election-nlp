#written by chatgpt
#should get all trump speech urls to scrape from

from bs4 import BeautifulSoup
import requests

#url = "https://www.rev.com/blog/transcript-category/donald-trump-transcripts"  # Replace with the actual URL

# Step 2: Fetch the webpage
#response = requests.get(url)

#req = urllib.request.Request('https://v2.gcchmc.org/book-appointment/')

# Check if the request was successful (status code 200)
#if response.status_code == 200:
    # Step 3: Parse the HTML content with BeautifulSoup
with open("listofspeeches.html", 'r') as file:
    
    soup = BeautifulSoup(file, 'html.parser')
    # Find the specific <div> with class 'fl-post-grid' and itemscope attribute
    #fl_post_grid_div = soup.find('div', class_='fl-post-grid', attrs={"itemscope": "itemscope"})

    # Find all <a> tags with an href attribute within that specific division
    #if fl_post_grid_div:
    print('gothere')
    a_tags = soup.find_all('a', href=True)

        # Extract and print the href (URL) from each <a> tag
    for a_tag in a_tags:
        with open('harrisurls.txt', 'a') as file:
            print(a_tag['href'], file = file)


    
#else:
#    print(f'Failed to retrieve the webpage. Status code: {response.status_code}')




