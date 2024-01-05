from bs4 import BeautifulSoup
import requests 
import time

#create a variable to hold all of the user inputs
unfamiliar_skills = []

#create a loop to keep asking the user for input and stop when they are 'done'
while True:
    user_input = input('Enter skills you are unfamiliar with (or type "done" when finished):')

    if user_input.lower() == 'done':
            break
    
    #after each input, append it to the unfamiliar_skills list
    unfamiliar_skills.append(user_input)

#if the user has no unfamiliar skills, praise em
if not unfamiliar_skills:
    print("You have no unfamiliar skills? Wonderful!")

#print a message stating what skills are being filtered out from the job postings
else:
    print(f'Filtering Out {unfamiliar_skills}')

#create a function for the scraping and writing of data into files
def find_jobs():

    #use requests.get to get the .text of a webpage
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords=python&txtLocation=').text
    
    #create an instance of BeautifulSoup for html_text using the lxml parser
    soup = BeautifulSoup(html_text, 'lxml')

    #in the BeautifulSoup instance, find all of the li tags that have the "clearfix job-bx wht-shd-bx" class to get every job posting
    jobs = soup.find_all('li', class_= "clearfix job-bx wht-shd-bx")

    #enumerate the jobs variable so we can access the index and loop through each job and their index in jobs
    for index, job in enumerate(jobs):

        #set the published_date = to when the job posting was published, it's in a span tag within a span tag
        published_date = job.find('span', class_ = 'sim-posted').span.text

        #if 'few' exists in the published date then it is recent and we want to include this job
        if 'few' in published_date:

            #find the company name, the skills and the link to more info for the job posting
            company_name = job.find('h3', class_= 'joblist-comp-name').text.replace(' ','')
            skills = job.find('span', class_ = "srp-skills").text.replace(' ', '')
            more_info = job.header.h2.a['href']

            #initialize an unfamiliar_counter to count if there are unfamiliar skills from the user in the required skills list of the job posting
            unfamiliar_counter = 0
            
            #if there are unfamiliar skills, loop through each one and if it exists in the required skills, add 1 to the unfamiliar_counter
            if unfamiliar_skills:
                for skill in unfamiliar_skills:
                    if skill in skills:
                        unfamiliar_counter = unfamiliar_counter + 1
                    
                    #if there are no unfamiliar skills in the required skills of the job posting then open a new .txt file associated with the job's index
                        #and write the company name, required skills and more info link into it, then print where it was saved
                    if unfamiliar_counter == 0 or not unfamiliar_skills:
                        with open(f'posts/{index}.txt', 'w') as f:
                            f.write(f"Company Name: {company_name.strip()} \n") 
                            f.write(f"Required Skills: {skills.strip()} \n") 
                            f.write(f"More Info: {more_info}")
                        print(f'File Saved: {index}')

            #if there are no unfamiliar_skills at all then go ahead and write into a file the company name, required skill and more info link for the job
            else:
                with open(f'posts/{index}.txt', 'w') as f:
                    f.write(f"Company Name: {company_name.strip()} \n") 
                    f.write(f"Required Skills: {skills.strip()} \n") 
                    f.write(f"More Info: {more_info}")
                print(f'File Saved: {index}')

#if this python script is being run as the main program and not as a module to another script (which it is), then wait x time and rerun 
if __name__ == '__main__':
    while True: 
        find_jobs()
        time_wait = 10
        print(f"Waiting {time_wait} minutes...")
        time.sleep(time_wait * 60)