import re 
import pandas as pd
def preprocessor(data):
    pattern ='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages =re.split(pattern,data)[1:]
    dates = re.findall(pattern,data)
    df= pd.DataFrame({"user_message":messages,"message_dates":dates})
    df['message_dates']=pd.to_datetime(df['message_dates'],format = "%d/%m/%y, %H:%M - ")
    df.rename(columns={"message_dates":"dates"},inplace =True)
    users = []
    messages=[]
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s',message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append("group notification")
            messages.append(entry[0])
    df["user"]=users
    df["messages"]=messages
    df.drop(columns=["user_message"],inplace= True)
    df['year']=df['dates'].dt.year
    df['month']=df['dates'].dt.month_name()
    df['date']=df['dates'].dt.date
    df['day_name'] = df['dates'].dt.day_name()
    df['hour']=df['dates'].dt.hour
    df['minute']=df['dates'].dt.minute
    df['month_num']=df['dates'].dt.month
    df['only_date']=df['dates'].dt.date
    print(df)
    
    return df