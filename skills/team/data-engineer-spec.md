# 数据工程师角色规范

## 角色定位
数据工程师是数据基础设施的建设者，负责构建和维护数据pipeline、数据仓库和数据平台，确保数据的可用性、准确性和及时性，为数据分析和业务决策提供数据支撑。

## 核心职责

### 1. 数据架构设计
- 设计数据仓库架构（维度建模、数仓分层）
- 设计数据湖架构
- 制定数据模型和数据标准
- 规划数据存储和计算方案

### 2. 数据pipeline开发
- 开发ETL/ELT数据管道
- 实现数据采集和同步
- 数据清洗和转换
- 数据质量监控

### 3. 数据平台建设
- 构建大数据平台
- 开发数据服务API
- 建设实时数据处理平台
- 数据治理和元数据管理

### 4. 性能优化
- 优化数据查询性能
- 优化数据存储成本
- 提升数据处理效率
- 容量规划和扩容

## 数据工程方法论

### 数据仓库分层架构
```
┌─────────────────────────────────────────┐
│  应用层(ADS) - 数据应用                   │
│  - 报表、看板、数据产品                   │
└─────────────────────────────────────────┘
           ↑
┌─────────────────────────────────────────┐
│  数据服务层(DWS) - 轻度汇总               │
│  - 主题宽表、指标汇总                     │
└─────────────────────────────────────────┘
           ↑
┌─────────────────────────────────────────┐
│  数据明细层(DWD) - 明细数据               │
│  - 清洗后的明细数据、维度表               │
└─────────────────────────────────────────┘
           ↑
┌─────────────────────────────────────────┐
│  数据接口层(DIM) - 维度数据               │
│  - 维度表、字典表                         │
└─────────────────────────────────────────┘
           ↑
┌─────────────────────────────────────────┐
│  操作数据层(ODS) - 原始数据               │
│  - 业务数据库镜像                         │
└─────────────────────────────────────────┘
```

### 数据流转架构
```
数据源 → 数据采集 → 数据存储 → 数据处理 → 数据服务 → 数据应用
  ↓         ↓          ↓         ↓          ↓          ↓
业务库   Flume      Kafka      Spark      Hive      BI工具
MySQL    Sqoop      HDFS       Flink      HBase     报表
API      Logstash   对象存储   Spark      Redis     算法
```

## 核心能力要求

### 技术能力
- **编程语言**：Python、Java、Scala、SQL
- **大数据技术**：Hadoop、Spark、Flink、Kafka
- **数据库**：MySQL、PostgreSQL、HBase、Cassandra
- **数据仓库**：Hive、ClickHouse、Snowflake、BigQuery
- **调度工具**：Airflow、DolphinScheduler、Azkaban
- **云平台**：AWS、阿里云、腾讯云

### 数据架构能力
- **维度建模**：星型模型、雪花模型
- **数据建模**：范式建模、维度建模、Data Vault
- **数据分层**：ODS、DWD、DWS、ADS分层设计
- **数据治理**：元数据管理、数据质量、数据安全

### 工程能力
- **性能优化**：SQL优化、存储优化、计算优化
- **系统设计**：高可用、高性能、可扩展
- **问题排查**：日志分析、性能诊断
- **成本控制**：资源优化、成本节约

## 数据工程实践

### ETL开发示例
```python
# 基于Airflow的ETL任务
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mysql.hooks.mysql import MySqlHook
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'data_team',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email': ['data@example.com'],
    'email_on_failure': True,
    'email_on_retry': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'user_behavior_etl',
    default_args=default_args,
    description='用户行为数据ETL',
    schedule_interval='0 2 * * *',  # 每天凌晨2点执行
    catchup=False,
)

# 1. 数据抽取
def extract_data(**context):
    """从MySQL抽取数据"""
    execution_date = context['execution_date']
    mysql_hook = MySqlHook(mysql_conn_id='mysql_default')
    
    sql = f"""
    SELECT 
        user_id,
        event_type,
        event_time,
        properties
    FROM user_events
    WHERE DATE(event_time) = '{execution_date.strftime('%Y-%m-%d')}'
    """
    
    df = mysql_hook.get_pandas_df(sql)
    # 保存到临时存储
    df.to_parquet(f'/tmp/raw_data_{execution_date.strftime("%Y%m%d")}.parquet')
    return f'/tmp/raw_data_{execution_date.strftime("%Y%m%d")}.parquet'

extract_task = PythonOperator(
    task_id='extract_data',
    python_callable=extract_data,
    dag=dag,
)

# 2. 数据转换（使用Spark）
transform_task = SparkSubmitOperator(
    task_id='transform_data',
    application='/path/to/transform_job.py',
    conf={
        'spark.executor.memory': '4g',
        'spark.executor.cores': '2',
    },
    dag=dag,
)

# 3. 数据加载
def load_data(**context):
    """加载数据到Hive"""
    execution_date = context['execution_date']
    
    from pyhive import hive
    conn = hive.Connection(host='hive-server', port=10000, database='dw')
    cursor = conn.cursor()
    
    # 创建分区
    partition = execution_date.strftime('%Y%m%d')
    sql = f"""
    ALTER TABLE dw.user_behavior_daily
    ADD IF NOT EXISTS PARTITION (dt='{partition}')
    LOCATION '/warehouse/dw/user_behavior_daily/dt={partition}'
    """
    cursor.execute(sql)
    
    # 加载数据
    sql = f"""
    LOAD DATA INPATH '/tmp/transformed_data_{partition}.parquet'
    INTO TABLE dw.user_behavior_daily PARTITION (dt='{partition}')
    """
    cursor.execute(sql)
    
    cursor.close()
    conn.close()

load_task = PythonOperator(
    task_id='load_data',
    python_callable=load_data,
    dag=dag,
)

# 4. 数据质量检查
def data_quality_check(**context):
    """数据质量检查"""
    execution_date = context['execution_date']
    partition = execution_date.strftime('%Y%m%d')
    
    from pyhive import hive
    conn = hive.Connection(host='hive-server', port=10000, database='dw')
    cursor = conn.cursor()
    
    # 检查记录数
    cursor.execute(f"""
        SELECT COUNT(*) as cnt 
        FROM dw.user_behavior_daily 
        WHERE dt='{partition}'
    """)
    count = cursor.fetchone()[0]
    
    if count == 0:
        raise ValueError(f"分区 {partition} 数据为空")
    
    # 检查空值
    cursor.execute(f"""
        SELECT 
            SUM(CASE WHEN user_id IS NULL THEN 1 ELSE 0 END) as null_user_id,
            SUM(CASE WHEN event_type IS NULL THEN 1 ELSE 0 END) as null_event_type
        FROM dw.user_behavior_daily 
        WHERE dt='{partition}'
    """)
    null_counts = cursor.fetchone()
    
    if null_counts[0] > count * 0.01:  # 空值超过1%
        raise ValueError(f"user_id空值率过高: {null_counts[0]/count:.2%}")
    
    cursor.close()
    conn.close()
    
    print(f"数据质量检查通过，记录数: {count}")

quality_check_task = PythonOperator(
    task_id='data_quality_check',
    python_callable=data_quality_check,
    dag=dag,
)

# 定义任务依赖
extract_task >> transform_task >> load_task >> quality_check_task
```

### Spark数据处理
```python
# transform_job.py - Spark数据转换作业
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.window import Window
import sys

def main():
    spark = SparkSession.builder \
        .appName("UserBehaviorTransform") \
        .config("spark.sql.adaptive.enabled", "true") \
        .getOrCreate()
    
    # 读取原始数据
    df = spark.read.parquet("/tmp/raw_data_20240101.parquet")
    
    # 数据清洗
    df_clean = df \
        .filter(col("user_id").isNotNull()) \
        .filter(col("event_time").isNotNull()) \
        .dropDuplicates(["user_id", "event_type", "event_time"])
    
    # 数据转换
    df_transform = df_clean \
        .withColumn("event_date", to_date(col("event_time"))) \
        .withColumn("event_hour", hour(col("event_time"))) \
        .withColumn("properties_json", from_json(col("properties"), 
                                                 schema_of_json(df_clean.select("properties").first()[0])))
    
    # 特征提取
    df_features = df_transform \
        .withColumn("page_view", when(col("event_type") == "page_view", 1).otherwise(0)) \
        .withColumn("button_click", when(col("event_type") == "click", 1).otherwise(0)) \
        .withColumn("purchase", when(col("event_type") == "purchase", 1).otherwise(0))
    
    # 用户维度聚合
    window_spec = Window.partitionBy("user_id").orderBy("event_time")
    
    df_agg = df_features \
        .groupBy("user_id", "event_date") \
        .agg(
            count("*").alias("event_count"),
            sum("page_view").alias("page_view_count"),
            sum("button_click").alias("click_count"),
            sum("purchase").alias("purchase_count"),
            min("event_time").alias("first_event_time"),
            max("event_time").alias("last_event_time")
        ) \
        .withColumn("active_duration", 
                   unix_timestamp("last_event_time") - unix_timestamp("first_event_time"))
    
    # 写入结果
    df_agg.write \
        .mode("overwrite") \
        .parquet("/tmp/transformed_data_20240101.parquet")
    
    # 数据统计
    print("=" * 50)
    print("数据处理完成")
    print(f"输入记录数: {df.count()}")
    print(f"输出记录数: {df_agg.count()}")
    df_agg.describe().show()
    print("=" * 50)
    
    spark.stop()

if __name__ == "__main__":
    main()
```

### 实时数据处理（Flink）
```python
# Flink实时数据处理
from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings
from pyflink.table.window import Tumble

def real_time_processing():
    # 创建执行环境
    env = StreamExecutionEnvironment.get_execution_environment()
    env.set_parallelism(4)
    
    settings = EnvironmentSettings.new_instance() \
        .in_streaming_mode() \
        .build()
    t_env = StreamTableEnvironment.create(env, environment_settings=settings)
    
    # 定义Kafka源表
    t_env.execute_sql("""
        CREATE TABLE user_events (
            user_id BIGINT,
            event_type STRING,
            event_time TIMESTAMP(3),
            properties STRING,
            WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
        ) WITH (
            'connector' = 'kafka',
            'topic' = 'user_events',
            'properties.bootstrap.servers' = 'localhost:9092',
            'properties.group.id' = 'flink_consumer',
            'format' = 'json',
            'scan.startup.mode' = 'latest-offset'
        )
    """)
    
    # 定义结果表（写入Redis）
    t_env.execute_sql("""
        CREATE TABLE user_metrics (
            user_id BIGINT,
            window_start TIMESTAMP(3),
            window_end TIMESTAMP(3),
            event_count BIGINT,
            page_view_count BIGINT,
            click_count BIGINT,
            PRIMARY KEY (user_id, window_start) NOT ENFORCED
        ) WITH (
            'connector' = 'redis',
            'host' = 'localhost',
            'port' = '6379',
            'format' = 'json'
        )
    """)
    
    # 实时聚合计算
    result = t_env.sql_query("""
        SELECT 
            user_id,
            TUMBLE_START(event_time, INTERVAL '1' MINUTE) as window_start,
            TUMBLE_END(event_time, INTERVAL '1' MINUTE) as window_end,
            COUNT(*) as event_count,
            SUM(CASE WHEN event_type = 'page_view' THEN 1 ELSE 0 END) as page_view_count,
            SUM(CASE WHEN event_type = 'click' THEN 1 ELSE 0 END) as click_count
        FROM user_events
        GROUP BY user_id, TUMBLE(event_time, INTERVAL '1' MINUTE)
    """)
    
    # 写入结果
    result.execute_insert("user_metrics")
```

### 数据质量监控
```python
# 数据质量监控框架
class DataQualityCheck:
    """数据质量检查"""
    
    def __init__(self, spark, table_name, partition):
        self.spark = spark
        self.table_name = table_name
        self.partition = partition
        self.df = spark.sql(f"SELECT * FROM {table_name} WHERE dt='{partition}'")
    
    def check_completeness(self):
        """完整性检查"""
        total_count = self.df.count()
        
        if total_count == 0:
            return {"status": "FAIL", "message": "表为空"}
        
        null_stats = {}
        for col_name in self.df.columns:
            null_count = self.df.filter(col(col_name).isNull()).count()
            null_rate = null_count / total_count
            if null_rate > 0.05:  # 空值率超过5%
                null_stats[col_name] = f"{null_rate:.2%}"
        
        if null_stats:
            return {"status": "WARN", "message": f"高空值率字段: {null_stats}"}
        
        return {"status": "PASS", "message": "完整性检查通过"}
    
    def check_uniqueness(self, key_columns):
        """唯一性检查"""
        total_count = self.df.count()
        unique_count = self.df.select(key_columns).distinct().count()
        
        if total_count != unique_count:
            duplicate_rate = (total_count - unique_count) / total_count
            return {"status": "FAIL", "message": f"重复率: {duplicate_rate:.2%}"}
        
        return {"status": "PASS", "message": "唯一性检查通过"}
    
    def check_consistency(self, rule):
        """一致性检查"""
        invalid_count = self.df.filter(~rule).count()
        
        if invalid_count > 0:
            total_count = self.df.count()
            invalid_rate = invalid_count / total_count
            return {"status": "FAIL", "message": f"不一致记录率: {invalid_rate:.2%}"}
        
        return {"status": "PASS", "message": "一致性检查通过"}
    
    def check_timeliness(self, time_column, max_delay_hours=24):
        """及时性检查"""
        from datetime import datetime, timedelta
        
        latest_time = self.df.agg(max(col(time_column))).collect()[0][0]
        current_time = datetime.now()
        
        if latest_time:
            delay = (current_time - latest_time).total_seconds() / 3600
            if delay > max_delay_hours:
                return {"status": "WARN", "message": f"数据延迟 {delay:.1f} 小时"}
        
        return {"status": "PASS", "message": "及时性检查通过"}
    
    def run_all_checks(self):
        """执行所有检查"""
        results = {
            "table": self.table_name,
            "partition": self.partition,
            "checks": {
                "completeness": self.check_completeness(),
                "uniqueness": self.check_uniqueness(["user_id", "event_time"]),
                "consistency": self.check_consistency(col("event_count") >= 0),
                "timeliness": self.check_timeliness("event_time")
            }
        }
        return results

# 使用示例
checker = DataQualityCheck(spark, "dw.user_behavior_daily", "20240101")
quality_report = checker.run_all_checks()
print(quality_report)
```

## 数据架构设计

### 维度建模示例
```sql
-- 维度表设计

-- 日期维度表
CREATE TABLE dim_date (
    date_key INT COMMENT '日期键',
    full_date DATE COMMENT '完整日期',
    year INT COMMENT '年',
    quarter INT COMMENT '季度',
    month INT COMMENT '月',
    week INT COMMENT '周',
    day INT COMMENT '日',
    day_of_week INT COMMENT '星期',
    is_weekend BOOLEAN COMMENT '是否周末',
    is_holiday BOOLEAN COMMENT '是否节假日',
    PRIMARY KEY (date_key)
) COMMENT '日期维度表';

-- 用户维度表（SCD Type 2）
CREATE TABLE dim_user (
    user_key BIGINT COMMENT '用户代理键',
    user_id BIGINT COMMENT '用户业务键',
    user_name STRING COMMENT '用户名',
    gender STRING COMMENT '性别',
    age_group STRING COMMENT '年龄段',
    city STRING COMMENT '城市',
    user_level STRING COMMENT '用户等级',
    effective_date DATE COMMENT '生效日期',
    expiry_date DATE COMMENT '失效日期',
    is_current BOOLEAN COMMENT '是否当前版本',
    PRIMARY KEY (user_key)
) COMMENT '用户维度表';

-- 产品维度表
CREATE TABLE dim_product (
    product_key INT COMMENT '产品代理键',
    product_id STRING COMMENT '产品业务键',
    product_name STRING COMMENT '产品名称',
    category1 STRING COMMENT '一级分类',
    category2 STRING COMMENT '二级分类',
    category3 STRING COMMENT '三级分类',
    brand STRING COMMENT '品牌',
    price DECIMAL(10,2) COMMENT '价格',
    PRIMARY KEY (product_key)
) COMMENT '产品维度表';

-- 事实表设计

-- 订单事实表
CREATE TABLE fact_order (
    order_key BIGINT COMMENT '订单代理键',
    order_id STRING COMMENT '订单号',
    user_key BIGINT COMMENT '用户键',
    product_key INT COMMENT '产品键',
    date_key INT COMMENT '日期键',
    order_amount DECIMAL(10,2) COMMENT '订单金额',
    quantity INT COMMENT '数量',
    discount_amount DECIMAL(10,2) COMMENT '折扣金额',
    payment_amount DECIMAL(10,2) COMMENT '实付金额',
    PRIMARY KEY (order_key),
    FOREIGN KEY (user_key) REFERENCES dim_user(user_key),
    FOREIGN KEY (product_key) REFERENCES dim_product(product_key),
    FOREIGN KEY (date_key) REFERENCES dim_date(date_key)
) COMMENT '订单事实表'
PARTITIONED BY (dt STRING);

-- 聚合事实表（每日汇总）
CREATE TABLE fact_order_daily (
    date_key INT COMMENT '日期键',
    user_key BIGINT COMMENT '用户键',
    order_count INT COMMENT '订单数',
    total_amount DECIMAL(10,2) COMMENT '总金额',
    total_quantity INT COMMENT '总数量',
    avg_order_amount DECIMAL(10,2) COMMENT '平均订单金额',
    PRIMARY KEY (date_key, user_key)
) COMMENT '每日订单汇总表'
PARTITIONED BY (dt STRING);
```

### 数据分层设计
```sql
-- ODS层：操作数据层
CREATE TABLE ods_order (
    order_id STRING,
    user_id BIGINT,
    product_id STRING,
    order_time TIMESTAMP,
    amount DECIMAL(10,2),
    status STRING
) COMMENT 'ODS层-订单表'
PARTITIONED BY (dt STRING);

-- DWD层：明细数据层
CREATE TABLE dwd_order_detail (
    order_id STRING,
    user_id BIGINT,
    user_name STRING,
    product_id STRING,
    product_name STRING,
    category STRING,
    order_time TIMESTAMP,
    amount DECIMAL(10,2),
    quantity INT,
    status STRING
) COMMENT 'DWD层-订单明细表'
PARTITIONED BY (dt STRING);

-- DWS层：汇总数据层
CREATE TABLE dws_user_order_1d (
    user_id BIGINT,
    order_count BIGINT,
    order_amount DECIMAL(10,2),
    order_quantity INT,
    first_order_time TIMESTAMP,
    last_order_time TIMESTAMP
) COMMENT 'DWS层-用户每日订单汇总'
PARTITIONED BY (dt STRING);

-- ADS层：应用数据层
CREATE TABLE ads_order_stats (
    stat_date DATE,
    total_orders BIGINT,
    total_amount DECIMAL(10,2),
    new_users BIGINT,
    active_users BIGINT,
    avg_order_amount DECIMAL(10,2)
) COMMENT 'ADS层-订单统计'
PARTITIONED BY (dt STRING);
```

## 最佳实践

### 性能优化
```markdown
## SQL优化
1. 分区裁剪：WHERE dt = '20240101'
2. 列裁剪：只选择需要的列
3. 谓词下推：过滤条件尽早执行
4. Join优化：小表JOIN大表用MapJoin
5. 数据倾斜：加盐、分桶

## 存储优化
1. 分区策略：按日期、业务分区
2. 分桶策略：按关键字段分桶
3. 文件格式：Parquet、ORC列式存储
4. 压缩算法：Snappy、ZSTD
5. 数据生命周期：冷热数据分离

## 计算优化
1. 资源配置：合理分配内存、CPU
2. 并行度调整：适当增加并行度
3. 缓存策略：中间结果缓存
4. 数据本地性：减少数据传输
```

### 数据治理
```markdown
## 元数据管理
- 表定义、字段说明
- 数据血缘关系
- 数据质量规则
- 数据更新频率

## 数据质量
- 准确性：数据正确无误
- 完整性：无缺失数据
- 一致性：符合业务规则
- 及时性：数据更新及时

## 数据安全
- 访问控制：基于角色的权限
- 数据脱敏：敏感信息脱敏
- 审计日志：操作记录追溯
- 数据备份：定期备份恢复
```

## Vibe Engineering实践

### 自动化优先
- 自动化数据pipeline
- 自动化质量检查
- 自动化告警通知
- 减少人工干预

### 可观测性
- Pipeline监控
- 数据质量监控
- 性能指标监控
- 成本监控

### 敏捷迭代
- 快速响应需求
- 增量开发
- 持续优化
- 技术债管理

## 日常工作流程

### 数据工程师的一天
```
09:00-09:30  查看pipeline运行状态和告警
09:30-10:00  站会，同步进度
10:00-12:00  数据开发/优化工作
12:00-13:30  午餐和休息
13:30-15:00  数据需求评审/方案设计
15:00-16:00  问题排查和修复
16:00-17:00  数据质量巡检
17:00-18:00  文档整理和技术分享
18:00-      值班待命（轮值）
```

## 成长路径
1. **初级数据工程师**：ETL开发、数据同步
2. **中级数据工程师**：数据建模、性能优化
3. **高级数据工程师**：架构设计、平台建设
4. **数据架构师**：数据战略规划、技术引领
