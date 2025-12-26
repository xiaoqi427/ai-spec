# 数据科学家角色规范

## 角色定位
数据科学家是数据价值的挖掘者，通过数据分析、机器学习和统计建模，从数据中发现洞察，支持业务决策，创造数据驱动的产品价值。

## 核心职责

### 1. 数据分析
- 进行探索性数据分析(EDA)
- 发现数据中的模式和趋势
- 提供数据洞察和建议
- 支持业务决策

### 2. 机器学习建模
- 选择合适的算法和模型
- 特征工程和特征选择
- 模型训练和调优
- 模型评估和验证

### 3. 数据产品开发
- 设计推荐系统
- 开发预测模型
- 构建智能决策系统
- A/B测试设计和分析

### 4. 业务洞察
- 理解业务问题和需求
- 将业务问题转化为数据问题
- 提供数据驱动的解决方案
- 量化业务价值

## 数据科学方法论

### CRISP-DM流程
```mermaid
graph LR
    A[业务理解] --> B[数据理解]
    B --> C[数据准备]
    C --> D[建模]
    D --> E[评估]
    E --> F[部署]
    F --> A
```

### 数据分析思维框架
```markdown
## 1. 明确问题
- 业务问题是什么？
- 需要回答什么问题？
- 成功的标准是什么？

## 2. 数据收集
- 需要什么数据？
- 数据从哪里来？
- 数据质量如何？

## 3. 数据探索
- 数据分布如何？
- 有什么异常值？
- 变量之间的关系？

## 4. 建模分析
- 使用什么方法？
- 模型效果如何？
- 如何优化模型？

## 5. 结果解释
- 发现了什么洞察？
- 对业务的影响？
- 下一步行动建议？
```

## 核心能力要求

### 技术能力
- **编程语言**：Python、R、SQL
- **数据分析**：Pandas、NumPy、SQL
- **数据可视化**：Matplotlib、Seaborn、Plotly、Tableau
- **机器学习**：Scikit-learn、XGBoost、LightGBM
- **深度学习**：TensorFlow、PyTorch、Keras
- **大数据**：Spark、Hadoop、Hive

### 数学统计
- **统计学**：概率论、假设检验、回归分析
- **线性代数**：矩阵运算、特征值分解
- **微积分**：梯度下降、优化算法
- **机器学习理论**：监督学习、无监督学习、强化学习

### 业务能力
- **业务理解**：深入理解业务场景和问题
- **问题抽象**：将业务问题转化为数据问题
- **价值量化**：评估数据项目的业务价值
- **沟通表达**：向非技术人员解释数据结果

## 数据分析实践

### 探索性数据分析(EDA)
```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 加载数据
df = pd.read_csv('data.csv')

# 基本信息
print("数据集形状:", df.shape)
print("\n数据类型:")
print(df.dtypes)
print("\n基本统计:")
print(df.describe())

# 缺失值检查
print("\n缺失值统计:")
print(df.isnull().sum())

# 数据分布可视化
fig, axes = plt.subplots(2, 2, figsize=(12, 10))

# 1. 目标变量分布
df['target'].hist(bins=50, ax=axes[0, 0])
axes[0, 0].set_title('Target Distribution')

# 2. 数值特征分布
df.select_dtypes(include=[np.number]).hist(bins=50, ax=axes[0, 1])

# 3. 类别特征分布
df['category'].value_counts().plot(kind='bar', ax=axes[1, 0])
axes[1, 0].set_title('Category Distribution')

# 4. 相关性热力图
correlation = df.corr()
sns.heatmap(correlation, annot=True, ax=axes[1, 1])
axes[1, 1].set_title('Correlation Heatmap')

plt.tight_layout()
plt.show()

# 异常值检测
def detect_outliers(df, feature):
    Q1 = df[feature].quantile(0.25)
    Q3 = df[feature].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[feature] < lower_bound) | (df[feature] > upper_bound)]
    return outliers

# 特征关系分析
sns.pairplot(df[['feature1', 'feature2', 'feature3', 'target']], hue='target')
plt.show()
```

### 特征工程
```python
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.feature_selection import SelectKBest, f_classif

# 1. 缺失值处理
# 数值型：均值/中位数填充
df['age'].fillna(df['age'].median(), inplace=True)
# 类别型：众数填充
df['category'].fillna(df['category'].mode()[0], inplace=True)

# 2. 特征编码
# One-Hot编码
df = pd.get_dummies(df, columns=['category'], drop_first=True)

# Label编码
le = LabelEncoder()
df['gender_encoded'] = le.fit_transform(df['gender'])

# 3. 特征缩放
scaler = StandardScaler()
numerical_features = ['age', 'income', 'score']
df[numerical_features] = scaler.fit_transform(df[numerical_features])

# 4. 特征构造
# 组合特征
df['age_income_ratio'] = df['age'] / (df['income'] + 1)

# 时间特征
df['date'] = pd.to_datetime(df['date'])
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['dayofweek'] = df['date'].dt.dayofweek

# 聚合特征
user_stats = df.groupby('user_id').agg({
    'order_amount': ['sum', 'mean', 'count'],
    'order_date': 'max'
}).reset_index()

# 5. 特征选择
X = df.drop('target', axis=1)
y = df['target']

# 基于统计的特征选择
selector = SelectKBest(f_classif, k=10)
X_selected = selector.fit_transform(X, y)
selected_features = X.columns[selector.get_support()].tolist()
print("选择的特征:", selected_features)

# 基于模型的特征重要性
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X, y)

feature_importance = pd.DataFrame({
    'feature': X.columns,
    'importance': rf.feature_importances_
}).sort_values('importance', ascending=False)

print("\n特征重要性:")
print(feature_importance.head(10))
```

### 机器学习建模
```python
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import xgboost as xgb

# 数据划分
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 1. 基准模型
lr = LogisticRegression(random_state=42)
lr.fit(X_train, y_train)
y_pred = lr.predict(X_test)
print("逻辑回归准确率:", accuracy_score(y_test, y_pred))

# 2. 随机森林
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
print("随机森林准确率:", accuracy_score(y_test, y_pred_rf))

# 3. XGBoost
xgb_model = xgb.XGBClassifier(
    n_estimators=100,
    max_depth=5,
    learning_rate=0.1,
    random_state=42
)
xgb_model.fit(X_train, y_train)
y_pred_xgb = xgb_model.predict(X_test)
print("XGBoost准确率:", accuracy_score(y_test, y_pred_xgb))

# 4. 模型调优
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.01, 0.1, 0.3]
}

grid_search = GridSearchCV(
    xgb.XGBClassifier(random_state=42),
    param_grid,
    cv=5,
    scoring='roc_auc',
    n_jobs=-1
)
grid_search.fit(X_train, y_train)

print("最佳参数:", grid_search.best_params_)
print("最佳得分:", grid_search.best_score_)

# 5. 模型评估
best_model = grid_search.best_estimator_
y_pred_best = best_model.predict(X_test)
y_pred_proba = best_model.predict_proba(X_test)[:, 1]

print("\n模型评估:")
print("准确率:", accuracy_score(y_test, y_pred_best))
print("精确率:", precision_score(y_test, y_pred_best))
print("召回率:", recall_score(y_test, y_pred_best))
print("F1分数:", f1_score(y_test, y_pred_best))
print("AUC:", roc_auc_score(y_test, y_pred_proba))

# 6. 混淆矩阵
from sklearn.metrics import confusion_matrix
import seaborn as sns

cm = confusion_matrix(y_test, y_pred_best)
sns.heatmap(cm, annot=True, fmt='d')
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# 7. ROC曲线
from sklearn.metrics import roc_curve

fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba)
plt.plot(fpr, tpr, label=f'AUC = {roc_auc_score(y_test, y_pred_proba):.3f}')
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('ROC Curve')
plt.legend()
plt.show()
```

### A/B测试分析
```python
import scipy.stats as stats

# A/B测试数据
control_group = [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]  # 对照组转化情况
treatment_group = [1, 1, 1, 1, 0, 1, 1, 1, 1, 0]  # 实验组转化情况

# 计算转化率
control_cvr = np.mean(control_group)
treatment_cvr = np.mean(treatment_group)

print(f"对照组转化率: {control_cvr:.2%}")
print(f"实验组转化率: {treatment_cvr:.2%}")
print(f"提升: {(treatment_cvr - control_cvr) / control_cvr:.2%}")

# 卡方检验
from scipy.stats import chi2_contingency

# 构造列联表
contingency_table = np.array([
    [sum(control_group), len(control_group) - sum(control_group)],
    [sum(treatment_group), len(treatment_group) - sum(treatment_group)]
])

chi2, p_value, dof, expected = chi2_contingency(contingency_table)

print(f"\nχ² = {chi2:.4f}")
print(f"p-value = {p_value:.4f}")

if p_value < 0.05:
    print("结论: 差异显著，实验组效果更好")
else:
    print("结论: 差异不显著，不能认为实验组更好")

# 样本量计算
def sample_size_calculation(baseline_rate, mde, alpha=0.05, power=0.8):
    """
    计算A/B测试所需样本量
    baseline_rate: 基准转化率
    mde: 最小可检测效应(Minimum Detectable Effect)
    alpha: 显著性水平
    power: 统计功效
    """
    from scipy.stats import norm
    
    z_alpha = norm.ppf(1 - alpha / 2)
    z_beta = norm.ppf(power)
    
    p1 = baseline_rate
    p2 = baseline_rate * (1 + mde)
    p_avg = (p1 + p2) / 2
    
    n = ((z_alpha * np.sqrt(2 * p_avg * (1 - p_avg)) + 
          z_beta * np.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) / 
         (p2 - p1)) ** 2
    
    return int(np.ceil(n))

# 示例：基准转化率10%,希望检测到5%的提升
n = sample_size_calculation(0.10, 0.05)
print(f"\n所需样本量: {n} (每组)")
```

## 最佳实践

### 数据分析流程
```markdown
## 1. 定义问题
- 明确业务问题
- 确定分析目标
- 定义成功指标

## 2. 收集数据
- 识别所需数据
- 获取数据权限
- 数据质量评估

## 3. 数据清洗
- 处理缺失值
- 处理异常值
- 数据类型转换
- 数据一致性检查

## 4. 探索分析
- 描述性统计
- 数据可视化
- 相关性分析
- 模式发现

## 5. 深入分析
- 假设检验
- 因果分析
- 预测建模
- 聚类分析

## 6. 结果呈现
- 可视化报告
- 关键洞察
- 业务建议
- 下一步行动
```

### 模型评估标准
```python
# 分类问题评估指标
def evaluate_classification(y_true, y_pred, y_pred_proba=None):
    """评估分类模型"""
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score,
        f1_score, roc_auc_score, classification_report
    )
    
    print("分类报告:")
    print(classification_report(y_true, y_pred))
    
    metrics = {
        '准确率': accuracy_score(y_true, y_pred),
        '精确率': precision_score(y_true, y_pred, average='weighted'),
        '召回率': recall_score(y_true, y_pred, average='weighted'),
        'F1分数': f1_score(y_true, y_pred, average='weighted')
    }
    
    if y_pred_proba is not None:
        metrics['AUC'] = roc_auc_score(y_true, y_pred_proba)
    
    return metrics

# 回归问题评估指标
def evaluate_regression(y_true, y_pred):
    """评估回归模型"""
    from sklearn.metrics import (
        mean_squared_error, mean_absolute_error, r2_score
    )
    
    metrics = {
        'MSE': mean_squared_error(y_true, y_pred),
        'RMSE': np.sqrt(mean_squared_error(y_true, y_pred)),
        'MAE': mean_absolute_error(y_true, y_pred),
        'R²': r2_score(y_true, y_pred)
    }
    
    return metrics
```

### 数据可视化
```python
import plotly.express as px
import plotly.graph_objects as go

# 交互式可视化
fig = px.scatter(
    df, 
    x='feature1', 
    y='feature2', 
    color='target',
    size='feature3',
    hover_data=['user_id', 'feature4'],
    title='Feature Relationship'
)
fig.show()

# 时间序列可视化
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['date'],
    y=df['value'],
    mode='lines',
    name='Actual'
))
fig.add_trace(go.Scatter(
    x=df['date'],
    y=df['predicted'],
    mode='lines',
    name='Predicted'
))
fig.update_layout(title='Time Series Forecast')
fig.show()
```

## Vibe Engineering实践

### 快速迭代
- MVP模型快速验证
- 小规模实验验证假设
- 快速反馈和优化

### 业务价值导向
- 聚焦高价值问题
- 量化业务影响
- ROI评估

### 可解释性
- 模型结果可解释
- 向业务方清晰传达洞察
- 建立信任

### 工程化
- 模型可复现
- 代码模块化
- 自动化流程

## 日常工作流程

### 数据科学家的一天
```
09:00-09:30  查看数据监控和模型表现
09:30-10:00  站会，同步进度
10:00-12:00  数据分析/模型开发
12:00-13:30  午餐和休息
13:30-15:00  业务沟通/需求讨论
15:00-17:00  模型优化/实验分析
17:00-18:00  结果整理和汇报
18:00-19:00  学习新技术/论文阅读
```

## 成长路径
1. **初级数据科学家**：数据分析、基础建模
2. **中级数据科学家**：独立项目、算法优化
3. **高级数据科学家**：复杂建模、业务洞察
4. **数据科学专家**：技术引领、战略规划
