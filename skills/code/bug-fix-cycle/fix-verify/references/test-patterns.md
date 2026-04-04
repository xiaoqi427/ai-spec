# 单元测试模式参考

## 项目测试框架

| 组件 | 版本 | 说明 |
|------|------|------|
| JUnit 5 (Jupiter) | 由 Spring Boot 3.5.6 管理 | 测试框架 |
| Mockito | 由 Spring Boot 3.5.6 管理 | Mock 框架 |
| AssertJ | 由 Spring Boot 3.5.6 管理 | 流畅断言 |
| spring-boot-starter-test | 3.5.6 | 聚合依赖 |
| Java | 21 | 运行环境 |

## 测试类命名约定

| 源文件 | 测试文件 | 说明 |
|--------|---------|------|
| `XxxServiceImpl.java` | `XxxServiceImplTest.java` | Service 实现类 |
| `XxxDoServiceImpl.java` | `XxxDoServiceImplTest.java` | DO Service 实现类 |
| `XxxBusiness.java` | `XxxBusinessTest.java` | Business 层 |
| `XxxController.java` | `XxxControllerTest.java` | Controller 层 (可选) |
| `XxxUtil.java` | `XxxUtilTest.java` | 工具类 |
| `XxxDtoConverter.java` | `XxxDtoConverterTest.java` | 转换器 |

## 测试目录结构

```
fssc-claim-service/
├── claim-otc/
│   └── claim-otc-service/
│       ├── src/main/java/com/yili/claim/otc/claim/t047/head/impl/
│       │   └── T047NewClaimServiceImpl.java           ← 源文件
│       └── src/test/java/com/yili/claim/otc/claim/t047/head/impl/
│           └── T047NewClaimServiceImplTest.java        ← 测试文件
```

规则：测试类与源文件**镜像包结构**，即 `src/main/java/...` 对应 `src/test/java/...`。

## 测试类编写规范

### 基础模板

```java
package com.yili.claim.otc.claim.t047.head.impl;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Nested;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import lombok.extern.slf4j.Slf4j;

import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.mockito.Mockito.*;

/**
 * XxxServiceImpl 单元测试
 *
 * @author sevenxiao
 */
@Slf4j
@ExtendWith(MockitoExtension.class)
@DisplayName("XxxServiceImpl 单元测试")
class XxxServiceImplTest {

    @InjectMocks
    private XxxServiceImpl xxxService;

    @Mock
    private IYyyDoService yyyDoService;

    @Nested
    @DisplayName("methodName 方法")
    class MethodNameTest {

        @Test
        @DisplayName("正常情况 - 应该返回正确结果")
        void should_return_correct_result_when_valid_input() {
            // Given
            when(yyyDoService.findById(anyLong())).thenReturn(mockData);

            // When
            var result = xxxService.methodName(input);

            // Then
            assertThat(result).isNotNull();
            verify(yyyDoService).findById(anyLong());
        }

        @Test
        @DisplayName("异常情况 - 参数为空应该抛异常")
        void should_throw_exception_when_null_input() {
            assertThatThrownBy(() -> xxxService.methodName(null))
                .isInstanceOf(I18nException.class);
        }
    }
}
```

### 关键注解

| 注解 | 用途 |
|------|------|
| `@ExtendWith(MockitoExtension.class)` | 启用 Mockito |
| `@InjectMocks` | 自动注入被测类 |
| `@Mock` | Mock 依赖 |
| `@DisplayName("中文描述")` | 测试显示名 |
| `@Nested` | 嵌套测试类，按方法分组 |
| `@BeforeEach` | 每个测试前的初始化 |
| `@Test` | 标记测试方法 |

### 断言风格

```java
// AssertJ 链式断言（推荐）
assertThat(result).isNotNull();
assertThat(result.getAmount()).isEqualByComparingTo(new BigDecimal("100.00"));
assertThat(list).hasSize(3).extracting("name").contains("T047");

// 异常断言
assertThatThrownBy(() -> service.process(null))
    .isInstanceOf(I18nException.class)
    .hasMessageContaining("参数不能为空");
```

### 测试方法命名

格式: `should_<预期行为>_when_<条件>`

```java
should_return_success_when_valid_input()
should_throw_exception_when_null_param()
should_calculate_correct_amount_when_multi_items()
should_set_default_value_when_field_is_empty()
```

## Maven 测试命令

### 运行指定测试类

```bash
# 单个测试类
mvn test -pl claim-otc/claim-otc-service \
  -Dtest=T047NewClaimServiceImplTest \
  -DskipTests=false \
  -Dmaven.test.skip=false

# 多个测试类（逗号分隔）
mvn test -pl claim-otc/claim-otc-service \
  -Dtest=T047NewClaimServiceImplTest,T047LoadClaimServiceImplTest \
  -DskipTests=false \
  -Dmaven.test.skip=false \
  -T 1C

# 带通配符
mvn test -pl claim-otc/claim-otc-service \
  -Dtest="T047*Test" \
  -DskipTests=false \
  -Dmaven.test.skip=false
```

### 重要参数

| 参数 | 说明 |
|------|------|
| `-pl <module>` | 指定模块（相对路径） |
| `-Dtest=<Class>` | 指定测试类名（支持通配符） |
| `-DskipTests=false` | 覆盖 pom 中的 skipTests=true |
| `-Dmaven.test.skip=false` | 覆盖 pom 中的 maven.test.skip |
| `-T 1C` | 按 CPU 核数并行构建 |
| `--fail-at-end` | 所有模块跑完再报错 |

### 注意事项

1. 项目 pom.xml 中默认配置 `<skipTests>true</skipTests>`，必须用 `-DskipTests=false` 覆盖
2. 同时需要 `-Dmaven.test.skip=false`，否则 maven-surefire-plugin 可能仍跳过
3. `-pl` 参数中模块路径是从项目根目录（如 `fssc-claim-service`）开始的相对路径

## Surefire 报告

### 报告路径

```
<module>/target/surefire-reports/
├── TEST-com.yili.claim.otc.claim.t047.head.impl.T047NewClaimServiceImplTest.xml
├── com.yili.claim.otc.claim.t047.head.impl.T047NewClaimServiceImplTest.txt
└── ...
```

### XML 结构

```xml
<?xml version="1.0" encoding="UTF-8"?>
<testsuite xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
           xsi:noNamespaceSchemaLocation="...surefire-test-report-3.0.xsd"
           version="3.0"
           name="com.yili.claim.otc.claim.t047.head.impl.T047NewClaimServiceImplTest"
           time="3.456"
           tests="10"
           errors="0"
           skipped="2"
           failures="1">

  <testcase name="should_return_success_when_valid_input"
            classname="...T047NewClaimServiceImplTest"
            time="0.123"/>

  <testcase name="should_throw_when_null"
            classname="...T047NewClaimServiceImplTest"
            time="0.234">
    <failure message="Expected exception" type="org.opentest4j.AssertionFailedError">
      <![CDATA[stack trace...]]>
    </failure>
  </testcase>

  <testcase name="should_skip_when_disabled"
            classname="...T047NewClaimServiceImplTest"
            time="0">
    <skipped/>
  </testcase>
</testsuite>
```

### 解析关键字段

| 字段 | 含义 |
|------|------|
| `tests` | 测试总数 |
| `failures` | 断言失败数 |
| `errors` | 运行时错误数 |
| `skipped` | 跳过数 |
| `time` | 执行耗时(秒) |
| `testcase > failure` | 失败详情（message + 堆栈） |

## 现有测试示例

| 测试类 | 模块 | 行数 | 说明 |
|--------|------|------|------|
| `T047NewClaimServiceImplTest` | claim-otc/claim-otc-service | ~326 | T047 新建报账单测试 |
| `T047LoadClaimServiceImplTest` | claim-otc/claim-otc-service | ~505 | T047 加载报账单测试 |
| `T047QuyInvItemInfoServiceImplTest` | claim-otc/claim-otc-service | ~84 | T047 查询发票项测试 |
| `IT017SaveClaimServiceImplTest` | claim-eer/claim-eer-service | ~268 | IT017 保存报账单测试 |

这些测试都使用 JUnit 5 + Mockito + AssertJ 编写，可作为新测试的参考模板。
