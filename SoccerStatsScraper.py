from time import sleep
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

def scrape_data(soup, season_text, league_name) :
    import csv 
    import os

    rows = soup.find(id="league-chemp").find_all('tr')

    base_dir = "./"  # Base directory where repositories will be created
    # Create repository directory if it doesn't exist
    repo_dir = os.path.join(base_dir, season_text)
    if not os.path.exists(repo_dir):
        os.makedirs(repo_dir)

    # Path to save the CSV file
    csv_file_path = os.path.join(repo_dir, league_name+".csv")

    # Open the CSV file in write mode
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a CSV writer object
        writer = csv.writer(csvfile)

        # Iterate over each table row
        for row in rows:
            # Extract data from each cell in the row
            row_data = [cell.get_text(strip=True) for cell in row.find_all(['td', 'th'])]

            # Write the row data to the CSV file
            writer.writerow(row_data)

    print(f"\tCSV file saved at: {csv_file_path}")
    
def main():
    
    driver = webdriver.Chrome()
    url = "https://understat.com/league/EPL/2014"
    driver.get(url)
    
    driver.find_element(By.XPATH, "/html/body/div[1]/header/div/div[1]/div").click()                            ## find and click on league button
    sleep(.5)

    leagues = driver.find_elements(By.XPATH, "/html/body/div[1]/header/div/div[1]/ul/li")

    for j in range(len(leagues)):
        league = driver.find_element(By.XPATH, f"/html/body/div[1]/header/div/div[1]/ul/li[{j+1}]")
        league_name = league.text
        print(f"scraping {league_name} league")
        league.click()
        sleep(2)
        
        
        driver.find_element(By.XPATH, "/html/body/div[1]/header/div/div[2]/div").click()
        sleep(0.5)
        seasons = driver.find_elements(By.XPATH, "/html/body/div[1]/header/div/div[2]/ul/li")
            
        for i in range(len(seasons)):
            
            season = driver.find_element(By.XPATH, f"/html/body/div[1]/header/div/div[2]/ul/li[{i+1}]")
            season_text = season.text.replace("/", "-")
            print(f"\tscraping {season_text} season")
            season.click()
            sleep(3)
            
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            
            scrape_data(soup, season_text, league_name)
            
            driver.find_element(By.XPATH, "/html/body/div[1]/header/div/div[2]/div").click()
            sleep(1)
            
        driver.find_element(By.XPATH, "/html/body/div[1]/header/div/div[1]/div").click()
        sleep(1)
        
        
if __name__ == "__main__":
    main()
    
