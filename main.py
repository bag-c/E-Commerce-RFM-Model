import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import joblib

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

# 将R转化为正向指标（值越大越好）
df['recency_score'] = 1 / (df['time_gap'] + 1)  # +1防止除零

print("\n=== RFM描述性统计 ===")
print(f"近度范围：{df['time_gap'].min()} - {df['time_gap'].max()} 天")
print(f"频次范围：{df['order_count'].min()} - {df['order_count'].max()} 次")
print(f"金额范围：{df['total_amount'].min():.2f} - {df['total_amount'].max():.2f} 元")

'''3.搭建RFM模型'''
#使用K-means算法进行聚类

#对R、F、M进行归一化
features = ['recency_score', 'order_count', 'total_amount']
x = df[features].values

#构建模板
scaler = StandardScaler()

#对x进行归一化
x_scaler = scaler.fit_transform(x)

#设置空列表，用来存储SSE值（簇内误差平方和）
sseList = []

#使用’肘部法则计算最优K值‘
for K in range(2,7):
    test_kmeans = KMeans(n_clusters=K, random_state=1, n_init=10)
    #训练模型
    test_kmeans.fit(x_scaler)
    sseList.append(test_kmeans.inertia_)

plt.plot(range(2,7), sseList, marker='o')
plt.xlabel('聚类数K')
plt.ylabel('SSE (簇内误差平方和)')
plt.title('肘部法则')
plt.show() 

#找到最优k值,构建K-Means聚类模型
k=3
model = KMeans(n_clusters=3, random_state=1, n_init=10)
model.fit(x_scaler)

#获取分类结果
labels = model.labels_
df['customer_type'] = labels

# 评估模型：轮廓系数（值越接近1越好）
score = silhouette_score(x_scaler, labels)
print(f'K-means模型轮廓系数：{score:.3f}')

'''分群结果分析'''

segment_std = df.groupby('customer_type').agg({
    'uid':'count',
    'recency_score':'mean',
    'order_count':['mean', 'max'],
    'total_amount':['mean', 'sum']
}).round(2)

segment_names = {
    0: '高价值活跃用户',
    1: '中等价值用户', 
    2: '低价值沉默用户'
}
df['segment_name'] = df['customer_type'].map(segment_names)

# 美化输出
segment_std.columns = ['用户数', '平均间隔(天)', '平均频次', '最高频次', '平均金额', '总金额']
segment_std['占比%'] = (segment_std['用户数'] / len(df) * 100).round(1)

print("\n=== 用户分群详细统计 ===")
print(segment_std)

# 各分群RFM特征对比
print("\n=== 各分群RFM特征对比 ===")
rfm_means = df.groupby('segment_name')[['recency_score', 'order_count', 'total_amount']].mean().round(3)
print(rfm_means)

'''可视化结果'''
#创建画布
fig = plt.figure(figsize=(12,8))

#创建3d坐标
ax = fig.add_subplot(projection='3d')

#设置颜色
color = ['red', 'green', 'blue']
center_color = ["pink", 'yellow', 'black']

#遍历3个簇
for i in range(3):
    d = df[df['customer_type'] == i]
     #绘制分类为i的簇所对应的R、F和M这三个指标数据
    ax.scatter(d['recency_score'], d['order_count'], d['total_amount'], color=color[i], label=f'用户群体{i}')
    #标记中心的位置
    center = d[['recency_score', 'order_count', 'total_amount']].mean()
    ax.scatter(center.iloc[0], center.iloc[1], center.iloc[2], color=center_color[i], label=f'中心{i}')

#设置R、F、M标题
ax.set_xlabel('R - 近度得分\n(1/(间隔天数+1))', fontsize=11)
ax.set_ylabel('F - 消费频次\n(订单数)', fontsize=11)
ax.set_zlabel('M - 消费金额\n(总消费额)', fontsize=11)
ax.set_title('RFM用户智能分群3D可视化\n(每个X标记表示簇中心)', fontsize=14)

plt.legend(loc='upper left',fontsize=10)

plt.show()

'''业务建议与模型保存 '''
print("\n" + "="*50)
print("业务策略建议")
print("="*50)

strategy_advice = {
    '高价值活跃用户': '重点维护：提供VIP服务、专属优惠，提升忠诚度和复购率',
    '中等价值用户': '价值提升：通过交叉销售、套餐推荐提高客单价和消费频次',
    '低价值沉默用户': '激活召回：发送优惠券、新品通知，重新激发消费兴趣'
}

for segment, advice in strategy_advice.items():
    if segment in df['segment_name'].values:
        count = (df['segment_name'] == segment).sum()
        percent = count / len(df) * 100
        print(f"\n【{segment}】（{percent:.1f}%用户）")
        print(f"  特征：{rfm_means.loc[segment].to_dict()}")
        print(f"  建议：{advice}")

# 保存模型（工程化体现）
print("\n" + "="*50)
print("模型保存与部署准备")
print("="*50)

model_package = {
    'kmeans_model': model,
    'scaler': scaler,
    'feature_names': features,
    'segment_names': segment_names,
    'metadata': {
        'n_samples': len(df),
        'silhouette_score': score,
        'best_k': k
    }
}

joblib.dump(model_package, 'rfm_segmentation_model.joblib')
print(" 模型已保存为 'rfm_segmentation_model.joblib'")

# 提供预测示例
print("\n 预测示例：")
test_user = np.array([[0.05, 3, 800]])  # 30天未消费(1/31≈0.032)、3次订单、800元
test_scaled = scaler.transform(test_user)
predicted_cluster = model.predict(test_scaled)[0]
print(f"  输入：新用户(30天未购, 3次订单, 消费800元)")
print(f"  预测：{segment_names[predicted_cluster]} (簇{predicted_cluster})")

# ========== 9. 导出结果 ==========
output_cols = ['uid', 'last_order_date', 'order_count', 'total_amount', 
               'customer_type', 'segment_name']
df[output_cols].to_csv('rfm_clustering_results.csv', index=False, encoding='utf-8-sig')
print(f"\n 分群结果已导出：'rfm_clustering_results.csv' ({len(df)}条记录)")

print("\n" + "="*50)
print("    RFM用户分群分析完成！")
print(f"   用户总数：{len(df)}")
print(f"   最佳分群：{k}类")
print(f"   模型质量：轮廓系数 {score:.3f}")
print("="*50)
