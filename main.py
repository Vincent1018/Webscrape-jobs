from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import requests 
import time

#1 create a variable to hold all of the user inputs
#2 create a loop to keep asking the user for input and stop when they are 'done'
#3 after each input, append it to the unfamiliar_skills list
unfamiliar_skills = []

while True:
    user_input = input('Enter skills you are unfamiliar with (or type "done" when finished):')

    if user_input.lower() == 'done':
            break
    
    unfamiliar_skills.append(user_input)

#4 if the user has no unfamiliar skills, praise em
#5 else print a message stating what skills are being filtered out from the job postings   
if not unfamiliar_skills:
    print("You have no unfamiliar skills? Wonderful!")

else:
    print(f'Filtering Out {unfamiliar_skills}')

#6 create a function for the scraping and writing of data into files
#7 use requests.get to get the .text of a webpage
#8 create an instance of BeautifulSoup for html_text using the lxml parser
#9 in the BeautifulSoup instance, find all of the li tags that have the "clearfix job-bx wht-shd-bx" class to get every job posting
def find_jobs(base_url, num_pages):
    for page in range(1, num_pages + 1):
        url = f'{base_url}&sequence={page}'
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')
        jobs = soup.find_all('li', class_= "clearfix job-bx wht-shd-bx")

        #10 enumerate the jobs variable so we can access the index and loop through each job and their index in jobs
        #11 set the published_date = to when the job posting was published, it's in a span tag within a span tag
        #12 if 'few' exists in the published date then it is recent and we want to include this job
        for index, job in enumerate(jobs):
            published_date = job.find('span', class_ = 'sim-posted').span.text

            if 'few' in published_date:

                #13 find the company name, the skills and the link to more info for the job posting
                #14 initialize an unfamiliar_counter to count if there are unfamiliar skills from the user in the required skills list of the job posting
                company_name = job.find('h3', class_= 'joblist-comp-name').text.replace(' ','')
                skills = job.find('span', class_ = "srp-skills").text.replace(' ', '')
                more_info = job.header.h2.a['href']

                unfamiliar_counter = 0
                
                #15 if there are unfamiliar skills, loop through each one and if it exists in the required skills, add 1 to the unfamiliar_counter
                #16 if there are no unfamiliar skills in the required skills of the job posting then open a new .txt file associated with the job's index
                    #16.5 and write the company name, required skills and more info link into it, then print where it was saved
                if unfamiliar_skills:
                    for skill in unfamiliar_skills:
                        if skill in skills:
                            unfamiliar_counter = unfamiliar_counter + 1
                        
                        if unfamiliar_counter == 0:
                            with open(f'posts/{index}.txt', 'w') as f:
                                f.write(f"Company Name: {company_name.strip()} \n") 
                                f.write(f"Required Skills: {skills.strip()} \n") 
                                f.write(f"More Info: {more_info}")
                            print(f'File Saved: {index}')

                #17 if there are no unfamiliar_skills at all then go ahead and write into a file the company name, required skill and more info link for the job
                else:
                    with open(f'posts/{index}.txt', 'w') as f:
                        f.write(f"Company Name: {company_name.strip()} \n") 
                        f.write(f"Required Skills: {skills.strip()} \n") 
                        f.write(f"More Info: {more_info}")
                    print(f'File Saved: {index}')

#18 if this python script is being run as the main program and not as a module to another script (which it isn't), then wait x time and rerun 
if __name__ == '__main__':
    base_url = 'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation='

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 10)

    try:
        driver.get(base_url)

        # Navigate through the pagination
        while True:
            try:
                # Wait for the 'Next' button to be clickable
                next_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "nxtC")))

                # Use JavaScript to click the 'Next' button
                driver.execute_script("arguments[0].click();", next_button)

            except (NoSuchElementException, TimeoutException, StaleElementReferenceException):
                # Break the loop if 'Next' button is not found or not clickable
                break

        # Once the last page is reached, find the last page number
        page_numbers = driver.find_elements(By.TAG_NAME, 'em')
        last_page_num = max([int(page.text) for page in page_numbers if page.text.isdigit()])

        print(f"Last page number: {last_page_num}")

    finally:
        driver.quit()
    #while True: 
     #   find_jobs(base_url, num_pages)
      #  time_wait = 10
       # print(f"Waiting {time_wait} minutes...")
        #time.sleep(time_wait * 60)


