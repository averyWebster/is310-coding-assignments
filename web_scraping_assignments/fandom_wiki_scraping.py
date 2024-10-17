import requests
import csv
from bs4 import BeautifulSoup

season_url = "https://breakingbad.fandom.com/wiki/Category:Breaking_Bad_Episodes#Season_1"

with open('bb_episodes.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Episode Name", "Director", "Writer(s)", "Number of Viewers"])

    page = requests.get(season_url)
    soup = BeautifulSoup(page.content, 'html.parser')

    episodes_section = soup.find('div', class_='category-page__members')

    if episodes_section:
        episode_links = episodes_section.find_all('a', class_='category-page__member-link')

        for link in episode_links:
            episode_url = "https://breakingbad.fandom.com" + link['href']
            
            episode_page = requests.get(episode_url)
            episode_soup = BeautifulSoup(episode_page.content, 'html.parser')

            episode_name = episode_soup.find('h1', class_='page-header__title').text.strip()

            director = "N/A"
            writers = "N/A"
            viewers = "N/A"

            infobox = episode_soup.find('aside', class_='portable-infobox')

            if infobox:
                for row in infobox.find_all('div', class_='pi-item'):
                    header = row.find('h3', class_='pi-data-label')
                    if header:
                        header_text = header.text.strip()
                        data_value = row.find('div', class_='pi-data-value').text.strip()

                        if 'Directed by' in header_text:
                            director = data_value
                        elif 'Written by' in header_text:
                            writers = data_value
                        elif 'U.S. Viewers' in header_text or 'viewers' in header_text.lower():
                            viewers = data_value

            print(f"Episode Name: {episode_name}")
            print(f"Director: {director}")
            print(f"Writers: {writers}")
            print(f"Viewers: {viewers}")

            writer.writerow([episode_name, director, writers, viewers])
    else:
        print("Unable to find episodes section.")

