from bs4 import BeautifulSoup
import requests
import os
from dotenv import load_dotenv
import openai

## Loading Env Variables
load_dotenv()
GPT_SECRET_KEY = os.getenv('GPT_SECRET_KEY')
openai.api_key = GPT_SECRET_KEY

def get_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup

def get_article_title(soup):
    title = soup.find('h1').text
    return title

def get_article_author(soup):
    author = soup.find('h2', class_='pw-author-name').text
    return author

def get_article_date(soup):
    date = soup.find('p', class_='pw-published-date').text
    return date

def get_article_reading_time(soup):
    content = soup.find('div', class_='pw-reading-time').text
    return content

# Breaks the medium article into sections and sub sections based on headers
def get_article_content(soup):
    # Get the content of the article
    content = soup.findAll(class_='pw-post-body-paragraph')
    content = [x for x in content]
    heading_tag = 'h1'
    headings = soup.findAll(heading_tag)
    # Fix for articles with only one main heading
    if(len(headings) < 2):
        heading_tag = 'h2'
        headings = soup.findAll(heading_tag)
    sections = {}
    for heading in headings:
        section = {}
        key = '_content_'
        inner_section = []
        temp = heading
        while(True):
            check = temp.next_sibling
            if check is None:
                break
            if check.name == heading_tag:
                break
            if check.name == 'h2':
                if len(inner_section) > 0:
                    section[key] = ' '.join(inner_section)
                key = check.text
                inner_section = []
            temp = check
            if check.name == 'p':
                inner_section.append(check.text)
        if(len(inner_section) > 0):
            section[key] = ' '.join(inner_section)
        if len(section) > 0:
            sections[heading.text] = section
    return sections


# Uses da-vinci to generate a summary of the article based on the sections and sub sections
def fetch_summary(sections):
    final_summary = ""
    article_length = 0
    # Loop through the sections
    for section_count, section in enumerate(sections):
        final_summary += f"<h3>{section}</h3><br>"
        temp_prompt = ""
        # Loop through the sub sections
        for subsection_count, key in enumerate(sections[section]):
            prompt = sections[section][key]
            if(key != '_content_' and len(prompt.split(" ")) > 100):
                # display(Markdown(f"### {key}"))
                final_summary += f"<h4>{key}</h4><br>"
            temp_prompt += prompt
            # If the prompt is too short, add the next section to it
            if(len(temp_prompt.split(" ")) < 100 and section_count != len(sections) - 1 and subsection_count != len(sections[section]) - 1):
                continue
            article_length += len(temp_prompt.split(" "))
            # Generate the summary
            try:
                response = openai.Completion.create(
                    model="text-davinci-003",
                    prompt=f"Summarize the following text. Do not leave any sentences incomplete. If you reach the maximum length, remove the incomplete sentence: \n\n{temp_prompt}",
                    temperature=0.7,
                    top_p=1.0,
                    max_tokens=150,
                    frequency_penalty=0,
                    presence_penalty=1
                )
            except Exception as e:
                print("error occurered")
                continue
            summary = response['choices'][0]['text']
            print(summary)
            if len(summary) > 0:
                final_summary += f"{summary}<br>"
            temp_prompt = ""
    return final_summary, article_length

# Display the summary of the article
def display_summary(url):
    soup = get_soup(url)
    title = get_article_title(soup)
    author = get_article_author(soup)
    date = get_article_date(soup)
    sections = get_article_content(soup)
    title = f"<h1>{title}</h1><br><br>"
    author = f"<h3> Written By:</h3> {author} <h3>on</h3> {date}<br>"
    final_summary, article_length = fetch_summary(sections)
    return (title+author+final_summary), article_length