from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time


options = Options()
# options.add_argument("user-data-dir=/home/ahmed-elatar/.config/google-chrome")

options.add_argument("profile-directory=Default")
# path_to_chromedriver = 'home/ahmed-elatar/.config/google-chrome'


driver_service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=driver_service, options=options)

#Function to convert tweets to List of strings 
def Get_tweets(username,n):
        list_of_tweets=[]
    
        link = 'https://twitter.com/'+username
        driver.get(link)

        tweet_text_elements = []

        # Scroll n / 2  times to load  tweets
        
        for i in range(max((n//2),1)):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(4) 

            html_content = driver.page_source
            soup = BeautifulSoup(html_content, 'html.parser')

            # Find all elements with 'tweetText'
            tweet_text_elements.extend(soup.find_all('div', {'data-testid': 'cellInnerDiv'}))

        # first n tweet
        for tweet_text_element in tweet_text_elements[:n]:
            tweet_text = tweet_text_element.text.strip().replace("\n", "")
            list_of_tweets.append(tweet_text)
            
        return list_of_tweets
            
# Function to search about Tickers in the List of string 
# 
def Count_tiker(Ticker , List_of_users , num_of_tweets,wait_time):
    t=0
    while(True):
        t+=1
        
        print(f"start {t}  interval ")
        driver.set_window_position(900,50)
        
        counter=0
        for user in List_of_users:
            cnt=0
            tweets=Get_tweets(user , num_of_tweets)
            for k in tweets:
                counter+= k.lower().count(Ticker.lower())
                cnt+=  k.lower().count(Ticker.lower())
            print(" Ticker : " ,Ticker," has mentioned ",cnt, "times" ,user ,"Account in last ",num_of_tweets,"tweets" )
        print(" Ticker : ",ticker , " has mentioned ",counter , " times in last ",num_of_tweets,"tweets of all Accounts")
        print(f"finsed {t} time --------------------------------------------------------")
        driver.minimize_window()
        time.sleep(wait_time*60)
            
         


List_of_users=["Mr_Derivatives", "warrior_0719","ChartingProdigy","allstarcharts",
               "yuriymatso","TriggerTrades","AdamMancini4", "CordovaTrades", "Barchart"
]

ticker="$SPX"                  # the ticker to search about it 
num_tweets=5                   #last x tweets in this account
time_between_intervals=0.3     #time between intervals


Count_tiker(ticker,List_of_users,num_tweets,time_between_intervals)















