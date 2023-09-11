                     
                     PROJECT TITLE:    YouTube-Data-Harvesting-and-Warehousing-using-MongoDB, SQL-and-Streamlit application.

Problem Statement:  Create a streamlit App which allows users to extract data from youtube api v3 (channels,videos,comments data)
                         and store data in MONGO DB and SQL datawarehouse for further analysis. Built an Q&A dropdown where user can
                         analyse the important metrics about  their channels and videos performance.


              PROJECT DONE BY: JAGADEESH BUSAYAVALASA (certified in MASTERS IN DATASCIENCE from GUVI IIT collabaration)
              PROJECT DOMAIN : DATA SCIENCE & ANALYTICS



DEMO VIDEO URL: https://www.youtube.com/watch?v=BKJXhXDjDuA

LINKED IN URL : https://www.linkedin.com/posts/samuel-solomon-116884244_youtube-data-harvesting-and-warehousing-activity-7076940665137332224-2oYd?utm_source=share&utm_medium=member_desktop

The application consists following features: 

1.Display some Metrics like number of channels available in DB,Channel with highest subscribers, Most liked video etc on Home page.

2. Retrieving all the required channel data (Channel name, subscribers, total videos count, playlist ID, video ID,Views, likes, dislikes,  comments of each video) just by entering channel id using Google API Key for authentication purpose.

3. After retrieving data user can store data in mongodb using "UPLOAD MONGODB" function  as a datalake.
 
4. Option to migrate the channel data  from the data lake to a SQL database as tables just by clicking SQL upload function. 

5. Ability to select 10 important questions and get meaninful metrics useful for EVALUATION & ANALYSIS of channel performance.

6. User can select 10 questions from RUN Queries section and get answers from SQL database.

Requirements:

$ Google API Developer console:  You can use the Google API client library for Python to make requests to the Youtube API V3 by enabling API in Google developer console. 

$ Pandas : Python library to preprocess the data and before uploading data into  Mongo DB data lake.

$ MongoDB data lake: Once you retrieve the data from the YouTube API in JSON, you can store it in a MongoDB data lake by preprocessing data using pandas library. MongoDB is a great choice for a data lake because it can handle unstructured and semi-structured data easily. 

$ SQL data warehouse: After you've collected data for channel, you can migrate it to a SQL data warehouse. You can use any SQL database such as MySQL or PostgreSQL for this. 

$ Streamlit: we can use streammilt library for front end ui purpose which allows user to interact with backend API's or functionalities.

Overall, this approach involves building a simple UI with Streamlit, retrieving data from the YouTube API using python, storing it in a MongoDB data lake, migrating it to a SQL data warehouse, querying the data warehouse with SQL, and displaying the data in the Streamlit app.

Configuration:

1.Open the youtubedata.py file in the project directory in any IDE.

2.Set the desired configuration options:

    i. Specify your YouTube API key generated in GOOGLE developer console.

   ii.Specify the database connection details (Mongo DB & SQL)

3.Get the Youtube Channel ID any cahnnel from the Youtube's sourcepage

4.Run the streamlit application using " streamlit run youtubedata.py" (from the located path)

4.Enter the Youtube Channel ID in channel id textbox and enter it to retrieve data

5.After retrieving data please use "upload to MONGODB" to store in datawarehouse in form of collections.

6.Use SQL upload if you want to analayse data and receive metrics from sql datawarehouse.

7.Use Runqueries section to get  realational data useful for evaluating channels and videos performance with your competitors
Usage:


Any specific additional functionalities as addon are welecome from all of you!
If you want to contribute to this project, please follow these steps:

1.Fork the repository.

2.Create a new branch: "git checkout -b feature/your-feature-name"

3.Make your modifications and commit the changes: "git commit -m "Add your commit message here"

4.Push your branch: "git push origin feature/your-feature-name"

5.Open a pull request on the GitHub repository, explaining the changes you made and why they should be merged.
