# Visualization and Analysis on NYC Restaurant Yelp Ratings by Price Level, Cuisine Category, and Location
Hetian Bai (hb1500), Jieyu Wang (jw4937), Zhiming Guo (zg758)

### Abstract 
Abstract—In this project, we use NYC restaurants data crawled from Yelp with its Fusion API to build an interactive interface on Python Jupyter Notebook, which filters restaurants based on its cuisine category, price and whether they are open at the time of searching or not. This interface also generates a pie graph that shows the rating composition of these restaurants. Besides, we visualize the data in an interactive way to reveal the relationships between rating, price level and locations of restaurants. By analyzing these plots, we find out that for French, Italian, and Japanese restaurants, higher-price ones tend to be higher rated. Conversely, for Chinese and Mexican restaurants, high priced restaurants tend to be poorly rated. In addition, for Indian and Korean restaurants, price factor seems to barely have an effect on the rating.
 
### I. INTRODUCTION
New York City is a world food bank. According to National Restaurant’s survey conducted in 2015[1], there are 45,681 dining and drinking locations in New York City, so there is a huge amount of food options available. For example, we may choose the food spots nearby, or make our decision based on empirical data like ratings, price, and location. In addition, we may consider by food cuisines, like Chinese, Japanese, French, Italian, etc. For this reason, we are interested to know the role of food category playing in rating, price level, and location.
 
#### Problem Formulation: 

Visualization: 
* Pin restaurant locations on Google map and briefly show restaurant profile in Jupyter Notebook using Gmap library[2].
* Create an interactive interface in Jupyter Notebook which allows users to select restaurants by cuisines, business status (opening/closing), and price levels.
* Visualize the relationships between NYC restaurants price levels, ratings, and food cuisines with various plot styles using Pygal[3].

Analysis: 
* Give interpretation of each graph to unfold the relationship between price levels, ratings, and food categories.
 
### II. METHODOLOGY
1. Using Yelps Fusion API to fetch data of restaurants by certain categories and store it in a dataframe. 

2. With packages including Pandas, Matplotlib and Numpy, we extract their locations and use Ipywidgets and Gmap to plot their locations on a Google map. Besides, we use Pygal to plot an interactive pie graph of these restaurants rating percentages.

3. Pygal library is utilized to visualize the relationships between NYC restaurants price levels, ratings, and food cuisines. The data used to plot are summarized by Pandas groupby function.

#### References:
[1] New York restaurant industry at a glance. (n.d.). Retrieved December 08, 2017, from http://www.restaurant.org/Downloads/PDFs/State-Statistics/

[2] Pbugnion. Pbugnion/Gmaps. GitHub, 11 Nov. 2017, github.com/pbugnion/gmaps./

[3] K. (2017, July 05). Kozea/pygal. Retrieved December 10, 2017, from https://github.com/Kozea/pygal/

Last updated: Dec 12th 2017
