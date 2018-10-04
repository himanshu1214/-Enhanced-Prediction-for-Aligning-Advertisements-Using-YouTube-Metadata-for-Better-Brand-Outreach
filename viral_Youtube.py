# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import csv as csv
import numpy as np
import datetime
import pandas as pd
import re
columns = ['video_id', 'title', ]

#Load Data from viral videos

ca_vid = pd.read_csv("C:/Users/Girijesh/Desktop/DM Docs/Project/project_data/CAvideos.csv")
gb_vds = pd.read_csv("C:/Users/Girijesh/Desktop/DM Docs/Project/project_data/GBvideos.csv",  error_bad_lines= False )
us_vid = pd.read_csv("C:/Users/Girijesh/Desktop/DM Docs/Project/project_data/USvideos.csv", error_bad_lines = False)
us_comments =pd.read_csv("C:/Users/Girijesh/Desktop/DM Docs/Project/project_data/UScomments.csv", error_bad_lines = False)
de_vid = pd.read_csv("C:/Users/Girijesh/Desktop/DM Docs/Project/project_data/DEvideos.csv", error_bad_lines =False)
gb_comments = pd.read_csv("C:/Users/Girijesh/Desktop/DM Docs/Project/project_data/GBcomments.csv", error_bad_lines= False)
us_vid1= pd.read_csv("C:/Users/Girijesh/Desktop/DM Docs/Project/project_data/USvideos1.csv", error_bad_lines =False)

 #print(us_vid['date'].unique())
 #print(gb_vds['date'].unique())
 
# print('')
#us_vid_head = us_vid.head()#video, title, tags, published date, caetogory_id, views, likes, dislikes, comment_total, thumbnail, date
#category
import json
with open('C:/Users/Girijesh/Desktop/DM Docs/Project/project_data/US_category_id.json') as json_data:
    d = json.load(json_data)
    category_tit= []
    category_id = []
    for row in d['items']:
        category_tit.append(row['snippet']['title'])
        category_id.append(row["id"])
        #category_tit["id"] = row["id"]
        #category_tit["title"]
        
        #Pandas
        import pandas
        us_vid1["trending_date"] = pd.to_datetime(us_vid1["trending_date"], format = "%y.%d.%m")
        us_vid1["std_trending_date"] = pd.to_datetime(us_vid1["trending_date"]).apply(lambda x:x.date().strftime('%y.%d.%m'))
        us_vid1["publish_time"] = pd.to_datetime(us_vid1["publish_time"])
        us_vid1["std_publish_time"] = pd.to_datetime(us_vid1["publish_time"]).apply(lambda x:x.date().strftime('%y.%d.%m'))
        
      

        
        us_vid1["trending_year"]   = us_vid1["trending_date"].dt.year  
        us_vid1["trending_month"]   = us_vid1["trending_date"].dt.month
        us_vid1["trending_day"] = us_vid1["trending_date"].dt.day
        us_vid1["trending_week"] = us_vid1["trending_date"].dt.dayofweek
        us_vid1["publish_year"]   = us_vid1["publish_time"].dt.year
        us_vid1["publish_month"]   = us_vid1["publish_time"].dt.month
        us_vid1["publish_day"] = us_vid1["publish_time"].dt.day
        us_vid1["publish_week"] = us_vid1["publish_time"].dt.dayofweek
        us_vid1["publish_hour"] = us_vid1["publish_time"].dt.hour
        
        # Numbering on week??
        
        day_maping= {0: 'Mon', 1:'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
        us_vid1["publish_week"] = us_vid1["publish_week"].map(day_maping)
        us_vid1["trending_week"] = us_vid1["trending_week"].map(day_maping)
        
        # Data Type for each variable 
        us_vid1.dtypes
        us_category = pd.DataFrame({"id": category_id, "title": category_tit})
        
      #Number of Tags in video:       
        x= us_vid1.loc[:, 'tags'].tolist()
        tags_lis = []
        import re
        for j in x:
            for k in j.split("\n"):
                tags_lis.append(re.sub(r"[^a-zA-Z0-9]+", ' ', k))
                
                tags_df= pd.DataFrame({"tags_n":tags_lis})
                
                tag_num = []
                for i in tags_df['tags_n']:
                    tag_num.append(len(i.split()))
                    
                    tag_num_df = pd.DataFrame({"tag_count": tag_num})
                    
                    us_vid1["tag_count"] = tag_num_df["tag_count"]
                    
                   # Days between Publish and Trending time: 
                    from datetime import datetime
                    import datetime
                #    date_format = "%y.%d.%m"
                    
                    

                    ii = []
                     for i in us_vid1["std_trending_date"]:
                         ii.append(datetime.datetime.strptime(i, date_format))
                     jj = [] 
                     for j in us_vid1["std_publish_time"]:
                         jj.append(datetime.datetime.strptime(j, date_format))
                           
                             
                             cc= []  
                           
                           for k in range(len(ii)):
                               cc.append(ii[k] -jj[k])
                               us_vid1["no_of_days"] = cc
                             
                             no_days= pd.DataFrame({"days_between": cc})
                             
                            #Below code works fine
                us_vid1["no_days"] = us_vid1.trending_date.sub(us_vid1.publish_time, axis=0)
                us_vid1["no_days"] = us_vid1["no_days"].dt.days
                us_vid1.loc[us_vid1["no_days"]== -1  ,'no_days']= 1
                us_vid1.loc[us_vid1["no_days"]== 0  ,'no_days']= 1
                            
                                # Average Views over time:
                                us_vid1["view_rate"]=us_vid1["views"]/us_vid1["no_days"]
                                # Average Likes Over Time:
                                us_vid1["view_rate"]=us_vid1["likes"]/us_vid1["no_days"]    
                                #Average Dislikes over time:    
                                us_vid1["view_rate"]=us_vid1["views"]/us_vid1["no_days"]
                                    
                          us_vid1.descreiption = us_vid1.description.astype(str)          
                            
                 
                            
                    in_links = []        
                    in_links_count = []
                    for tags in us_vid1["description"]:
                        try:
                            in_links.append(re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', tags))
                            in_links_count.append(len(re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', tags)))
                        
                        except  TypeError:
                             in_links.append(0)
                             in_links_count.append(0)
                           us_vid1["in_links"]=pd.DataFrame(in_links) #this doesnt work
                           us_vid1["in_links_count"]=pd.DataFrame(in_links_count)
                           
                           
                from numpy  import inf
                
               
               channel_view_avg = pd.DataFrame(us_vid1.groupby('channel_title', as_index = False)['view_rate'].mean())
               channel_view_avg = channel_view_avg.sort_values('view_rate', ascending = False)
                #groupby(['channel_title','view_rate'], as_index=False).mean()
                #channel_view_avg.loc[channel_view_avg['view_rate']== inf,'view_rate']= 200000000
                
                del channel_view_avg[False]
                
                for i in range(1,10):
                 c_max = int(channel_view_avg.view_rate.max()) mvr)
                 c_min = int(channel_view_avg.view_rate.min())
                mvr_diff = int((channel_view_avg.view_rate.max()-channel_view_avg.view_rate.min())/500)
                   bins= [] 
                   labels = []
                for x in range(0,500):
                    {
                            
                        labels.append(x)    
                            
                            }
                   # bins = np.arrange(0,channel_view_avg.view_rate.max(),  )
                    
                    bins=np.arange(c_min,c_max,mvr_diff)

                    
                channel_view_avg['channel_score']=pd.cut(channel_view_avg['view_rate'],bins=bins, labels= labels)
                
                
                channel_view_avg[channel_view_avg['channel_score'].isnull()] = 500

                
                channel_view_avg.view_rate.median()
                
                channel_dict=dict(zip(channel_view_avg.channel_title, channel_view_avg.channel_score))
                us_vid1["channel_score"]=us_vid1["channel_title"].map(channel_dict)
                
                