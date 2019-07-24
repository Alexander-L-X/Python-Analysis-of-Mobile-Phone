import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
gender_age_train = pd.read_csv('gender_age_train.csv')
phone = pd.read_csv('phone_brand_device_model.csv')

phone_categories = phone.groupby(['phone_brand','device_model'])['phone_brand'].count()
num = 1
num1 = 0
brand_dic = {}
model_dic = {}
temp = 'E人E本'
for i in phone_categories.index:
    if temp == i[0]:
        brand_dic[i[0]] = num
        num1 += 1
        model_dic[i[1]] = num + float('0.' + str(num1))
    else:
        num1 = 1
        num+=1
        brand_dic[i[0]] = num
        model_dic[i[1]] = num + float('0.' + str(num1))
    temp = i[0]
brand2num = []
model2num = []
for i in range(len(phone['phone_brand'])):
    brand_value = phone.loc[i,'phone_brand']
    model_value = phone.loc[i,'device_model']
    brand2num.append(brand_dic[brand_value])
    model2num.append(model_dic[model_value])
phone['brand2num'] = brand2num
phone['model2num'] = model2num

connect = gender_age_train.join(phone.set_index('device_id'),on='device_id',how='left')
print('gender_age_train表与phone表根据关键字device_id连接后表如下：\n',connect.head())
connect.dropna(axis = 0,how = 'any',inplace = True)
connect.drop_duplicates(subset=['device_id'],keep='first',inplace=True)
connect.reset_index(inplace = True)
connect.drop(['index'],axis = 1,inplace = True)
gender_count = connect.groupby(['phone_brand','gender'])['phone_brand'].count()
age_count = connect.groupby(['phone_brand','age'])['phone_brand'].count()
age_dup = connect['group'].drop_duplicates()
age_group = {}
for value in age_dup:
    if value.endswith('-') or value.endswith('+'):
        age_group[value] = int(value[1:3])
    else:
        age_group[value] = int((int(value[1:3])+int(value[4:6]))/2)
ages_reset = []
for i in connect['group']:
    ages_reset.append(age_group[i])
connect['ages_reset'] = ages_reset

mi_age = age_count['小米']
count = {'10~20':0,'20~30':0,'30~40':0,'40~50':0,'50~60':0,'60~70':0,'70~80':0,'80~90':0}
for i in mi_age.index:
    value = mi_age[i]
    if i<=20:
        count['10~20'] += value
    elif 20<i<=30:
        count['20~30'] += value
    elif 30 < i <= 40:
        count['30~40'] += value
    elif 40 < i <= 50:
        count['40~50'] += value
    elif 50 < i <= 60:
        count['50~60'] += value
    elif 60 < i <= 70:
        count['60~70'] += value
    elif 70 < i <= 80:
        count['70~80'] += value
    elif 80 < i <= 90:
        count['80~90'] += value
plt.figure()
plt.subplot(2,1,1)
plt.title('小米手机男女使用比例')
plt.pie([i for i in gender_count['小米']],labels = ['女性','男性'],autopct='%1.1f%%',shadow=False,startangle=150)
plt.subplot(2,1,2)
plt.title('小米手机各年龄段使用情况')
plt.bar(count.keys(),count.values(),color = 'g')
plt.show()

label = []
for i in connect['gender']:0
    if i == 'M':
        label.append(0)
    else:
        label.append(1)
label = {'label':label[10000:20000]}
label = pd.DataFrame(label)
label1 = connect['ages_reset'][10000:20000]
data = connect[['brand2num','model2num']].iloc[10000:20000,:]
print('经过一系列处理后，connect表格最终形式如下：\n',connect.head())

train_data,test_data,train_label,test_label = train_test_split(data,label,test_size = 0.12,random_state = 10)
train_data_scaler = MinMaxScaler().fit_transform(train_data)
test_data_scaler = MinMaxScaler().fit_transform(test_data)
test_label = test_label.reset_index(drop = True)
svm = SVC().fit(train_data_scaler,train_label)
predict = svm.predict(test_data_scaler)
count = 0
for i in range(len(predict)):
    if predict[i] == test_label.loc[i,'label']:
        count+=1
print('性别预测准确率为：{:.2%}'.format(count/len(predict)))

train_data1,test_data1,train_label1,test_label1 = train_test_split(data,label1,test_size = 0.12,random_state = 10)
train_data_scaler1 = MinMaxScaler().fit_transform(train_data1)
test_data_scaler1 = MinMaxScaler().fit_transform(test_data1)
test_label1 = test_label1.reset_index(drop = True)
svm1 = SVC().fit(train_data_scaler1,train_label1)
predict1 = svm1.predict(test_data_scaler1)
count = 0
for i in range(len(predict1)):
    if predict1[i] == test_label1[i]:
        count+=1
print('年龄预测准确率为：{:.2%}'.format(count/len(predict1)))

gender_age_test = pd.read_csv('gender_age_test.csv')
test = pd.concat([gender_age_test,phone],ignore_index=True)
test.dropna(axis = 0,how = 'any',inplace = True)
data = test[['brand2num','model2num']].iloc[10000:20000,:]
data = MinMaxScaler().fit_transform(data)
result = svm.predict(data)
result1 = svm1.predict(data)
print('性别预测结果如下：\n',result)
print('年龄预测结果如下：\n',result1)