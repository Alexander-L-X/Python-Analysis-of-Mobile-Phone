import pandas as pd
from mpl_toolkits.basemap import Basemap
import numpy as np
import matplotlib.pyplot as plt
app_events = pd.read_csv('app_events.csv')
app_labels = pd.read_csv('app_labels.csv')
label_categories = pd.read_csv('label_categories.csv')
events = pd.read_csv('events.csv')
times = events['timestamp'].values
longitudes = events['longitude'].values
latitudes = events['latitude'].values
dates = {}
dates1 = {}
time_span = {}
time_span1 = {}
longitudes_dic = {}
latitudes_dic = {}
long_la_dic = {}
lon=[]
lat=[]
for i in times:
    value = i.split(' ')
    date = value[0]
    date2int = int(date.replace('-',''))
    hour = value[1].split(':')[0]
    hour1 = int(hour)
    hour = hour + '~' + str(int(hour) + 1)
    dates[date] = 1 + dates.get(date, 0)
    time_span[hour] = 1 + time_span.get(hour, 0)
    time_span1[hour1] = 1 + time_span1.get(hour1, 0)
    dates1[date2int] = 1 + dates1.get(date2int, 0)
for index in range(len(longitudes)):
    i,j = int(longitudes[index]),int(latitudes[index])
    if i==0 and j==0:
        continue
    long_la = str(i) + ',' + str(j)
    long_la_dic[long_la] = 1 + long_la_dic.get(long_la, 0)
    lon.append(i)
    lat.append(j)

dates = sorted(dates.items(),key = lambda x:x[1],reverse = True)
dates1 = sorted(dates1.items(),key = lambda x:x[0])
dates = pd.DataFrame(dates,columns = ['使用日期','当天使用量'])
dates1 = pd.DataFrame(dates1,columns = ['使用日期','当天使用量'])
print('使用App最活跃的日期及当天App使用量情况为：\n',dates)

hours = sorted(time_span.items(),key = lambda x:x[1],reverse = True)
hours1 = sorted(time_span1.items(),key = lambda x:x[0])
hours = pd.DataFrame(hours,columns = ['时间段（小时）','每个时间段使用量'])
print('使用App最活跃的时间段及每个时间段使用量情况为：\n',hours)

hours1 = pd.DataFrame(hours1,columns = ['时间段（小时）','每个时间段使用量'])
long_la_dic = sorted(long_la_dic.items(),key = lambda x:x[1],reverse = True)
long_la_dic = pd.DataFrame(long_la_dic,columns = ['纬度，经度','该地区使用量'])
print('使用App最活跃地区及该地区范围使用量情况为：\n',long_la_dic)

# 画时间峰值图
a = []
x = []
for i in hours1['时间段（小时）']:
    x.append(str(i)+'~'+str(i+1))
y=hours1['每个时间段使用量'].values.tolist()
for value in dates1['使用日期'].values.tolist():
    value = list(str(value))
    value.insert(4, '-')
    value.insert(7, '-')
    a.append(''.join(value))
b=dates1['当天使用量'].values.tolist()

# 时间
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
p1 = plt.figure(figsize=(9,9))
ax1 = p1.add_subplot(2,1,1)
plt.title('各时间段活跃量')
plt.ylabel('活跃人数')
plt.xlabel('时间段')
plt.xticks(rotation = 45)
plt.plot(x,y,'ro-',lw=3,color = 'g')
plt.bar(x,y,color='b')
# 日期
ax2 = p1.add_subplot(2,1,2)
plt.title('各日期活跃量')
plt.ylabel('活跃人数')
plt.xlabel('日期')
plt.bar(a,b,color='k')
plt.show()

label_categories.dropna(axis = 0,how = 'any',inplace = True)
label_id = label_categories['label_id']
category = label_categories['category']
categories = pd.DataFrame(category,index = label_id,columns = ['category'])
app_id = app_events.groupby('app_id')['is_active'].sum()
app_popular = app_id.sort_values(ascending = False).head()
popular = {}
for i in app_popular.index:
    for j in range(len(app_labels['app_id'])):
        if i == app_labels.loc[j,'app_id']:
            label_id = app_labels.loc[j,'label_id']
            popular[i] = categories.loc[label_id,'category']
            break
print('排名前五的app_id及category是：')
for i in popular.items():
    print(i)

# 画地图

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
m = Basemap(width = 10000000000,height = 10000000000)  # 实例化一个map
m.drawcoastlines(linewidth=0.25)  # 画海岸线
m.drawstates(linewidth=0.25, color='m') #画出州界线
m.drawcountries(linewidth=0.25, color='g')# 画出国境线
m.drawmapboundary(fill_color = 'aqua') #整个地球蓝色
#m.fillcontinents(color = 'coral', lake_color = 'aqua') #大陆棕色江河海为蓝色
#m.shadedrelief()# 绘制阴暗的浮雕图
parallels = np.arange(-90., 90., 10.)  # 画纬度，范围为[-90,90]间隔为10
m.drawparallels(parallels, labels=[False, True, True, False],fontsize=5)
meridians = np.arange(-180., 180., 20.)  # 经度，范围为[-180,180]间隔为10
m.drawmeridians(meridians, labels=[True, False, False, True],fontsize=5)

# 绘制区域使用点图

lon, lat = m(lon, lat)
m.scatter(lon, lat, s=5,marker = '.', color = 'r')
plt.title('App使用区域图')
plt.savefig('map.png', dpi=1000)
plt.show()

