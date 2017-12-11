### Visualization and Analysis on NYC Restaurant Yelp Ratings by Price Level, Cuisine Category, and Location
Hetian Bai (hb1500), Jieyu Wang (jw4937), Zhiming Guo (zg758)

Abstract 
In this project, we used NYC restaurants data crawled from Yelp API to build an interactive interface on Python Jupyter Notebook to realize the filter function on Yelp website which allows users to select restaurants by restricting food categories, business status, and price levels. In addition, we visualized the data in an interactive way to reveal the relationships between rating, price level and locations of restaurants. 
 
# I. INTRODUCTION
New York City is a world food bank. According to National Restaurant's survey conducted in 2015[1], there are 45,681 dining and drinking locations in New York City, so there is a huge amount of food options available. For example, we may choose the food spots nearby, or make our decision based on empirical data like ratings, price, and location. In addition, we may consider by food cuisines, like Chinese, Japanese, French, Italian, etc. For this reason, we are interested to know the role of food category plays in rating, price level and locations. 
 
Problem Formulation: 
Visualization: 
Pin restaurant locations on Google map and briefly show restaurant profile in Jupyter Notebook using gmap library
Create interactive interface in Jupyter Notebook which allows users to select restaurant by cuisines, business status (opening/closing), and price levels
Visualize the relationships between NYC restaurant’s price levels, ratings, and food cuisines with various plot styles using pygal[2]
Analysis: 
Give interpretation on each graph to unfold the relationship between price levels, ratings, and good categories. 
 
# II. METHODOLOGY
Using Yelp’s Fusion API to fetch data of restaurants by certain categories and store it in a dataframe. 
With packages including Pandas, Matplotlib and Numpy, we extract their locations and use Ipywidgets and Gmap to plot their locations on a Google map. Besides, we use Pygal to plot an interactive pie graph of these restaurants’ rating percentages
Pygal library was utilized to visualize the relationships between NYC restaurant’s price levels, ratings, and food cuisines. The data used to plot were summarized by Pandas groupby functions. 
