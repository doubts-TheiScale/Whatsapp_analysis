import streamlit as st
import preprocessor
import helper
import matplotlib.pyplot as plt
st.sidebar.title("whatsapp chat analysis")
uploded_file= st.sidebar.file_uploader("choose a file")


if uploded_file is not None:
    byte_data = uploded_file.getvalue()
    data=byte_data.decode("utf-8")
    df=preprocessor.preprocessor(data)
    st.dataframe(df)
    user_list = df["user"].unique().tolist()
    try:
        user_list.remove("group notification")
    except:
        print("NO group notification found 🤷‍♂️🤷‍♀️")  
    user_list.sort() 
    user_list.insert(0,"Overall")
    sellected = st.sidebar.selectbox("show analysis wrt:",user_list)
    
    if st.sidebar.button("show Analysis"):
        st.title("Top Statistics of whatsapp analysis")
        messages,words,media_messages,links=helper.fetch_stats(sellected,df)
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(messages)
        with col2:
            st.header("Total words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(media_messages)
        with col4:
            st.header("links shared")
            st.title(links)
        if sellected == "Overall":
            st.title("MOst busy persion")
            x,new_df= helper.most_busy_users(df)
            fig, ax = plt.subplots()
            col1,col2=st.columns(2)
            with col1:
                ax.bar(x.index,x.values, color = "red")
                st.pyplot(fig)
            with col2:
                # st.header("Total words")
                st.dataframe(new_df)
        # common wolrds
        most_common_df =helper.most_common_words(sellected,df)
        st.dataframe(most_common_df)
        fig , ax =plt.subplots()
        ax.bar(most_common_df[0],most_common_df[1],color="orange")
        plt.xticks(rotation ='vertical')
        st.title("most Common words")
        st.pyplot(fig)

        #emoji
        emoji_df= helper.emoji_helper(sellected , df)
        st.title("Emoji analysis:")
        
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig , ax =plt.subplots()
            ax.pie(emoji_df[1].head(), labels=emoji_df[0].head(),autopct="%0.2f")
            st.pyplot(fig)


        ## "Montly Timeline Analysis
        st.title("Montly Timeline Analysis:")
        timeline=helper.monthly_timeline(sellected,df)
        fig , ax =plt.subplots()
        ax.plot(timeline['time'],timeline['messages'])
        plt.xticks(rotation ='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title("Daily Timeline Analysis:")
        daily_timeline=helper.daily_timeline(sellected,df)
        fig , ax =plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['messages'])
        plt.xticks(rotation ='vertical')
        st.pyplot(fig)