# E-Commerce RFM Customer Segmentation Model

## 项目简介
这是一个针对电商用户的**RFM用户分层模型**项目，通过分析用户的最近消费时间、消费频次和消费金额，将用户划分为不同价值层级，为电商精准运营、资源倾斜提供数据支撑，逻辑完整且可直接运行。该模型会通过三个维度的重要指标，对用户的价值做识别，并据此将用户分为8个组，进行精细化的管理。

## 核心功能
1.  数据预处理：清洗缺失值、异常值（负向数据）和重复用户数据
2.  RFM指标计算：自动计算R（最近消费间隔）、F（消费频次）、M（消费金额）三大核心指标
3.  描述性分析：对R/F/M指标进行分布统计并可视化展示
4.  用户分层：基于RFM指标实现8类用户分层，输出可落地的用户标签
5.  结果可视化：通过双y轴图直观展示各层级用户数量及占比

## 运行环境
- Python 3.x（推荐3.8及以上版本）
- 核心依赖库：
  - pandas：数据读取与处理
  - matplotlib：数据可视化
  - datetime：时间格式转换与计算

## 数据集格式
无需上传原始数据集，仅需准备`csv`格式数据，包含以下核心字段：
| 字段名          | 字段说明                  |
|-----------------|---------------------------|
| uid             | 用户唯一标识ID            |
| order_count     | 用户累计订单数（F指标）   |
| total_amount    | 用户累计消费金额（M指标）  |
| last_order_date | 用户最后一次消费日期      |

## 项目核心流程
1.  **数据预处理**
    - 删除`order_count`和`total_amount`字段的缺失值
    - 过滤订单数、消费金额为负数的异常数据
    - 去除`uid`重复的用户数据，保证用户唯一性

2.  **RFM指标计算**
    - F指标：直接使用`order_count`字段
    - M指标：直接使用`total_amount`字段
    - R指标：以2019年4月1日为截止时间，计算用户最后消费日期与截止时间的间隔天数（`time_gap`）

3.  **RFM分箱与分层**
    - 采用`pd.qcut`分箱（3等分）
    - 通过自定义函数`rfmTrans`将分箱结果转换为0/1二值标签
    - 结合3个标签组合（`mark`字段），通过`rfmTypes`函数实现8类用户分层

4.  **可视化展示**
    - 子图展示R/F/M三大指标的分布情况
    - 双y轴图展示用户分层结果（数量+占比）

## 用户分层结果说明
| 标签组合 | 用户类型       | 说明                     |
|----------|----------------|--------------------------|
| 111      | 高价值用户     | 最近消费、频次、金额均优 |
| 101      | 重点发展用户   | 最近消费、金额优，频次待提升 |
| 011      | 重点唤回用户   | 频次、金额优，需唤醒复购 |
| 001      | 重点潜力用户   | 金额优，其余两项待优化   |
| 110      | 一般潜力用户   | 最近消费、频次优，金额待提升 |
| 100      | 一般发展用户   | 最近消费优，其余两项待优化 |
| 010      | 一般用户       | 频次优，其余两项待优化   |
| 其他     | 低价值用户     | 三项指标均待提升         |

## 运行方式
1.  将上述Python代码保存为`.py`文件（如`ecommerce_rfm_analysis.py`）
2.  修改代码中`pd.read_csv`的文件路径为你的本地数据集路径
3.  安装依赖库（若未安装）：`pip install pandas matplotlib`
4.  直接运行代码，自动输出可视化图表与用户分层结果


-------------------

# E-Commerce RFM Customer Segmentation Model
## Project Overview
This is an **RFM customer segmentation model** project designed for e-commerce users. By analyzing users' recency of last purchase, purchase frequency, and monetary value, the model classifies users into different value tiers. It provides data support for e-commerce precision marketing and resource allocation, featuring complete logic and ready-to-run capability. The model identifies user value through three core dimensions and divides users into 8 segments for refined management.

## Core Features
1.  **Data Preprocessing**: Cleans missing values, abnormal data (negative values), and duplicate user records.
2.  **RFM Metric Calculation**: Automatically computes three core metrics: R (Recency of last purchase), F (Purchase Frequency), and M (Monetary Value).
3.  **Descriptive Analysis**: Conducts distribution statistics on R/F/M metrics and presents results through visualization.
4.  **User Segmentation**: Implements 8-tier user classification based on RFM metrics and outputs actionable user labels.
5.  **Result Visualization**: Intuitively displays the quantity and proportion of users in each tier via a dual-y-axis chart.

## Runtime Environment
- Python 3.x (Python 3.8 or higher is recommended)
- Core Dependencies:
  - pandas: Data reading and processing
  - matplotlib: Data visualization
  - datetime: Time format conversion and calculation

## Dataset Format
There is no need to upload the raw dataset. Simply prepare a `csv` file with the following core fields:

| Field Name          | Field Description                  |
|---------------------|------------------------------------|
| uid                 | Unique user identification ID      |
| order_count         | Total number of orders per user (F metric) |
| total_amount        | Total consumption amount per user (M metric) |
| last_order_date     | Date of the user's last purchase   |

## Core Project Workflow
1.  **Data Preprocessing**
    - Removes missing values in the `order_count` and `total_amount` fields.
    - Filters out abnormal data with negative order counts or consumption amounts.
    - Eliminates duplicate user data based on `uid` to ensure user uniqueness.

2.  **RFM Metric Calculation**
    - **F Metric**: Directly uses the `order_count` field.
    - **M Metric**: Directly uses the `total_amount` field.
    - **R Metric**: Sets April 1, 2019 as the cutoff date and calculates the number of days between the user's last purchase date and the cutoff date (`time_gap`).
    - Adopts `pd.qcut` for 3-level binning.
    - Converts binning results into binary labels (0/1) via the custom function `rfmTrans`.
    - Combines the three binary labels into a `mark` field and implements 8-tier user segmentation through the custom function `rfmTypes`.

3.  **Visualization Display**
    - Uses subplots to show the distribution of R/F/M metrics.
    - Uses a dual-y-axis chart to display user segmentation results (quantity + proportion).

## User Segmentation Results Explanation
| Label Combination | User Type               | Explanation                                  |
|-------------------|-------------------------|----------------------------------------------|
| 111               | High-Value Users        | Excellent performance in recency, frequency, and monetary value |
| 101               | Key Development Users   | Strong in recency and monetary value; needs improvement in purchase frequency |
| 011               | Key Recall Users        | Good in frequency and monetary value; requires repurchase stimulation |
| 001               | Key Potential Users     | High monetary value; needs optimization in recency and frequency |
| 110               | General Potential Users | Strong in recency and frequency; needs to increase consumption amount |
| 100               | General Development Users | Good in recency; requires improvement in frequency and monetary value |
| 010               | Regular Users           | Strong in frequency; needs optimization in recency and monetary value |
| Others            | Low-Value Users         | Requires improvement in all three metrics    |

## How to Run
1.  Save the above Python code as a `.py` file (e.g., `ecommerce_rfm_analysis.py`).
2.  Modify the `pd.read_csv` file path in the code to your local dataset path.
3.  Install the required dependencies if they are not already installed: `pip install pandas matplotlib`.
4.  Run the code directly to automatically output visualization charts and user segmentation results.