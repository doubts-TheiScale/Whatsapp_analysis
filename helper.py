from urlextract import URLExtract
import pandas as pd
from collections import Counter
import emoji
def fetch_stats(selected,df):
    if selected !="Overall":
        df =df[df['user']==selected]
        
    
    messages=df.shape[0]
    #finding number of words 
    word=[]
    for i in df["messages"]:
        word.extend(i.split())
        links=[]
   
    #finding number media messages 
    media_messsages=(df[df['messages']=="<Media omitted>\r\n"].shape[0])+(df[df['messages']=="<Media omitted>\r\n\r\n"].shape[0])+(df[df['messages']=="<Media omitted>\n"].shape[0])
    
    #url extraction
    extractor=URLExtract()
    for message in df['messages']:
        links.extend(extractor.find_urls(message))
    return messages,len(word),media_messsages,len(links)

def most_busy_users(df):
    x=df['user'].value_counts().head()
    df=round((df["user"].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={"index":"Name","user":"Name","count":"percentage"})
    return x,df

def most_common_words(selected,df):
    f= open('stop_hinglish.txt','r')
    stop_words = f.read()
    if selected !="Overall":
        df =df[df['user']==selected]
    
    temp = df[df['user'] != 'group notification']
    temp=temp[temp['messages']!="<Media omitted>\n"]
    words=[]
    for message in temp["messages"]:
        for word in message.lower().split():
            if word not in  stop_words:
                words.extend(message.split())
    most_common_df=pd.DataFrame(Counter(words).most_common(25))            
    return most_common_df

def emoji_helper(selected , df):
    if selected !="Overall":
        df =df[df['user']==selected]
    emojis=[]
    for message in df['messages']:
        emojis.extend([c  for c in message if c in emoji.EMOJI_DATA])
    return pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

def monthly_timeline(selected,df):
    if selected !="Overall":
        df =df[df['user']==selected]
    
    timeline=df.groupby(['year','month_num','month']).count()['messages'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+'-'+str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily_timeline(selected,df):
    if selected !="Overall":
        df =df[df['user']==selected]
    daly_timeline=df.groupby("only_date").count()['messages'].reset_index()
    return daly_timeline;