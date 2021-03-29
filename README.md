# kkbox-s-music-recommendation-challenge-case-study

We have to build a model which will predict whether a user will re-listen to that song by evaluating given features of the user and songs.Here problem is Binary Classification Problem.we will predict whether a user will re-listen that song(1) or not(0).

In this problem we use AUC Score.why?

Ex 1. let's take list of song that user listened.
list of song : s1,s2,s3,s4 
Out of list user is re-listen s1,s3 only.

let say model predict user will re-listen s1 , s3 and s4 songs.but actually user not re-listen s4.In this problem it is okay if model is making some mistake like this. what if we recommend s1,s3,s4 to user and suppose user  start listening s4 also otherwise user have next button⏭.Here small mistake does not cost anything right!

Ex 2. let say user listen s1,s2,s3,s4 and not re-listen none of them. , but model predicts user will re-listen s3.
Here also model predict something than nothing and also recommend s3 to user will not impact on user's experience.
So mistakes here are okay.Having a low specificity is fine but it is about how much mistakes we want from model to make,we focus on tradeoff between sensitivity and specificity.This can be achieved easily by AUC Score.

We collect data from kaggle. Data source link : https://www.kaggle.com/c/kkbox-music-recommendation-challenge
The data has 6 csv file.

A. train.csv : 
msno(user_id) , song_id(song id) , source_system_tab(tab name where event was triggered) , source_screen_name(name of the layout a user sees) , source_type(entry point a user first plays music on mobile apps) , target(target = 1 means user re-listen song and 0 means user not listen song again.)

B. songs.csv : song information
song_id , song_length(length of song in ms) , genre_ids(genre of song) , language(language of song) , artist_name , composer , lyricist.

C. members.csv : user information 
msno , city(city of user) , bd(age of user "feature has outlier values.") , gender(gender of user) , registered_via(registration method) , registration_init_time(%y%m%d format) , expiration_date(%y%m%d format)

D. song_extra_info.csv
song_id , song_name(name of song) , isrc(The International Standard Recording Code) , 

E. test.csv
id(id that will be used for submission) , msno , song_id , source_system_tab , source_screen_name , source_type

F. sample_submission.csv
id , target

Here is my blog link : https://medium.com/@ajayjogiyaofficial.
