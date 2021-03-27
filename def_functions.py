import os
import pandas as pd
import numpy as np
#from tqdm.notebook import tqdm
# we know that age of user are not less than zero and not greter than 100
# here we make lower threshold = 0 and upper threshold = 60.
# if age is <= 0 than put 0 , if age > 60 than put 60.
def age_replace(data):

    new_age = []
    for i in data['bd'].values:
        if i <= 0 :
            new_age.append(0)
        elif i > 60:
            new_age.append(60)
        else :
            new_age.append(i)
    data['bd'] = new_age
    return data


# we extract date , month , year from registration_init_time and expiration_date.
def get_d_m_y(sample_data):

    regi_date = sample_data['registration_init_time'].values
    expi_date = sample_data['expiration_date'].values

    day   = []
    month = []
    year  = []

    for i in regi_date:
        i = str(i)
        day.append(int(i[:4]))
        month.append(int(i[4:6]))
        year.append(int(i[6:]))
    sample_data['regi_day']   = day
    sample_data['regi_month'] = month
    sample_data['regi_year']  = year

    day   = []
    month = []
    year  = []

    for i in expi_date:
        i = str(i)
        day.append(int(i[:4]))
        month.append(int(i[4:6]))
        year.append(int(i[6:]))
    sample_data['expire_day']   = day
    sample_data['expire_month'] = month
    sample_data['expire_year']  = year

    sample_data = sample_data.drop(['expiration_date','registration_init_time'],axis =1)

    return sample_data


# function for remove columns which name start with 'Unnamed:'
def remove_funtion(data):
    for i in data.columns:
        if i.split()[0] == 'Unnamed:':
            data = data.drop(i,axis = 1)
    return data


# seprate genre_ids and make seprate columns for each genre_ids
def separate_genre(data):
    genre = data['genre_ids'].values
    genre_category  = []

    # seprate all genre and store in genre_category
    for i in genre:
        lis = []
        i = str(i)
        if '|' in i:
            sen = i.split('|')
            genre_category.append(sen)
        else:
            lis.append(i)
            genre_category.append(lis)
    # if len(genre) < 8 than fill 0 to make all len(genre) == 8        
    genre_id_list = []
    for i in genre_category:
        while len(i) < 8:
            i.append(0)
        genre_id_list.append(i)

    genre_ids = np.array(genre_id_list)

    # make seprate columns for all genre_ids 
    data['one_genre']   = genre_ids[:,0]
    data['two_genre']   = genre_ids[:,1] 
    data['three_genre'] = genre_ids[:,2]
    data['four_genre']  = genre_ids[:,3]
    data['five_genre']  = genre_ids[:,4]
    data['six_genre']   = genre_ids[:,5]
    data['seven_genre'] = genre_ids[:,6]
    data['eight_genre'] = genre_ids[:,7]

    data = data.drop('genre_ids' , axis = 1)

    return data


# make new feature : if song len < mean : 1, else: 0
def song_len(mean,sample_data):
    # we find the mean of only train data
    #mean = train_data['song_length'].mean()
    #print(mean)
    binary_feature = []
    #sample_data.head()

    song_len = sample_data['song_length'].values

    for i in song_len:
        if i < mean:
            binary_feature.append(1)
        else:
            binary_feature.append(0)
    sample_data['binary_song_length'] = binary_feature
    return sample_data


# create new feature
# if language = 3 or 52 than 1 else: 0
# we know that most song language are 3 or 52.
def like_language(sample_data):
    language = sample_data['language'].values
    like_language = []
    for i in language:
        if i == 3 or i == 52:
            like_language.append(1)
        else:
            like_language.append(0)
    sample_data['like_language'] = like_language
    return sample_data


# count how many name.name are seprate with  ['|',',','/','\\',';','、']
def count_funtion(x,zero):
    if x != zero:
        split_lis = ['|',',','/','\\',';','、']
        sum = 0
        for i in split_lis:
            sum += x.count(i)
        return sum + 1
    else:
        return 0
    

# get first name of composer
def get_composer_name(sample_data):
    composer = sample_data['composer'].values
    composer_first_name = []
    for i in (composer):
        
        special = 0
        split_lis = ['|',',','\_','/','\\',';','、']
        
        #if any value of split_lis present in i than go in.
        if any((c in split_lis) for c in i):
            #check spliting character
            for j in split_lis:
                if j in i:
                    special = j
                    composer_first_name.append(i.split(special)[0])
                    #print(i.split(special)[0])
                    break
        else:
            composer_first_name.append(i)
            #print(i)

    sample_data['composer_first_name'] = composer_first_name
    return sample_data


# get first name of artist_name
def get_artist_name(sample_data):
    artist_name = sample_data['artist_name'].values
    artist_name_first_name = []
    for i in (artist_name):
        i = str(i)
        special = 0
        split_lis = ['|',',','\_','/','\\',';','、']
        
        #if any value of split_lis present in i than go in.
        if any((c in split_lis) for c in i):
            #check spliting character
            for j in split_lis:
                if j in i:
                    special = j
                    artist_name_first_name.append(i.split(special)[0])
                    #print(i.split(special)[0])
                    break
        else:
            artist_name_first_name.append(i)
            #print(i)

    sample_data['first_artist_name'] = artist_name_first_name
    return sample_data



# funtion for extract values from isrc feature
def extract_code(c):
    if c == '0':
        return 0,0,0,0
    else:
        return c[:2],c[2:5],c[5:7],c[7:]
    
    
# extract values from isrc feature
# create 4 features
def get_isrc(sample_data):
    country_code , regi_code , year , designation_code = [],[],[],[]

    for i in sample_data['isrc'].values:
        a,b,c,d = extract_code(i)
        country_code.append(a)
        regi_code.append(b)
        year.append(c)
        designation_code.append(d)

    sample_data['country_code '] = country_code 
    sample_data['regi_code'] = regi_code
    sample_data['year'] = year
    sample_data['designation_code'] = designation_code
    return sample_data
    

# https://github.com/lystdo/Codes-for-WSDM-CUP-Music-Rec-1st-place-solution
def calculate_groupby_features(data):
    '''Function to calculate group by features on dataframe '''
    
    # song count for each user
    member_song_count = data.groupby('msno').count()['song_id'].to_dict()
    data['member_song_count'] = data['msno'].apply(lambda x: member_song_count[x])

    # song count for each artist
    artist_song_count = data.groupby('first_artist_name').count()['song_id'].to_dict()
    data['artist_song_count'] = data['first_artist_name'].apply(lambda x: artist_song_count[x])

    # song count for each lanugage
    lang_song_count = data.groupby('language').count()['song_id'].to_dict()
    data['lang_song_count'] = data['language'].apply(lambda x: lang_song_count[x])

    # user count for each song
    song_member_count = data.groupby('song_id').count()['msno'].to_dict()
    data['song_member_count'] = data['song_id'].apply(lambda x: song_member_count[x])

    # We can add group by wrt 'age'
    age_song_count = data.groupby('bd').count()['song_id'].to_dict()
    data['age_song_count'] = data['bd'].apply(lambda x: age_song_count[x])

    return data



