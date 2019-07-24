import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
phone = pd.read_csv('phone_brand_device_model.csv')
gender_age_train = pd.read_csv('gender_age_train.csv')
brand_count = phone.groupby('phone_brand')['phone_brand'].count()
# print(type(brand_count))
print('市场上已有手机品牌种类数为：%d，品牌名称如下：'%len(brand_count))
for i in brand_count.index:
    print(i,end = ',')
brand_sort = brand_count.sort_values(ascending = False)
print('\n其中使用最多即最受欢迎手机品牌前五如下：\n',brand_sort.head())
model_count = phone.groupby(['phone_brand','device_model'])['device_model'].count()
# print(model_count)
print('排名前五的手机品牌版本及各型号前五使用数量排序如下：\n')
for i in brand_sort.index[:5]:
    print(model_count.loc[i,:].sort_values(ascending = False).head())

device_model_count = phone.groupby('device_model')['device_model'].count()
device_model_sort = device_model_count.sort_values(ascending = False)
print('\n最受欢迎手机设备型号使用数量前五如下long_la_dic：\n',device_model_sort.head())

labels = list(brand_sort.index[0:5])
labels.append('其它')
values = brand_sort.head().values
values = list(values)
sum = 0
for i in values:
    sum = sum+i
others_brand_count = len(phone['phone_brand'])-sum
values.append(others_brand_count)
plt.figure()
plt.subplot(2,1,1)
plt.pie(values,labels=labels,autopct='%1.1f%%',shadow=False,startangle=150)
plt.title('各手机品牌使用量所占比例')

plt.subplot(2,1,2)
plt.barh(device_model_sort.index[0:10],device_model_sort[0:10])
plt.title('最受欢迎手机设备型号使用数量前十')
plt.show()



