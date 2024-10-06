import undetected_chromedriver as uc
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from bs4 import BeautifulSoup
import config
import openai
from discord_webhook import DiscordWebhook

#Function to create a Chromium instance we will use later
def create_driver():
    chrome_options = Options()
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")

    driver = uc.Chrome(options=chrome_options)
    
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script('''window.navigator.chrome = {
        runtime: {},
        // etc.
    };''')
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']});")
    
    return driver
    
def listOffers(driver, url):
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'a[data-jk]'))
    )

    job_elements = driver.find_elements(By.CSS_SELECTOR, 'a[data-jk]')
    job_ids = [job.get_attribute('data-jk') for job in job_elements]

    new_ids = []
    
    try:
        with open('visited.txt', 'r') as file:
            existing_ids = set(line.strip() for line in file)
    except FileNotFoundError:
        existing_ids = set()

    with open('visited.txt', 'a') as file:
        for job_id in job_ids:
            if job_id not in existing_ids:
                new_ids.append(job_id)
                file.write(f"{job_id}\n")

    return new_ids
    
def loadOfferInformations(driver, offerId):
    offerUrl = f"https://fr.indeed.com/viewjob?jk={offerId}"
    driver.get(offerUrl)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'div.jobsearch-JobComponent'))
    )

    offer_element = driver.find_element(By.CSS_SELECTOR, 'div.jobsearch-JobComponent')
    offer_html = offer_element.get_attribute('outerHTML')

    soup = BeautifulSoup(offer_html, 'html.parser')
    offer_text = soup.get_text(separator='\n', strip=True)

    title_text = 'NOT_FOUND'
    try:
        title_element = driver.find_element(By.CSS_SELECTOR, 'h1[data-testid="jobsearch-JobInfoHeader-title"]')
        title_text = title_element.text.strip()
    except Exception as e:
        print(e)
        
    company_name = 'NOT_FOUND'
    try:
        company_element = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="inlineHeader-companyName"]')
        company_name = company_element.text.strip()
    except Exception as e:
        print(e)
        
    company_location = 'NOT_FOUND'
    try:
        location_element = driver.find_element(By.CSS_SELECTOR, 'div[data-testid="inlineHeader-companyLocation"]')
        company_location = location_element.text.strip()
    except Exception as e:
        print(e)
        
    short_description = 'NOT_FOUND'
    try:
        short_description_element = driver.find_element(By.CSS_SELECTOR, 'div#salaryInfoAndJobType')
        short_description = short_description_element.text.strip()
    except Exception as e:
        print(e)
    return [offer_text, title_text, company_name, company_location, short_description]

def getOfferScore(offerData):
    prompt = f"""
    Here's my resume:
    BEGINNING OF RESUME
    ===============================================
    {config.RESUME}
    ========================================
    END OF RESUME

    Now, here's a job offer:

    BEGINNING OF THE JOB OFFER
    ========================================
    {offerData}
    ================================================
    END OF THE JOB OFFER

    Can you estimate the % of compatibility between this job offer and my resume, to know if it will be interesting for me ? Just answer with the % (0 = completely incompatible, 100 = absolutely compatible). Answer only with a number, nothing else.
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150,  
            temperature=0.7
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        return None
        
def sendToDiscord(webhook_url, score, job_id, titre, description, entreprise, lieu):
    message = (
        f"=================================================\n"
        f"New interesting offer !\n"
        f"Title: {titre}\n"
        f"Description: {description}\n"
        f"Company: {entreprise}\n"
        f"Place: {lieu}\n"
        f"Score : {score}\n"
        f"Link : https://fr.indeed.com/viewjob?jk={job_id}\n"
        f"=================================================\n"
    )

    webhook = DiscordWebhook(url=webhook_url, content=message)

    try:
        response = webhook.execute()
        if response.status_code == 200:
            print("Message successfully sent.")
        else:
            print(f"Error while sending the message : {response.status_code}")
    except Exception as e:
        print(f"UError while sending the message : {e}")

global driver
newOffersList = []
openai.api_key = config.API_KEY
def initializeDriver():
    welcome_screen = """                                                                                    
                  @@@@@@@@@@                                                                     
             @@@@       @@   @@@@                                                                
           @@                @@@ @@                                                              
         @@                     @@ @@                                                            
       @@                         @@ @@                                                 -++      
      @@       @@@ @@ @@@          @@ @@                                           +@@@@@++@@@@  
      @      @@    @@    @@            @                                         @@%           %@
     @@     @@   @@@@@@   @@           @@                                      *@-               
     @     @@   @     @@   @            @                                     @%     %@@@@@      
     @ @   @@@@@@     @@@@@@            @@                                   @      @@@@@@@@     
     @@@@   @   @@   @@   @@            @@                                  @       @@@@@@@@     
     @@@@    @     @@    @@       @@@   @@                                  +        @@@@@@-     
      @ @@    @@@  @@  @@@              @@                                 #                     
       @ @@      @@@@@@                  @@                                               %      
        @ @@                              @@                                          @@@@@      
         @@                                @                                          @@@@@      
           @@@                          @@@@                                          @@@@@      
             @@        @@@              @@                                            @@@@@      
             @@           @@          @@@@                                            @@@@@      
             @@@@@@ @@     @@           @@                                            @@@@@      
             @@   @@@       @           @@                                            @@@@@      
             @@   @@@        @@        @@                                             @@@@*      
             @@@@@@@@@       @@@@@@@@@@                                                          
             @@              @@                                                                  
             @@              @@                                                                  
                                                                                                        
    Indeed job offers analyser by https://github.com/LouisDeMilleville \n
    """
    print(welcome_screen)
    print("Starting the bot...")
    driver = create_driver()
    time.sleep(3)
    driver.get('https://indeed.com/')
    time.sleep(3)
    return driver

driver = initializeDriver()
with open('search.txt', 'r') as file:
    urlsList = set(line.strip() for line in file)
for url in urlsList:
    urlOffers = listOffers(driver, url)
    newOffersList += urlOffers
    time.sleep(5)

for offer in newOffersList:
    offerData = loadOfferInformations(driver, offer)
    offerScore = getOfferScore(offerData[0])
    if int(offerScore) >= config.MINIMUM:
        sendToDiscord(config.WEBHOOK_URL, offerScore, offer, offerData[1], offerData[4], offerData[2], offerData[3])
    else:
        print("Offre pas suffisement intéressante :/")
        print(offerScore)
    time.sleep(3)
