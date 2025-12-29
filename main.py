import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime

#设置可视化字体
plt.rcParams['font.sans-serif'] = 'SimSun'
#防止负号在可视化中显示方框
plt.rcParams['axes.unicode_minus'] = False

#导入数据
df = pd.read_csv(r"E:\电商RFM模型\user_info\user_info.csv")


'''1.数据预处理'''

#--删除缺失值
df.drop(index=df[df['order_count'].isnull()].index, inplace=True)
df.drop(index=df[df['total_amount'].isnull()].index, inplace=True)

#--删除异常值

#删除订单数为负的值
df.drop(index=df[df['order_count']<0].index, inplace=True)
#删除金额为负数的值
df.drop(index=df[df['total_amount']<0].index, inplace=True)

#--删除重复值
df.drop(index=df[df['uid'].duplicated()].index, inplace=True)


'''2.计算RFM的值并进行描述性分析'''

#F与M可直接使用数据集中的'order_count'列与'total_amount'列
#--获取计算"R"指标的数据
#转换数据类型方便计算
df['last_order_date'] = pd.to_datetime(df['last_order_date'])

#设置截止时间（本数据集为2019年4月前的数据集）
endTime = datetime(2019,4,1)

#计算最后一次购买的时间距离截止日期的时间间隔
df['time_gap'] = endTime - df['last_order_date']
#获得R(去除单位)
df['time_gap'] = df['time_gap'].dt.days

#--对R、F、M进行描述性分析
#获取总数
s = df['uid'].count()

#--对R进行描述性分析
R = df['time_gap'].groupby(df['time_gap']).count()
R_percent = R / s
#绘制"R"柱状图
plt.subplot(1,3,1)
plt.bar(R_percent.index, R_percent.values)
plt.title('R（最近消费间隔分布）')


#--对F进行描述性分析
F = df['order_count'].groupby(df['order_count']).count()
F_percent = F / s
#绘制"F"柱状图
plt.subplot(1,3,2)
plt.bar(F_percent.index, F_percent.values)
plt.title("F（消费频次分布）")


#--对M进行描述性分析
M = df['total_amount']
#绘制"M"直方图
plt.subplot(1,3,3)
plt.hist(M, bins=100)
plt.title("M（消费金额分布）")

#可视化R、F、M
plt.show()

'''3.搭建RFM模型'''

#--对RFM进行切分, 防止重复值过多报错
df['R'] = pd.qcut(df['time_gap'], q=3, labels=[3,2,1], duplicates='drop')
df['F'] = pd.qcut(df['order_count'], q=3,labels=[1,2,3], duplicates='drop')
df['M'] = pd.qcut(df['total_amount'],q=3,labels=[1,2,3], duplicates='drop')

#--根据RFM进行分层

#定义分层函数
def rfmTrans(x):
    x_int = int(x)
    if x_int > 2:
        return 1
    else:
        return 0
    
#使用apply函数，对RFM进行分层
df['R'] = df['R'].apply(rfmTrans)
df['F'] = df['F'].apply(rfmTrans)
df['M'] = df['M'].apply(rfmTrans)

#结合RFM的分层结果对用户进行分层
df['mark'] = df['R'].astype(str) + df['F'].astype(str) + df['M'].astype(str)

#分层
def rfmTypes(x):
    if x == '111':
        return '高价值用户'
    elif x == '101':
        return '重点发展用户'
    elif x == '011':
        return '重点唤回用户'
    elif x == '001':
        return '重点潜力用户'
    elif x == '110':
        return '一般潜力用户'
    elif x =='100':
        return '一般发展用户'
    elif x == '010':
        return '一般用户'
    else:
        return '低价值用户'
    
#最终分层结果
df['customer_type'] = df['mark'].apply(rfmTypes)

#可视化分层结果
df_type = df['customer_type'].groupby(df['customer_type']).count()

df_perc = df_type / s

plt.bar(df_type.index, df_type.values)
plt.xlabel('用户分层类别')
plt.ylabel('各层级用户总数')
#旋转x轴标签，避免重叠
plt.xticks(rotation=45)

#绘制双y轴图
plt.twinx()

plt.plot(df_perc.index, df_perc.values, marker='o', color='green')
plt.ylabel('各层级用户总数占比')

plt.show()

print("=== RFM用户分层统计结果 ===")
print("各层级用户数量：")
print(df_type)
print("\n各层级用户占比（%）：")
print((df_perc * 100).round(2))