
# coding: utf-8

# # Prepare Data for Mapping Purpose 

# ## Connect to Yelp's Fusion API 

# In[1]:

import pandas as pd
import requests
app_id = 'NHD_-c5OUfJMGx-jKoObQQ'
app_secret = 'lpnJLuvVlWhnJFTjAfsbpDUCDW3KQ0uWFm5B05Qbepie6FKeksSGWrmP9G889KC1'
data = {'grant_type': 'client_credentials',
        'client_id': app_id,
        'client_secret': app_secret}
token = requests.post('https://api.yelp.com/oauth2/token', data=data)
access_token = token.json()['access_token']


# In[2]:

from matplotlib.cm import viridis
from matplotlib.colors import to_hex
import gmaps
import gmaps.datasets
import gmaps.geojson_geometries
#configuration 
gmaps.configure(api_key="AIzaSyAiDPUmhlpr5hYz1nop2SPG_XYzxnw-8P8") # Your Google API key


# ## Search Fuction 

# In[3]:

def search_business(offset, category, price, is_closed):
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'bearer %s' % access_token}
    params = {'location': 'New York City',
              'term': 'Restaurant',
              #'pricing_filter': '1, 2',
              #'sort_by': 'rating',
              'offset': str(offset),
              'limit': '50'
             }
    if (category!="all"):
        params['categories']=category
    if (price!="all"):
        params['price']=price
    if (is_closed!="all"):
        params['open_at']=is_closed
    #print (params)

    response = requests.get(url=url, params=params, headers=headers)
    return (response.json())['businesses']


# In[4]:

import numpy as np
def Search_result(category, price, is_closed):
    offset_list=np.arange(0, 1000, 50)
    response=[]
    for offset in offset_list:
        response.append(pd.DataFrame(search_business(offset, category, price, is_closed)))
    return pd.concat(response, ignore_index=True)


# In[10]:

def coordinates(dataset):
    result=[]
    for coordinate in dataset["coordinates"]:
        result.append((coordinate["latitude"], coordinate["longitude"]))
    return result


# ## Fetch Data using Yelp's API and fuction defined above 

# In[24]:

import time
categories_Chinese=["chinese", "japanese", "indian","korean","french", "italian",  "mexican"]
price_list=['1', '2', '3', '4']
is_closed_list=[int(time.time())]
search_result={}
for category in categories_Chinese:
    for price in price_list:
        for is_closed in is_closed_list:
            #print (category, price, is_closed)
            search_result[category+price+str(is_closed)]=Search_result(category, price, is_closed)

for category in categories_Chinese:
    for price in price_list:      
        search_result[category+price+"all"]=Search_result(category, price, "all")
for is_closed in is_closed_list:
    for price in price_list:
        search_result["all"+price+str(is_closed)]=Search_result("all", price, is_closed)
for category in categories_Chinese:
    for is_closed in is_closed_list: 
        search_result[category+"all"+str(is_closed)]=Search_result(category, "all", is_closed)
search_result["all"+"all"+"all"]=Search_result("all", "all", "all")


# # Visualization

# ## Mapping Fuction 

# In[38]:

from IPython.display import display
def Map_marker(category, price, is_closed):
    if (is_closed=="open"):
        is_closed=str(is_closed_list[0])


    fig = gmaps.figure()
    if (Plot_marker_info_map(fig, category, price, is_closed)==-1):
        return "There is no restaurants that you asked for"
    display(fig)


# ## Pie Figure Function

# In[32]:

def Pie_marker(category, price, is_closed):
    if (is_closed=="open"):
        is_closed=str(is_closed_list[0])
    #fig = gmaps.figure()
    business_info=search_result[category+price+str(is_closed)]
    if (len(business_info)==0):
        return "There is no restaurants that you asked for"
    Result_df=business_info.groupby("rating").count().reset_index()
    ratinglabel=list(Result_df["rating"])
    count=list(Result_df["categories"])
    pie_chart = pygal.Pie()
    pie_chart.title = "Restaurtant's rating percentage"
    for i in range(0, len(ratinglabel)):
        pie_chart.add(str(ratinglabel[i]), count[i])
    galplot(pie_chart) 


# In[33]:

import pygal 
base_html = """
<!DOCTYPE html>
<html>
  <head>
  <script type="text/javascript" src="http://kozea.github.com/pygal.js/javascripts/svg.jquery.js"></script>
  <script type="text/javascript" src="https://kozea.github.io/pygal.js/2.0.x/pygal-tooltips.min.js""></script>
  </head>
  <body>
    <figure>
      {rendered_chart}
    </figure>
  </body>
</html>
"""
def galplot(chart):
    rendered_chart = chart.render(is_unicode=True)
    plot_html = base_html.format(rendered_chart=rendered_chart)
    display(HTML(plot_html))


# ## combine two figure together 

# In[34]:

def all_marker(category, price, is_closed):
    Map_marker(category, price, is_closed)
    Pie_marker(category, price, is_closed)


# In[39]:

categories_Chinese=["chinese", "japanese", "indpak","korean","french", "italian",  "mexican", "all"]
price_list=["1", "2", "3", "4", "all"]
is_closed_list_=["open", "all"]
from ipywidgets import interact
interact(all_marker, category=categories_Chinese, price=price_list, is_closed=is_closed_list_);
##interact(Pie_marker, category=categories_Chinese, price=price_list, is_closed=is_closed_list);
from IPython.display import HTML

HTML('''<script>
code_show=true; 
function code_toggle() {
 if (code_show){
 $('div.input').hide();
 } else {
 $('div.input').show();
 }
 code_show = !code_show
} 
$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()"><input type="submit" value="Click here to toggle on/off the raw code."></form>''')#


# In[ ]:




# # Pyplot

# In[5]:

import pandas as pd
import pygal as pg
from IPython.display import display, HTML
from pygal.style import DarkStyle, NeonStyle, BlueStyle, DarkGreenStyle, LightColorizedStyle
import numpy as np
import matplotlib.pyplot as plt

### setting up the HTML with the necessary javascript and chart svg 
base_html = """
<!DOCTYPE html>
<html>
  <head>
  <script type="text/javascript" src="http://kozea.github.com/pygal.js/javascripts/svg.jquery.js"></script>
  <script type="text/javascript" src="https://kozea.github.io/pygal.js/2.0.x/pygal-tooltips.min.js""></script>
  </head>
  <body>
    <figure>
      {rendered_chart}
    </figure>
  </body>
</html>
"""

def galplot(chart):
    rendered_chart = chart.render(is_unicode=True)
    plot_html = base_html.format(rendered_chart=rendered_chart)
    display(HTML(plot_html))
    
data = pd.read_csv("F:/Study/study/Programming for Data Science/Project/Restaurant_df_1007.csv")


# # Plot average rating and price by categories

# In[6]:

from pygal.style import Style


data['price'] = data['price'].str.len()   # convert $ to number
index = ['cat', 'price', 'rating']
clean_data = data[index]
avg_data = clean_data.groupby('cat').mean()
avg_data


# Interactive Bar Chart
custom_style = Style(label_font_size = 15.0, major_label_font_size = 15)

ibar_chart = pg.Bar(x_title = 'Restaurant Categories',style = custom_style)
ibar_chart.title = 'Restarants'
ibar_chart.x_labels = ['Chinese', 'French', 'Indian', 'Italian', 'Japanese', 'Korean', 'Mexican']


for cols in avg_data.columns:
    ibar_chart.add(cols,avg_data[cols])

galplot(ibar_chart)   ### display pygal in Jupyter notebook


ibar_chart.render_to_file('chart.svg')


# # Plot rating overall by price

# ### Higher price lead to higher rating

# In[7]:

p_r = clean_data.groupby('price').mean()
p_r


# In[6]:

custom_style = Style(label_font_size = 15.0, major_label_font_size = 15)

bar_chart = pg.Bar(x_label_rotation=20, title=u'Rating by Price', x_title = 'Price', y_title = 'Rating',style = custom_style)
bar_chart.x_labels = '$','$$','$$$','$$$_$'     
bar_chart.add("rating",list(p_r['rating']))

galplot(bar_chart) 


# # Plot price overall by rating

# ## No obvious trend 

# In[8]:

r_p = clean_data.groupby('rating').mean()
r_p


# In[8]:

r_p.index


# In[9]:

custom_style = Style(label_font_size = 15.0, major_label_font_size = 15)

bar_chart = pg.Bar(title=u'Price by rating', x_title = 'Rating', y_title = 'Price', style = custom_style)

bar_chart.x_labels = list(r_p.index)   
bar_chart.add("Price",list(r_p['price']))

galplot(bar_chart) 


# # SolidGauge

# In[10]:

clean_data.groupby(['rating']).size()


# In[11]:


gauge = pg.SolidGauge(inner_radius=0.70)


gauge.add('price$/total', [{'value': 1339, 'max_value':5501}])
gauge.add('price$$/total', [{'value': 3072, 'max_value': 5501}])
gauge.add('price$$$/total', [{'value': 472, 'max_value': 5501}])
gauge.add('price$$$_$/total', [{'value': 111, 'max_value': 5501}])

                               
# gauge.add('rating [0,1)/total', [{'value': 161, 'max_value': 5501}])
# gauge.add('rating [1,2)/total', [{'value': 18 + 15, 'max_value': 5501}])
# gauge.add('rating [2,3)/total', [{'value': 60 + 190, 'max_value': 5501}])
# gauge.add('rating [3,4)/total', [{'value': 583 + 1528, 'max_value': 5501}])
# gauge.add('rating [4,5)/total', [{'value': 2020 + 747, 'max_value': 5501}])
# gauge.add('rating 5/total', [{'value': 179, 'max_value': 5501}])                               
                               
galplot(gauge)


# # Average Rating by Categories by price

# In[12]:

r_cp = clean_data['rating'].groupby([clean_data['cat'],clean_data['price']]).mean()
r_cp = pd.DataFrame(r_cp)
r_cp
r_cp = r_cp.reset_index(level=['cat', 'price'])

### lan de xie xun huan le 

# total_by_cat = r_cp[r_cp['cat'] == 'chinese']['rating'].sum()
# rating_perc = r_cp[r_cp['cat'] == 'chinese']['rating']/total_by_cat

# total_by_cat = r_cp[r_cp['cat'] == 'french']['rating'].sum()
# rating_perc = rating_perc.append(r_cp[r_cp['cat'] == 'french']['rating']/total_by_cat)

# total_by_cat = r_cp[r_cp['cat'] == 'indpak']['rating'].sum()
# rating_perc = rating_perc.append(r_cp[r_cp['cat'] == 'indpak']['rating']/total_by_cat)

# total_by_cat = r_cp[r_cp['cat'] == 'italian']['rating'].sum()
# rating_perc = rating_perc.append(r_cp[r_cp['cat'] == 'italian']['rating']/total_by_cat)

# total_by_cat = r_cp[r_cp['cat'] == 'japanese']['rating'].sum()
# rating_perc = rating_perc.append(r_cp[r_cp['cat'] == 'japanese']['rating']/total_by_cat)

# total_by_cat = r_cp[r_cp['cat'] == 'korean']['rating'].sum()
# rating_perc = rating_perc.append(r_cp[r_cp['cat'] == 'korean']['rating']/total_by_cat)


# total_by_cat = r_cp[r_cp['cat'] == 'mexican']['rating'].sum()
# rating_perc = rating_perc.append(r_cp[r_cp['cat'] == 'mexican']['rating']/total_by_cat)
# rating_perc 

# r_cp['rating_perc'] = rating_perc 
# r_cp


# In[13]:

custom_style = Style(label_font_size = 15.0, major_label_font_size = 15)

bar_chart = pg.Bar(x_title = 'Restaurant Categories', y_title = 'Rating', style = custom_style)
bar_chart.title = 'Restarants rating by categories by price'
bar_chart.x_labels = ['Chinese', 'French', 'Indian', 'Italian', 'Japanese', 'Korean', 'Mexican']


# bar_chart.add('price = $',list(r_cp[r_cp['price'] == 1].rating_perc))
# bar_chart.add('price = $$',list(r_cp[r_cp['price'] == 2].rating_perc))
# bar_chart.add('price = $$$',list(r_cp[r_cp['price'] == 3].rating_perc))
# bar_chart.add('price = $$$_$',list(r_cp[r_cp['price'] == 4].rating_perc))


bar_chart.add('price = $',list(r_cp[r_cp['price'] == 1].rating))
bar_chart.add('price = $$',list(r_cp[r_cp['price'] == 2].rating))
bar_chart.add('price = $$$',list(r_cp[r_cp['price'] == 3].rating))
bar_chart.add('price = $$$_$',list(r_cp[r_cp['price'] == 4].rating))

galplot(bar_chart) 


# # Average Price by Categories by rating

# In[13]:


## Delete row = 2839 and row = 3615 since only one french restaurant with rating = 1.5 and only one italian restaurant
## with rating = 2

# clean_data['cat'] == 'french'
# new = clean_data[clean_data['cat'] == 'french']
# new[new['rating'] == 1.5]


new = clean_data.drop([2839,3615], axis = 0)


p_cr=new['price'].groupby([new['cat'],new['rating']]).mean()
p_cr = pd.DataFrame(p_cr)
p_cr = p_cr.reset_index(level = ['cat', 'rating'])
# p_cr[head]



# new = clean_data[clean_data['cat'] == 'italian']

# new[new['rating'] == 2]


# In[14]:

custom_style = Style(label_font_size = 15.0, major_label_font_size = 15)

bar_chart = pg.Radar(x_title = 'Restaurant Categories', y_title = 'Price', style = custom_style, range=(0, 3))
bar_chart.title = 'Restarants price by categories by rating'
bar_chart.x_labels = ['Chinese', 'French', 'Indian', 'Italian', 'Japanese', 'Korean', 'Mexican']


bar_chart.add('rating = 0',list(p_cr[p_cr['rating'] == 0].price))
bar_chart.add('rating = 1',list(p_cr[p_cr['rating'] == 1].price)) 
bar_chart.add('rating = 1.5',list(p_cr[p_cr['rating'] == 1.5].price))  
bar_chart.add('rating = 2',list(p_cr[p_cr['rating'] == 2].price))
bar_chart.add('rating = 2.5',list(p_cr[p_cr['rating'] == 2.5].price))
bar_chart.add('rating = 3',list(p_cr[p_cr['rating'] == 3].price))
bar_chart.add('rating = 3.5',list(p_cr[p_cr['rating'] == 3.5].price))
bar_chart.add('rating = 4',list(p_cr[p_cr['rating'] == 4].price))
bar_chart.add('rating = 4.5',list(p_cr[p_cr['rating'] == 4.5].price))
bar_chart.add('rating = 5',list(p_cr[p_cr['rating'] == 5].price))


galplot(bar_chart) 


# # Trend Analysis price vs rating by restaurant categories

# In[56]:

p_cr = p_cr.dropna()

p_cr['rating_price'] = p_cr[['rating', 'price']].apply(tuple, axis=1)
chi_list = list(p_cr[p_cr['cat']=='chinese']['rating_price'])
ita_list = list(p_cr[p_cr['cat']=='italian']['rating_price'])
ind_list = list(p_cr[p_cr['cat']=='indpak']['rating_price'])
mex_list = list(p_cr[p_cr['cat']=='mexican']['rating_price'])
kor_list = list(p_cr[p_cr['cat']=='korean']['rating_price'])
fre_list = list(p_cr[p_cr['cat']=='french']['rating_price'])
jan_list = list(p_cr[p_cr['cat']=='japanese']['rating_price'])
# new_list = list(p_cr['rating_price'])


# In[61]:

custom_style = Style(label_font_size = 15.0, major_label_font_size = 15)

xy_chart = pg.XY(stroke= True, x_title = 'Rating', y_title = 'Price', style = custom_style)
xy_chart.title = 'price vs rating by categories'

xy_chart.add('chinese', chi_list)
xy_chart.add('italian', ita_list)
xy_chart.add('indian', ind_list)
xy_chart.add('mexican', mex_list)
xy_chart.add('korean', kor_list)
xy_chart.add('french', fre_list)
xy_chart.add('janpanese', jan_list)

galplot(xy_chart) 

