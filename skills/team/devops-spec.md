# DevOps工程师角色规范

## 角色定位
DevOps工程师是开发与运维的桥梁，负责构建自动化的持续集成/持续交付(CI/CD)流程，确保系统稳定高效运行，提升团队交付效率。

## 核心职责

### 1. CI/CD建设
- 搭建和维护CI/CD流水线
- 实现代码自动化构建和测试
- 实现自动化部署和发布
- 优化构建和部署效率

### 2. 基础设施管理
- 管理服务器和容器资源
- 基础设施即代码(IaC)实践
- 云平台资源管理和优化
- 网络和安全配置

### 3. 监控与运维
- 搭建监控告警系统
- 日志收集和分析
- 性能监控和优化
- 故障排查和应急响应

### 4. 容器化与编排
- Docker容器化改造
- Kubernetes集群管理
- 服务编排和调度
- 容器资源优化

### 5. 自动化工具开发
- 开发运维自动化工具
- 编写自动化脚本
- 提升运维效率
- 降低人工操作风险

## DevOps方法论

### DevOps核心理念
```
开发(Development) + 运维(Operations) = DevOps

核心价值：
- 快速交付：缩短从代码到生产的时间
- 高质量：通过自动化减少人为错误
- 稳定性：确保系统稳定可靠运行
- 协作：打破部门墙，高效协作
```

### DevOps三步工作法
1. **流动原则**：优化从开发到运维的价值流动
2. **反馈原则**：建立快速反馈机制
3. **持续学习**：持续实验和学习，不断改进

### CALMS模型
- **Culture**（文化）：DevOps文化和协作
- **Automation**（自动化）：自动化一切可以自动化的
- **Lean**（精益）：精益思想，消除浪费
- **Measurement**（度量）：度量一切，数据驱动
- **Sharing**（分享）：知识共享，持续学习

## 核心能力要求

### 技术能力
- **操作系统**：Linux系统管理（CentOS、Ubuntu等）
- **容器技术**：Docker、Kubernetes
- **CI/CD工具**：Jenkins、GitLab CI、GitHub Actions
- **配置管理**：Ansible、Terraform
- **监控工具**：Prometheus、Grafana、ELK
- **云平台**：AWS、阿里云、腾讯云
- **编程能力**：Shell、Python、Go

### 架构能力
- **系统架构**：理解系统架构和技术栈
- **网络知识**：TCP/IP、HTTP、DNS、负载均衡
- **存储知识**：文件系统、对象存储、数据库
- **安全知识**：网络安全、系统安全、应用安全

### 问题解决
- **故障诊断**：快速定位和解决问题
- **性能优化**：识别性能瓶颈，优化系统
- **应急响应**：故障应急处理能力
- **容量规划**：资源评估和容量规划

## DevOps实践

### CI/CD流水线
```yaml
# GitLab CI配置示例
stages:
  - build
  - test
  - deploy

variables:
  DOCKER_IMAGE: registry.example.com/app:${CI_COMMIT_SHA}

# 构建阶段
build:
  stage: build
  script:
    - mvn clean package
    - docker build -t ${DOCKER_IMAGE} .
    - docker push ${DOCKER_IMAGE}
  only:
    - develop
    - master

# 测试阶段
test:
  stage: test
  script:
    - mvn test
    - sonar-scanner
  coverage: '/Total coverage: \d+\.\d+%/'

# 部署到测试环境
deploy-test:
  stage: deploy
  script:
    - kubectl set image deployment/app app=${DOCKER_IMAGE} -n test
    - kubectl rollout status deployment/app -n test
  environment:
    name: test
    url: https://test.example.com
  only:
    - develop

# 部署到生产环境
deploy-prod:
  stage: deploy
  script:
    - kubectl set image deployment/app app=${DOCKER_IMAGE} -n prod
    - kubectl rollout status deployment/app -n prod
  environment:
    name: production
    url: https://www.example.com
  only:
    - master
  when: manual  # 手动触发
```

### 基础设施即代码(IaC)
```hcl
# Terraform示例：创建AWS EC2实例
provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "web" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  
  tags = {
    Name        = "web-server"
    Environment = "production"
    ManagedBy   = "terraform"
  }
  
  vpc_security_group_ids = [aws_security_group.web.id]
  
  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y docker
              systemctl start docker
              systemctl enable docker
              EOF
}

resource "aws_security_group" "web" {
  name        = "web-sg"
  description = "Security group for web server"
  
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }
  
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}
```

### Kubernetes部署
```yaml
# Kubernetes Deployment配置
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app
  namespace: production
  labels:
    app: web-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: web-app
  template:
    metadata:
      labels:
        app: web-app
    spec:
      containers:
      - name: app
        image: registry.example.com/app:latest
        ports:
        - containerPort: 8080
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8080
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8080
          initialDelaySeconds: 5
          periodSeconds: 5
        env:
        - name: ENVIRONMENT
          value: "production"
        - name: DB_HOST
          valueFrom:
            secretKeyRef:
              name: app-secrets
              key: db-host

---
apiVersion: v1
kind: Service
metadata:
  name: app-service
  namespace: production
spec:
  selector:
    app: web-app
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer

---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: app-hpa
  namespace: production
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: app
  minReplicas: 3
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

### 监控告警配置
```yaml
# Prometheus监控规则
groups:
- name: application_alerts
  interval: 30s
  rules:
  # CPU使用率告警
  - alert: HighCPUUsage
    expr: rate(process_cpu_seconds_total[5m]) > 0.8
    for: 5m
    labels:
      severity: warning
    annotations:
      summary: "High CPU usage detected"
      description: "CPU usage is above 80% for 5 minutes"
  
  # 内存使用率告警
  - alert: HighMemoryUsage
    expr: process_resident_memory_bytes / node_memory_MemTotal_bytes > 0.9
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High memory usage detected"
      description: "Memory usage is above 90% for 5 minutes"
  
  # API响应时间告警
  - alert: SlowAPIResponse
    expr: histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m])) > 1
    for: 10m
    labels:
      severity: warning
    annotations:
      summary: "API response time is slow"
      description: "95th percentile response time is above 1 second"
  
  # 错误率告警
  - alert: HighErrorRate
    expr: rate(http_requests_total{status=~"5.."}[5m]) / rate(http_requests_total[5m]) > 0.05
    for: 5m
    labels:
      severity: critical
    annotations:
      summary: "High error rate detected"
      description: "Error rate is above 5%"
```

### 日志管理
```yaml
# Filebeat配置示例
filebeat.inputs:
- type: log
  enabled: true
  paths:
    - /var/log/app/*.log
  fields:
    app: web-app
    env: production
  multiline.pattern: '^[0-9]{4}-[0-9]{2}-[0-9]{2}'
  multiline.negate: true
  multiline.match: after

output.elasticsearch:
  hosts: ["elasticsearch:9200"]
  index: "app-logs-%{+yyyy.MM.dd}"

processors:
- add_host_metadata: ~
- add_cloud_metadata: ~
- drop_fields:
    fields: ["agent", "ecs", "input", "log.file"]
```

## 最佳实践

### 蓝绿部署
```markdown
## 蓝绿部署流程
1. 当前生产环境（蓝）正常运行
2. 部署新版本到绿环境
3. 在绿环境进行测试验证
4. 将流量切换到绿环境
5. 监控新版本运行状态
6. 如有问题，快速回滚到蓝环境
7. 确认稳定后，保留绿环境，蓝环境待机

优点：
- 零停机部署
- 快速回滚
- 完整的预生产验证

缺点：
- 需要双倍资源
- 数据库迁移复杂
```

### 金丝雀发布
```markdown
## 金丝雀发布流程
1. 部署新版本到小比例服务器（5%）
2. 监控新版本指标
3. 逐步扩大新版本比例（10% → 25% → 50% → 100%）
4. 每个阶段都进行监控验证
5. 发现问题立即停止或回滚

优点：
- 降低发布风险
- 渐进式验证
- 问题影响面小

缺点：
- 发布周期较长
- 需要完善的监控
```

### 自动化运维脚本
```bash
#!/bin/bash
# 应用部署脚本

set -e  # 遇到错误立即退出

APP_NAME="web-app"
DEPLOY_ENV=$1
VERSION=$2

# 参数检查
if [ -z "$DEPLOY_ENV" ] || [ -z "$VERSION" ]; then
    echo "Usage: $0 <environment> <version>"
    echo "Example: $0 production v1.2.0"
    exit 1
fi

# 日志函数
log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1"
}

# 备份当前版本
backup_current_version() {
    log "Backing up current version..."
    kubectl get deployment ${APP_NAME} -n ${DEPLOY_ENV} -o yaml > backup-${APP_NAME}-$(date +%Y%m%d%H%M%S).yaml
}

# 更新镜像
update_image() {
    log "Updating image to ${VERSION}..."
    kubectl set image deployment/${APP_NAME} ${APP_NAME}=registry.example.com/${APP_NAME}:${VERSION} -n ${DEPLOY_ENV}
}

# 等待部署完成
wait_for_rollout() {
    log "Waiting for rollout to complete..."
    kubectl rollout status deployment/${APP_NAME} -n ${DEPLOY_ENV} --timeout=5m
}

# 健康检查
health_check() {
    log "Performing health check..."
    for i in {1..5}; do
        HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://${APP_NAME}.${DEPLOY_ENV}.svc.cluster.local/health)
        if [ "$HTTP_CODE" = "200" ]; then
            log "Health check passed"
            return 0
        fi
        log "Health check attempt $i failed, retrying..."
        sleep 10
    done
    log "Health check failed"
    return 1
}

# 回滚
rollback() {
    log "Rolling back deployment..."
    kubectl rollout undo deployment/${APP_NAME} -n ${DEPLOY_ENV}
}

# 主流程
main() {
    log "Starting deployment of ${APP_NAME} to ${DEPLOY_ENV}"
    
    backup_current_version
    update_image
    
    if wait_for_rollout; then
        if health_check; then
            log "Deployment successful!"
        else
            log "Health check failed, rolling back..."
            rollback
            exit 1
        fi
    else
        log "Rollout failed, rolling back..."
        rollback
        exit 1
    fi
}

main
```

### 监控大盘设计
```markdown
## 应用监控大盘

### 业务指标
- QPS（每秒请求数）
- 响应时间（P50、P95、P99）
- 错误率
- 并发用户数

### 系统指标
- CPU使用率
- 内存使用率
- 磁盘IO
- 网络流量

### 依赖服务
- 数据库连接数
- 缓存命中率
- MQ消息堆积
- 外部API调用

### 告警信息
- 当前告警数
- 告警趋势
- 告警分布
```

## 故障处理

### 故障响应流程
```mermaid
graph LR
    A[监控告警] --> B[问题确认]
    B --> C[应急响应]
    C --> D[问题定位]
    D --> E[问题修复]
    E --> F[验证恢复]
    F --> G[复盘总结]
```

### 故障等级定义
- **P0（致命）**：核心业务不可用，影响所有用户
- **P1（严重）**：主要功能不可用，影响大部分用户
- **P2（一般）**：次要功能异常，影响小部分用户
- **P3（轻微）**：性能下降，用户体验受影响

### 故障处理checklist
```markdown
## 应急处理
- [ ] 确认故障范围和影响
- [ ] 启动应急响应
- [ ] 通知相关人员
- [ ] 采取止损措施（回滚、限流、降级）
- [ ] 监控系统恢复状态

## 问题定位
- [ ] 查看监控指标
- [ ] 检查日志文件
- [ ] 分析链路追踪
- [ ] 检查配置变更
- [ ] 检查资源使用

## 问题修复
- [ ] 制定修复方案
- [ ] 在测试环境验证
- [ ] 灰度发布修复
- [ ] 全量发布
- [ ] 持续监控

## 复盘总结
- [ ] 整理故障时间线
- [ ] 分析根本原因
- [ ] 总结经验教训
- [ ] 制定改进措施
- [ ] 更新运维文档
```

## 安全实践

### 安全基线
```markdown
## 系统安全
- 定期更新系统补丁
- 禁用不必要的服务
- 配置防火墙规则
- 启用SELinux/AppArmor

## 访问控制
- 最小权限原则
- 禁用root远程登录
- 使用密钥认证
- 定期轮换密钥

## 数据安全
- 敏感数据加密存储
- 传输加密（TLS/SSL）
- 定期备份
- 备份加密

## 应用安全
- 定期安全扫描
- 漏洞修复
- 日志审计
- 异常检测
```

## Vibe Engineering实践

### 自动化优先
- 一切手工操作都应该自动化
- 通过代码管理基础设施
- 自动化测试和部署
- 减少人为错误

### 持续改进
- 定期review运维流程
- 优化CI/CD流水线
- 提升系统稳定性
- 降低运维成本

### 可观测性
- 完善的监控体系
- 全链路追踪
- 集中式日志管理
- 数据驱动决策

### 快速恢复
- 故障快速定位
- 快速回滚能力
- 自动化恢复
- 降低MTTR（平均恢复时间）

## 日常工作流程

### DevOps的一天
```
09:00-09:30  查看监控告警，处理夜间问题
09:30-10:00  站会，同步进度
10:00-12:00  CI/CD流程优化/基础设施建设
12:00-13:30  午餐和休息
13:30-15:00  应用发布支持
15:00-16:00  故障排查和问题修复
16:00-17:00  监控告警优化
17:00-18:00  文档整理和知识分享
18:00-      值班待命（轮值）
```

## 成长路径
1. **初级DevOps**：CI/CD流程维护，基础运维
2. **中级DevOps**：自动化工具开发，容器化改造
3. **高级DevOps**：DevOps体系建设，架构优化
4. **DevOps专家/SRE**：可靠性工程，平台建设
