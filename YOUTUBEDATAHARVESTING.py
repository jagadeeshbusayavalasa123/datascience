#import streamlit as st
#import sqlite3 as sql
#import pandas as pd
from googleapiclient.discovery import build
from pandas import json_normalize
from datetime import datetime
#from isodate import parse_duration
import streamlit as st
import json
import os
import time
import pymongo
import pandas as pd
#import mysql.connector
import sqlite3 as sql
from isodate import parse_duration

import plotly.express as px
from streamlit_option_menu import option_menu


with st.sidebar:
    selected = option_menu(None, ["Home","SQL queries Q&A"], 
                           icons=["house-door-fill","list-task","card-text"],
                           default_index=0,
                           orientation="vertical",
                           styles={"nav-link": {"font-size": "30px", "text-align": "centre", "margin": "0px", 
                                                "--hover-color": "#0e42ab"},
                                   "icon": {"font-size": "20px"},
                                   "container" : {"max-width": "6000px"},
                                   "nav-link-selected": {"background-color": "#6f9ee8"}}) #C80101
    
st.title("WELCOME TO YOUTUBE DATA HARVESTING") #2de376
st.text("\n")
def header(url):
     st.markdown(f'<p style="background-color:#0066cc;color:#e8f7e1;font-size:24px;text-align: center;border-radius:2%;">{url}</p>', unsafe_allow_html=True)
header("USEFUL  KPI  METRICS !!!")
st.text("\n")

st.markdown("""
<style>
div[data-testid="metric-container"] {
   background-color: rgba(28, 131, 225, 0.1);
   border: 1px solid rgba(28, 131, 225, 0.1);
   padding: 5% 5% 5% 10%;
   border-radius: 5px;
   color: rgb(30, 103, 119);
   overflow-wrap: break-word;
   text-align: center;         
}

/* breakline for metric text         */
div[data-testid="metric-container"] > label[data-testid="stMetricLabel"] > div {
   overflow-wrap: break-word;
   white-space: break-spaces;
   color: white;
   text-align: center;         
   font-size:70px;
}
</style>
"""
, unsafe_allow_html=True)


m = st.markdown("""
<style>
div.stButton > button:first-child {
    background-color: rgb(13, 191, 37);
}
</style>""", unsafe_allow_html=True)  

            
con = sql.connect("jaga.db")
mycursor=con.cursor()

mycursor.execute("""SELECT count(*),SUM(total_videos)  FROM channels""")    
noofchannels,total_videos=mycursor.fetchone() 
print(noofchannels) 
mycursor.execute("""SELECT channel_name,Subscribers FROM channels order by Subscribers DESC limit 1""") 
channel_with_highest_subscribers,Subscribers=mycursor.fetchone()
#Subscribers=mycursor.fetchone()[1]
mycursor.execute("""SELECT Title, Views
                            FROM videos 
                            ORDER BY Views DESC
                            LIMIT 1""")
video_name,view_count=mycursor.fetchone()
col1, col2, col3 = st.columns(3)
col1.metric("NUMBER   Of   CHANNELS  in   DATAWAREHOUSE", noofchannels,str(total_videos)+" videos")
col2.metric("CHANNEL  WITH  HIGHEST  NUMBER  OF  SUBSCRIBERS", channel_with_highest_subscribers, str(Subscribers)+" Subscibers")
col3.metric("MOST  TRENDING  VIDEO ", video_name, str(view_count)+" Views")

def run_queries(questions):
    if questions == '1. What are the names of all the videos and their corresponding channels?':
        mycursor.execute("""SELECT Title AS Video_Title, channel_title AS Channel_Name
                            FROM videos
                            ORDER BY channel_title""")
        #print(mycursor.fetchall())
        st.write("### :green[all videos in each channel :]")
        df = pd.DataFrame(mycursor.fetchall(),columns=['Video_Title','Channel_Name'])
        st.table(df)
        
    elif questions == '2. Which channels have the most number of videos, and how many videos do they have?':
        mycursor.execute("""SELECT channel_name AS Channel_Name, total_videos AS Total_Videos
                            FROM channels
                            ORDER BY total_videos DESC""")
        st.write("### :green[Number of videos in each channel :]")
        df = pd.DataFrame(mycursor.fetchall(),columns=['Channel_Name','Total_Videos'])
        st.table(df)
        #st.dataframe(df.style.highlight_max(axis=1))


       # st.write("### :green[Number of videos in each channel :]")
        #st.bar_chart(df,x= mycursor.column_names[0],y= mycursor.column_names[1])
        #fig = px.bar(df,
                  #   x=mycursor.column_names[0],
                  #   y=mycursor.column_names[1],
                   #  orientation='v',
                    # color=mycursor.column_names[0]
                    #)
        #st.plotly_chart(fig,use_container_width=True)
        
    elif questions == '3. What are the top 10 most viewed videos and their respective channels?':
        mycursor.execute("""SELECT channel_title AS Channel_Name, Title AS Video_Title, Views AS Views 
                            FROM videos 
                            ORDER BY Views DESC
                            LIMIT 10""")
        df = pd.DataFrame(mycursor.fetchall(),columns=['Channel_Name','Video_Title','Views'])
        st.write("### :green[Top 10 most viewed videos :]")
        st.table(df)
        #st.write("### :green[Top 10 most viewed videos :]")
        fig = px.bar(df,
                     x=mycursor.description[2],
                     y=mycursor.description[1],
                     orientation='h',
                     color=mycursor.description[0]
                    )
        st.plotly_chart(fig,use_container_width=True)
        
    elif questions == '4. How many comments were made on each video, and what are their corresponding video names?':
        mycursor.execute("""SELECT Title,Comments from videos ORDER BY Comments DESC""")
        df = pd.DataFrame(mycursor.fetchall(),columns=['Video_Title','Total Comments'])
        
        st.write("### :green[videos and comments-count:]")
        st.table(df)
          
    elif questions == '5. Which videos have the highest number of likes, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_title AS Channel_Name,title AS Video_Name,FORMAT(Likes,0) AS Likes_Count 
                            FROM videos
                            ORDER BY likes DESC
                            LIMIT 10""")
        df = pd.DataFrame(mycursor.fetchall(),columns=['Channel_Name','Video_Name', 'Likes_Count'])
        st.write("### :green[Top 10 most liked videos :]")
        st.table(df)
        #st.write("### :green[Top 10 most liked videos :]")
        fig = px.bar(df,
                     x=mycursor.description[2],
                     y=mycursor.description[1],
                     orientation='h',
                     color=mycursor.description[0]
                    )
        st.plotly_chart(fig,use_container_width=True)
        
    elif questions == '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?':
        mycursor.execute("""SELECT channel_title AS Channel_Name,Title AS Video_Name, FORMAT(Likes,0) AS Likes_Count, FORMAT(Dislikes,0) as Dislike_Count
                            FROM videos
                            ORDER BY likes DESC""")
        df = pd.DataFrame(mycursor.fetchall(),columns=['Channel_Name','Video_Name', 'Likes_Count','Dislike_Count'])
        st.write("### :green[Likes & Dislikes of each video :]")
        st.table(df)
         
    elif questions == '7. What is the total number of views for each channel, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_name AS Channel_Name, Views AS Views
                            FROM channels  ORDER BY views DESC""")
        df = pd.DataFrame(mycursor.fetchall(),columns=['Channel_Name','Views'])
        st.write("### :green[Channel Views :]")

        st.table(df)
        #st.write("### :green[Channels vs Views :]")
       # fig = px.bar(df,
                    # x=mycursor.column_names[0],
                    # y=mycursor.column_names[1],
                   #  orientation='v',
                    # color=mycursor.column_names[0]
                   # )
       # st.plotly_chart(fig,use_container_width=True)
        
    elif questions == '8. What are the names of all the channels that have published videos in the year 2022?':
        mycursor.execute("""SELECT distinct channel_title AS Channel_Name
                            FROM videos
                            WHERE Published_date LIKE '2022%'
                             ORDER BY channel_name""")
        df = pd.DataFrame(mycursor.fetchall(),columns=['Channel_Name'])
        st.write("### :green[Channels published videos in 2022 :]")
        st.write(df)
        
    elif questions == '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?':
        mycursor.execute("""select channel_title,AVG(duration) from videos group by channel_title order by AVG(duration) DESC""")
        st.write("### :green[Avg video duration for channels :]")
        df = pd.DataFrame(mycursor.fetchall(),columns=['Channel_name','Average duration(in sec)'])
        st.write(df)
        
    elif questions == '10. Which videos have the highest number of comments, and what are their corresponding channel names?':
        mycursor.execute("""SELECT channel_title AS Channel_Name,Title AS Video_Name,Comments AS Comments
                            FROM videos
                            ORDER BY comments DESC
                            LIMIT 10""")
        df = pd.DataFrame(mycursor.fetchall(),columns=['channel_title','video_name','comments'])
        st.write("### :green[Videos with most comments :]")
        st.write(df)
        #st.write("### :green[Videos with most comments :]")
#----------------------------------FUNCTIONS FOR HOME PAGE-----------------------------------------------------
api_key='AIzaSyAo5fKuWi0aSY87GFPAZLGfG8MZX_GYDls'
#ALL FUNCTIONS
# Function to retrive response list of channels from api
def channel_details(channel_id):
    #api_key ='AIzaSyBaFlktgFkWfsxcAfCz_dcTaaJdCn5tUZA' #'AIzaSyAo5fKuWi0aSY87GFPAZLGfG8MZX_GYDls'
    youtube_sob = build('youtube', 'v3', developerKey=api_key)
    # channels_data_list=[]

    request = youtube_sob.channels().list(part="statistics,snippet,contentDetails", id=channel_id)
    response = request.execute()
    # print(len(response['items']))
    # print(response)

    # for i in range(0,len(response['items'])):
    channel_data = {'channel_id': response['items'][0]['id'], 'channel_name': response['items'][0]['snippet']['title'],
                    'Subscribers': response['items'][0]['statistics']['subscriberCount'],
                    'Views': response['items'][0]['statistics']['viewCount'],
                    'Total_videos': response['items'][0]['statistics']['videoCount'],
                    'playlist_id': response['items'][0]['contentDetails']['relatedPlaylists']['uploads']}

    # channel_data_list.append(channel_data)

    return channel_data


# function for playlist
def getPlaylistsData(channel_id):
    c = []
    #api_key = 'AIzaSyBaFlktgFkWfsxcAfCz_dcTaaJdCn5tUZA'
    youtube_sob = build('youtube', 'v3', developerKey=api_key)

    request = youtube_sob.playlists().list(
        part="snippet,contentDetails",
        channelId=channel_id,
        maxResults=25
    )
    playlist_response = request.execute()
    for item in playlist_response['items']:
        playlist = {'playlist_id': item['id'],
                    'playlist_name': item['snippet']['title'],
                    'channel_id': item['snippet']['channelId'],
                    'videos_count': item['contentDetails']['itemCount'],

                    }
        c.append(playlist)
    return c


# function to get video ids
def get_video_ids(playlist_id):
   # api_key = 'AIzaSyBaFlktgFkWfsxcAfCz_dcTaaJdCn5tUZA'
    youtube = build('youtube', 'v3', developerKey=api_key)

    request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50)
    response = request.execute()

    video_ids = []

    for i in range(len(response['items'])):
        video_ids.append(response['items'][i]['contentDetails']['videoId'])

    next_page_token = response.get('nextPageToken')
    more_pages = True

    while more_pages:
        if next_page_token is None:
            more_pages = False
        else:
            request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=playlist_id,
                maxResults=50,
                pageToken=next_page_token)
            response = request.execute()

            for i in range(len(response['items'])):
                video_ids.append(response['items'][i]['contentDetails']['videoId'])

            next_page_token = response.get('nextPageToken')

    return video_ids


# ALL VIDEPO DETAILS
# TO GET ALLL VIDEO DETAILS OF 5 CHANNELS
def get_all_video_details(video_ids):
    all_video_stats = []
    #api_key = 'AIzaSyBaFlktgFkWfsxcAfCz_dcTaaJdCn5tUZA'
    youtube = build('youtube', 'v3', developerKey=api_key)

    for i in range(0, len(video_ids), 50):
        request = youtube.videos().list(
            part='snippet,statistics,contentDetails',
            id=','.join(video_ids[i:i + 50]))
        response = request.execute()
        # print(response)

        for video in response['items']:
            # print(video)
            #print(video['statistics']['likeCount'])
            # print(video['statistics']['commentCount'])
            # print(video['statistics']['dislikeCount'])
            # print(video)
            video_stats = {'Title': video['snippet']['title'],
                           'Description': video['snippet']['description'],
                           'Published_date': video['snippet']['publishedAt'],
                           'duration': video['contentDetails']['duration'],
                           'Views': video['statistics']['viewCount'],
                           'Likes': video['statistics'].get('likeCount'),
                            'Dislikes': video['statistics'].get('dislikeCount'),
                           'Comments': video['statistics'].get('commentCount'),
                           'favourite_count': video['statistics']['favoriteCount'],
                           'thumbnail': video['snippet']['thumbnails']['default']['url'],

                           'video_id': video['id'],
                           'channel_id': video['snippet']['channelId'],
                           'channel_title': video['snippet']['channelTitle'],
                           'caption_status': video['contentDetails']['caption']

                           # 'tags':video['snippet']['tags']
                           }
            all_video_stats.append(video_stats)

    return all_video_stats


# vl=['s6kR8O_imTA', 'FY2_mAf7Qes', 'MJ8h4QoEDtA']

# to get comments

def get_comments(video_id, token='', c=[]):  # comments=[],
    # comments=[]
    # c=[]
    #api_key = 'AIzaSyBaFlktgFkWfsxcAfCz_dcTaaJdCn5tUZA'
    youtube = build('youtube', 'v3', developerKey=api_key)

    video_response = youtube.commentThreads().list(part='snippet',
                                                   videoId=video_id, maxResults=50,
                                                   pageToken=token).execute()
    for item in video_response['items']:
        comment = {'comment_id': item['id'],
                   'comment_name': item['snippet']['topLevelComment']['snippet']['textDisplay'],
                   'author': item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                   'video_id': item['snippet']['videoId'],
                   'published_date': item['snippet']['topLevelComment']['snippet']['publishedAt']

                   }
        c.append(comment)
        # print(len(video_response['items']))

    next_page_token = video_response.get('nextPageToken')
    # print(next_page_token)

    if next_page_token is not None:
        return get_comments(video_id, next_page_token, c)
    else:
        return c


# for getting all comments actual funct
def commentdetails(videoids_list):
    allcommentstest = []
    # allcommentlist=[]
    for videoId in videoids_list:
          comment_threads = get_comments(videoId, c=[])
        # print(len(comment_threads))
        # print(len(comment_threads))
          allcommentstest.extend(comment_threads)
  
         #st.error("comments disabled for channel")
    # c=list()
    return allcommentstest


# MAIN function when channel id comes from ui

def main(channel):
    c = channel_details(channel)

    p = getPlaylistsData(channel)
    playlist_ids = c['playlist_id']  
    videoids_list = get_video_ids(playlist_ids)
    v = get_all_video_details(videoids_list)
    cm = commentdetails(videoids_list)
    data = {'channel details': c,
            'playlist details': p,
            'video details': v,
            'comment details': cm
            }
    return data


# function toconvert duration of video in seconds
def iso8601_to_minutes(duration_str):
    duration = parse_duration(duration_str)
    total_seconds = duration.total_seconds()
    # total_minutes = total_seconds / 60
    return total_seconds

def convert_to_numeric(data):
    channel_df = pd.DataFrame(data['channel details'], index=[0])
    playlist_df = pd.DataFrame(data['playlist details'])
    video_df = pd.DataFrame(data['video details'])
    comments_df = pd.DataFrame(data['comment details'])

    channel_df['Subscribers'] = pd.to_numeric(channel_df['Subscribers'])
    channel_df['Views'] = pd.to_numeric(channel_df['Views'])
    channel_df['Total_videos'] = pd.to_numeric(channel_df['Total_videos'])
    # video_df['Published_date']=pd.to
    video_df['Views'] = pd.to_numeric(video_df['Views'])
    video_df['Likes'] = pd.to_numeric(video_df['Likes'])
    video_df['Dislikes'] = pd.to_numeric(video_df['Dislikes'])
    video_df['Comments'] = pd.to_numeric(video_df['Comments'])
    
    video_df['duration'] = video_df['duration'].apply(iso8601_to_minutes)
    video_df['Published_date']=video_df['Published_date'].apply(convert_publish_date)
    comments_df['published_date']=comments_df['published_date'].apply(convert_publish_date)
    return channel_df,playlist_df,video_df,comments_df


def mongo_upload(data):
    channel_df = pd.DataFrame(data['channel details'], index=[0])
    playlist_df = pd.DataFrame(data['playlist details'])
    video_df = pd.DataFrame(data['video details'])
    comments_df = pd.DataFrame(data['comment details'])

    # convert channel column dtypes into numeric
    channel_df['Subscribers'] = pd.to_numeric(channel_df['Subscribers'])
    channel_df['Views'] = pd.to_numeric(channel_df['Views'])
    channel_df['Total_videos'] = pd.to_numeric(channel_df['Total_videos'])
    # video_df['Published_date']=pd.to
    video_df['Views'] = pd.to_numeric(video_df['Views'])
    video_df['Likes'] = pd.to_numeric(video_df['Likes'])
    video_df['Dislikes'] = pd.to_numeric(video_df['Dislikes'])
    
    video_df['Comments'] = pd.to_numeric(video_df['Comments'])
    # print(channel_df.info(),video_df.info())
    video_df['duration'] = video_df['duration'].apply(iso8601_to_minutes)
    collections = [channel_df, playlist_df, video_df, comments_df]
    con = pymongo.MongoClient("mongodb://localhost:27017/")
    db = con['capstone']
    channel_collection = db['channels']
    #j= channel_collection.countDocuments( { channel_id: st.session_state.id} )
    #print(j)
    #if(j>0):
    #if(channel_collection.find({'channel_id':st.session_state.id}).count() > 0):
       # st.write("Channel details already existed")


   # for doc in channel_collection.find({'channel_id':st.session_state.id},{'_id':0}):
      #if doc =={}:
          #print("1")

         # break;
    #print(existed)
    #if channel_id==existed:
          # st.write("Channel details already existed")
    #else:
    mongo_documents_upload(collections)
    st.info("Data uploaded into Mongo DB successfully")
    #mongo_documents_upload(collections)


# internal function called toupload docs
def mongo_documents_upload(collections):
    con = pymongo.MongoClient("mongodb://localhost:27017/")
    db = con['capstone']
    # creating newcollection 'staff' inside d7273 db
    channel_collection = db['channels']
    playlist_collection = db['playlist']
    videos_collection = db['video']
    comment_collection = db['comments']
    l = [channel_collection, playlist_collection, videos_collection, comment_collection]
    i = 0
    #for df in collections:
        #l[i].insert_many(df.to_dict('records'))
        #i = i + 1
    for df in collections:

        for index in df.index:
            l[i].insert_one(df.loc[index].to_dict())
        i = i + 1    

# FOR SQL UPLOAD

def sql_upload(data):
    channel_df,playlist_df,video_df,comments_df=convert_to_numeric(data)
    collections=[channel_df,video_df,comments_df]
    sql_connection(collections)

def convert_publish_date(published_date_string):
    # Convert the published date string to a datetime object
    published_date = datetime.strptime(published_date_string, '%Y-%m-%dT%H:%M:%SZ')
   # Convert the datetime object to a desired date format
    formatted_date = published_date.strftime('%Y-%m-%d  %H:%M:%S')
    return formatted_date
 
def sql_connection(collections):
    
# Establish a connection to the database
    con = sql.connect("jaga.db")
    print(con)
    cur = con.cursor() 
    print(st.session_state.id)
    #cur.execute("""select channel_id from channels where channel_id is 'UC5mz523fjzSZM28u1uRYW8Q' """)
    cur.execute("""select count(*) from channels where channel_id in ('st.session_state.id')  """)
   
    check=cur.fetchone()

    print(check)
    if check[0]>0:
    #if check[0]==st.session_state.id:
        st.write("channels details already transformed in to SQL Dataware house")
    else:    
         tables_list=['channels','videos','comments']

         i=0
         for table_name in tables_list:
        #insert_dataframe_to_mysql(collections[i], con, table_name)
            collections[i].to_sql(table_name, con, if_exists='append', index=False)
            con.commit()
            i=i+1
         st.success("Data uploaded into SQL DB successfully")  
    con.close()    
    
        

       
#---------------------------------------------------------------FOR HOME-----------------------------------------

if selected =='Home':
    #st.write("WELCOME TO YOUTUBE DATA HARVESTING")
    #data=[]
    channel_id=st.text_input(" :orange[Paste The Channel link]")
    channel_submit=st.button("Click here to extract Data")
    mongo=st.button("Upload to MongoDB")
    sql_up=st.button("Conversion to SQL DB")
    count=0
    if channel_submit :
      
         with st.spinner('Please Wait for it..'):

          # try:
                data= main(channel_id)#,playlist_ids
                st.info(f'#### Extracted data from :green["{data["channel details"]["channel_name"]}"] channel')
                st.json(data['channel details'])
                st.session_state.count=data
                st.session_state.id=channel_id
                print(st.session_state.id)
                # st.session_state.count='jagadeesg'
                 #print(st.session_state.count)
                 #count=1
 
           #except:
                   #st.error("Comments are disabled for this channel. Sorry! Can't extract info")    
                 #data=extracted_data       
           # st.info(f'#### Extracted data from :green["{data["channel details"]["channel_name"]}"] channel')
            #st.json(data['channel details'])
            #count=1
        # st.table(ch_details)
            #print(data['channel details'])
      
    if mongo:
          #print(data['channel details'])
          #print(st.session_state.count)
          data=st.session_state.count
                 
          with st.spinner('uploading data to MONGO DB...'):
               mongo_upload(data)
               #st.info("Data uploaded into Mongo DB successfully")
          #count=0    
   
    if sql_up:
           data=st.session_state.count
           print(data['channel details'])
           with st.spinner('uploading data to SQL DB...'):
             sql_upload(data)
             #st.success("Data uploaded into SQL DB successfully")

con = sql.connect("jaga.db")
mycursor=con.cursor()
#queries=st.button("click to select queries")

if selected == "SQL queries Q&A":
    
    st.write("## :orange[Select any question to get Insights]")
    questions = st.selectbox('Question',
    ['1. What are the names of all the videos and their corresponding channels?',
    '2. Which channels have the most number of videos, and how many videos do they have?',
    '3. What are the top 10 most viewed videos and their respective channels?',
    '4. How many comments were made on each video, and what are their corresponding video names?',
    '5. Which videos have the highest number of likes, and what are their corresponding channel names?',
    '6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?',
    '7. What is the total number of views for each channel, and what are their corresponding channel names?',
    '8. What are the names of all the channels that have published videos in the year 2022?',
    '9. What is the average duration of all videos in each channel, and what are their corresponding channel names?',
    '10. Which videos have the highest number of comments, and what are their corresponding channel names?'])
    submit=st.button("run query")
    if(submit):
         run_queries(questions)
    #queries=False
        
        
    
