<!--
## Sync Impact Report
- **Version Change**: v1.2.0 → v1.3.0
- **Change Type**: MINOR (新增行尾注释禁止规范)
- **Modified Principles**:
  - II. 命名规范 → 注释规范部分新增行尾注释禁止要求及代码示例
- **Added Sections**:
  - 行尾注释禁止规范（正确/错误示例）
- **Removed Sections**: 无
- **Templates Requiring Updates**:
  - `.specify/templates/plan-template.md` ✅ 兼容
  - `.specify/templates/spec-template.md` ✅ 兼容
  - `.specify/templates/tasks-template.md` ✅ 兼容
- **Follow-up TODOs**: 无
-->

# MRP Policy Center 编码规约

## Core Principles

### I. 分层架构规范

项目采用多模块分层架构，MUST 严格遵循以下规范：

**模块划分**：
- `mrp-policy-api`：对外暴露的API模块，仅包含DTO和Feign接口定义
  - `api/dto/`：请求和响应数据传输对象（命名：`*ReqDTO`、`*RespDTO`）
  - `api/feign/`：Feign客户端接口定义（命名：`*Feign`）
- `mrp-policy-service`：服务实现模块

**分层调用规则**（上层只能调用下层，禁止跨层或反向调用）：

```
Controller → Business → Service → DAO → Mapper
```

- `controller/`：REST接口层，实现Feign接口，仅负责请求转发和响应封装
- `business/`：业务编排层，处理复杂业务逻辑，命名为 `*Business`
- `service/`：服务层，处理单一职责业务，命名为 `*Service`
- `dao/`：数据访问层，封装Mapper操作和缓存逻辑，命名为 `*DAO`
- `dao/mapper/`：MyBatis Mapper接口，命名为 `*Mapper`
- `dao/entity/`：数据库实体类，命名为 `*Entity`

**依赖规则**：
- 上层可以依赖下层，下层 MUST NOT 依赖上层
- 同层之间 SHOULD 避免相互依赖，必要时通过上层协调

### II. 命名规范

所有代码 MUST 遵循以下命名规范以保持项目一致性：

**类命名规则**：

| 类型 | 命名规则 | 示例 |
|------|----------|------|
| Controller | `*Controller` | `PolicyQueryController` |
| Business | `*Business` | `MrpPolicyRuleBusiness` |
| Service | `*Service` | `MrpPolicyBaseInfoService` |
| DAO | `*DAO` | `PolicyGoodsPoolDAO` |
| Mapper | `*Mapper` | `PolicyGoodsPoolMapper` |
| Entity | `*Entity` | `PolicyGoodsPoolEntity` |
| DTO请求 | `*ReqDTO` | `QueryPolicyBaseInfoReqDTO` |
| DTO响应 | `*RespDTO` | `QueryPolicyBaseInfoRespDTO` |
| BO | `*BO` | `ActivityStoreGoodsAddBO` |
| Feign接口 | `*Feign` | `MrpPolicyQueryFeign` |
| 枚举 | `*Enum` / `*Enums` | `BatchTypeEnums`, `PolicyCashFlagEnum` |
| 常量类 | `*Constants` | `RedisConstants`, `PolicyConstants` |
| 消息消费者 | `*Consumer` | `BaseRocketmqConsumer` |
| 定时任务 | `*Job` | `PolicyCacheRefreshJob` |

**包命名规则**：
- 基础包名：`com.midea.mrp.policy`（零售政策）、`com.midea.mrp.scpolicy`（市场政策）
- 所有包名使用小写字母，多词使用单词组合，不使用下划线

**方法命名规则**：

| 场景 | 前缀 | 示例 |
|------|------|------|
| 查询单个 | `queryBy*`, `get*` | `queryByCode()`, `getPolicyBaseInfo()` |
| 查询列表 | `query*List`, `list*` | `queryPolicyGoodsPoolLimit()` |
| 新增 | `add*`, `insert*`, `save*` | `addPolicyGoodsPool()` |
| 批量保存 | `batchSave*`, `insertBatch*` | `batchSave()` |
| 更新 | `update*` | `updatePolicyGoodsEffectiveFlag()` |
| 删除 | `delete*` | `deleteByPolicyAndExtGoods()` |
| 构建对象 | `build*` | `buildBaseInfoEntity()` |
| 校验 | `check*`, `validate*` | `checkPolicyRuleParams()` |

**注释规范**：
- 所有类 MUST 添加类级别的 Javadoc 注释，说明类的职责和用途
- 所有公共方法 MUST 添加 Javadoc 注释，说明方法功能、参数和返回值
- 复杂业务逻辑处需添加行内注释说明
- MUST NOT 使用行尾注释，注释应单独成行置于代码上方

```java
// 正确示例 - 注释单独成行
// 查询商品池数据
List<PolicyGoodsPoolEntity> poolList = mapper.selectList(wrapper);

// 错误示例 - 不要使用行尾注释
List<PolicyGoodsPoolEntity> poolList = mapper.selectList(wrapper); // 查询商品池数据
```

```java
/**
 * 政策商品池数据访问对象
 * 负责政策商品池的CRUD操作和缓存管理
 *
 * @author xxx
 * @since 2025-01-01
 */
@Repository
public class PolicyGoodsPoolDAO {

    /**
     * 根据政策编码查询商品池列表
     *
     * @param policyCode 政策编码
     * @return 商品池列表，如果不存在返回空列表
     */
    public List<PolicyGoodsPoolEntity> queryByPolicyCode(String policyCode) {
        // 业务逻辑
    }
}
```

### III. 统一响应与请求封装

所有对外接口 MUST 遵循以下规范：

**请求封装**：
- 所有请求使用 `MrpCommonRequest<T>` 包装
- 分页请求使用 `MrpPaginationRequest<T>` 包装
- 请求参数通过 `@RequestBody @Validated` 校验

```java
// 正确示例
@PostMapping(value = "/queryPolicyBaseInfo")
public MrpCommonResponse<QueryPolicyBaseInfoRespDTO> queryPolicyBaseInfo(
    @RequestBody @Validated MrpCommonRequest<QueryPolicyBaseInfoReqDTO> request) {
    return business.queryPolicyBaseInfo(request.getRestParams());
}
```

**响应封装**：
- 所有响应使用 `MrpCommonResponse<T>` 包装
- 分页响应使用 `MrpPaginationResponse<T>` 包装
- 错误响应使用 `MrpCommonResponse.getFailResponse(ResultCode.*)` 返回

**Feign接口规范**：
- 接口定义在 `mrp-policy-api` 模块的 `api/feign/` 包下
- 使用 `@FeignClient(value = "mrp-policy-service", path = "/mrp-policy-service/...")` 注解
- 方法需添加 `@ApiOperation` 注解说明用途
- Controller MUST 实现对应的Feign接口

### IV. 数据访问规范

数据访问层 MUST 遵循以下规范：

**MyBatis-Plus使用规范**：
- Entity类使用 `@Data @Builder @NoArgsConstructor @AllArgsConstructor` 注解
- 表名使用 `@TableName("table_name")` 注解
- 主键使用 `@TableId(value = "id", type = IdType.AUTO)` 注解
- 字段使用 `@TableField(value = "column_name")` 注解

**DAO层规范**：
- DAO类使用 `@Repository` 注解
- DAO封装Mapper调用和缓存逻辑
- 复杂查询SQL写在Mapper XML中（路径：`resources/mapper/*.xml`）

**Redis缓存策略**：
- 缓存Key统一定义在 `RedisConstants` 常量类中
- 使用 `MessageFormat.format()` 构建动态Key
- 分布式锁使用 `RedisLockHelper.tryLock()` 获取
- 缓存操作封装在DAO层

```java
// 常量定义示例
interface CacheKey {
    String POLICY_GOODS_POOL_HASH_KEY = "POLICY:GOODS_POOL:{0}";
}

// 使用示例
String key = MessageFormat.format(RedisConstants.CacheKey.POLICY_GOODS_POOL_HASH_KEY, policyCode);
```

**事务管理**：
- 服务层方法需要事务时使用 `@Transactional` 注解
- 只读查询使用 `@Transactional(readOnly = true)`
- 跨服务调用 MUST NOT 在同一事务中

### V. 消息队列与异步处理

**RocketMQ消费者规范**：
- 继承 `BaseRocketmqConsumer<T>` 基类
- 使用 `@RocketMQMessageListener` 注解配置topic和consumerGroup
- 实现消息幂等性处理
- 异常消息自动进入重试队列

**XXL-Job定时任务规范**：
- 继承 `IJobHandler` 基类
- 使用 `@XxlJob("jobName")` 注解
- 使用分布式锁防止重复执行
- 执行结果发送告警通知

```java
@Component
@Slf4j
public class PolicyCacheRefreshJob extends IJobHandler {
    @Override
    @XxlJob("policyCacheRefreshJob")
    public ReturnT<String> execute(String params) {
        // 业务逻辑
        return ReturnT.SUCCESS;
    }
}
```

**日志规范**：
- 类级别使用 `@Slf4j` 注解
- 关键业务操作需记录日志
- 异常信息使用 `log.error("message", exception)` 记录完整堆栈
- 敏感信息脱敏处理
- Debug日志规范：
  - 打印对象优先使用默认 `toString()`，避免 JSON 序列化
  - 使用参数化日志，避免在占位符中进行计算
  - 使用 `log.isDebugEnabled()` 判断后再打印debug日志

```java
// 正确示例
if (log.isDebugEnabled()) {
    log.debug("业务对象 req={}", req);
}

// 错误示例 - 不要这样写
log.debug("业务对象 req={}", JsonUtils.toJsonString(req));
```

## 代码结构规范

### 技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Java | 1.8 | JDK版本 |
| Spring Boot | 2.x | 基于 mrp-starter-parent:2.0.3-RELEASE |
| Spring Cloud | - | OpenFeign服务调用 |
| MyBatis-Plus | - | ORM框架 |
| RocketMQ | - | 消息队列 |
| Redis/Redisson | - | 缓存与分布式锁 |
| XXL-Job | - | 分布式任务调度 |
| Lombok | - | 简化代码 |
| Guava | - | 工具库 |

### 依赖管理

- 父POM继承 `mrp-starter-parent`
- 版本号使用属性统一管理
- SNAPSHOT版本用于开发/测试环境
- RELEASE版本用于生产环境

### 项目目录结构

```
mrp-policy-center/
├── mrp-policy-api/                  # API模块
│   └── src/main/java/com/midea/mrp/policy/api/
│       ├── dto/                     # 数据传输对象
│       │   ├── request/             # 请求DTO
│       │   └── response/            # 响应DTO
│       └── feign/                   # Feign接口
│
└── mrp-policy-service/              # 服务模块
    └── src/main/java/com/midea/mrp/policy/
        ├── aop/                     # 切面
        ├── bo/                      # 业务对象
        ├── business/                # 业务编排层
        ├── common/                  # 公共组件
        ├── config/                  # 配置类
        ├── constants/               # 常量定义
        ├── controller/              # 控制器层
        ├── convert/                 # 对象转换器
        ├── dao/                     # 数据访问层
        │   ├── entity/              # 数据库实体
        │   └── mapper/              # MyBatis Mapper
        ├── enums/                   # 枚举定义
        ├── event/                   # 事件处理
        ├── interceptor/             # 拦截器
        ├── job/                     # 定时任务
        ├── mq/                      # 消息队列
        │   └── listener/            # 消息监听器
        ├── service/                 # 服务层
        └── utils/                   # 工具类
```

## Development Workflow

### 代码审查

- 所有代码变更需经过Code Review
- 遵循分层架构，禁止跨层调用
- 新增接口 MUST 在 `mrp-policy-api` 定义Feign接口
- DTO与Entity之间使用Convert转换

### 测试要求

- 核心业务逻辑需要单元测试
- 接口变更需要集成测试验证
- 定时任务和消息消费需要手动验证

### 质量门禁

- 代码编译无错误
- 无明显的代码规范违规
- 关键路径有日志记录
- 分布式场景考虑幂等性

## Governance

### 规约生效范围

本规约适用于 `mrp-policy-center` 项目的所有新增和修改代码。

### 修订流程

1. 提出修订建议并说明理由
2. 团队评审通过
3. 更新本文档并记录修订历史

### Version Policy

- **MAJOR**: 删除或重定义核心原则，不兼容变更
- **MINOR**: 新增原则/章节或实质性扩展指导
- **PATCH**: 澄清、措辞优化、错别字修复

### 例外处理

特殊情况需要偏离规约时，需在代码中添加注释说明原因，并在Code Review时获得批准。

**Version**: 1.3.0 | **Ratified**: 2025-12-24 | **Last Amended**: 2026-01-19
