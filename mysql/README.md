# 鲲擎校园管理系统 - 数据库文档

## 概述

本目录包含鲲擎校园管理系统的MySQL数据库相关文件，包括数据库结构创建脚本、示例数据插入脚本等。

## 文件说明

### 1. create_database.sql
数据库结构创建脚本，包含：
- 数据库创建
- 所有数据表结构定义
- 索引和外键约束
- 表注释和字段注释

### 2. sample_data.sql
示例数据插入脚本，包含：
- 测试用户数据
- 课程信息
- 失物招领记录
- 二手书信息
- 学习小组数据
- 系统配置信息

## 数据库结构

### 核心表结构

#### 用户表 (users)
存储用户基本信息，包括学号、邮箱、密码等。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT | 主键，自增 |
| student_id | VARCHAR(20) | 学号，唯一 |
| email | VARCHAR(100) | 邮箱，唯一 |
| password | VARCHAR(255) | 加密密码 |
| real_name | VARCHAR(50) | 真实姓名 |
| college | VARCHAR(100) | 学院 |
| major | VARCHAR(100) | 专业 |
| grade | VARCHAR(20) | 年级 |

#### 失物招领表 (lost_found)
存储失物招领信息。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT | 主键，自增 |
| user_id | INT | 发布用户ID |
| type | ENUM | 类型：lost/found |
| title | VARCHAR(200) | 标题 |
| description | TEXT | 详细描述 |
| location | VARCHAR(200) | 地点 |
| status | ENUM | 状态：open/closed/resolved |

#### 二手书表 (books)
存储二手书交易信息。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT | 主键，自增 |
| user_id | INT | 发布用户ID |
| book_name | VARCHAR(200) | 书名 |
| author | VARCHAR(100) | 作者 |
| price | DECIMAL(10,2) | 价格 |
| condition_desc | VARCHAR(100) | 书籍状态 |
| status | ENUM | 状态：available/sold/reserved |

#### 课程表 (courses)
存储课程基本信息。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT | 主键，自增 |
| course_code | VARCHAR(20) | 课程代码，唯一 |
| course_name | VARCHAR(200) | 课程名称 |
| teacher | VARCHAR(100) | 授课教师 |
| college | VARCHAR(100) | 开课学院 |

#### 学习小组表 (study_groups)
存储学习小组信息。

| 字段名 | 类型 | 说明 |
|--------|------|------|
| id | INT | 主键，自增 |
| user_id | INT | 创建者ID |
| title | VARCHAR(200) | 小组标题 |
| subject | VARCHAR(100) | 学科 |
| goal | TEXT | 学习目标 |
| target_members | INT | 目标成员数 |
| current_members | INT | 当前成员数 |

### 关联表

#### 学习小组成员表 (study_group_members)
存储学习小组成员关系。

#### 课程评价表 (course_reviews)
存储用户对课程的评价。

#### 消息表 (messages)
存储用户间的消息通信。

#### 系统配置表 (system_config)
存储系统配置参数。

## 安装步骤

### 1. 创建数据库
```sql
-- 执行数据库创建脚本
mysql -u root -p < create_database.sql
```

### 2. 插入示例数据（可选）
```sql
-- 插入测试数据
mysql -u root -p kunqing_campus < sample_data.sql
```

### 3. 验证安装
```sql
-- 连接数据库
mysql -u root -p kunqing_campus

-- 查看表结构
SHOW TABLES;

-- 查看数据
SELECT COUNT(*) FROM users;
```

## 数据库配置

### 连接参数
- 数据库名：`kunqing_campus`
- 字符集：`utf8mb4`
- 排序规则：`utf8mb4_unicode_ci`
- 存储引擎：`InnoDB`

### 用户权限
建议为应用程序创建专用数据库用户：

```sql
-- 创建应用用户
CREATE USER 'kunqing_app'@'localhost' IDENTIFIED BY 'your_password';

-- 授予权限
GRANT SELECT, INSERT, UPDATE, DELETE ON kunqing_campus.* TO 'kunqing_app'@'localhost';

-- 刷新权限
FLUSH PRIVILEGES;
```

## 维护说明

### 备份
```bash
# 备份数据库结构和数据
mysqldump -u root -p kunqing_campus > backup_$(date +%Y%m%d).sql

# 仅备份结构
mysqldump -u root -p --no-data kunqing_campus > structure_backup.sql
```

### 性能优化
1. 定期分析表：`ANALYZE TABLE table_name;`
2. 优化表：`OPTIMIZE TABLE table_name;`
3. 监控慢查询日志
4. 根据查询模式添加适当索引

### 数据清理
```sql
-- 清理过期消息（30天前）
DELETE FROM messages WHERE create_time < DATE_SUB(NOW(), INTERVAL 30 DAY) AND type = 'system';

-- 清理已解决的失物招领（90天前）
UPDATE lost_found SET status = 'closed' 
WHERE status = 'resolved' AND create_time < DATE_SUB(NOW(), INTERVAL 90 DAY);
```

## 扩展说明

### 添加新表
1. 在 `create_database.sql` 中添加表结构
2. 在 `sample_data.sql` 中添加示例数据
3. 更新本文档

### 修改表结构
1. 创建迁移脚本
2. 测试迁移过程
3. 更新文档

## 注意事项

1. **安全性**：
   - 用户密码使用bcrypt加密
   - 敏感信息不要明文存储
   - 定期更新数据库用户密码

2. **性能**：
   - 大表查询使用适当的索引
   - 避免SELECT *查询
   - 合理使用分页

3. **数据完整性**：
   - 使用外键约束保证数据一致性
   - 重要操作使用事务
   - 定期备份数据

## 联系信息

如有问题，请联系系统管理员或查看项目文档。

---
*最后更新时间：2024年*