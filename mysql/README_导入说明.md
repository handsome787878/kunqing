# 鲲擎校园管理系统数据库导入说明

## 问题分析

根据您遇到的错误，问题可能出现在以下几个方面：

1. **文件编码问题**：SQL文件可能不是UTF-8编码
2. **MySQL版本兼容性**：某些语法在不同MySQL版本中可能不兼容
3. **外键约束问题**：表创建顺序可能导致外键引用失败
4. **单个文件过大**：一次性导入所有表可能导致超时或内存问题

## 解决方案：分步骤导入

我已经将原始的数据库创建脚本拆分为多个小文件，建议按以下顺序逐步导入：

### 步骤1：创建数据库和用户表
文件：`create_database_simple.sql`
- 创建数据库
- 删除已存在的表
- 创建用户表（基础表，无外键依赖）

### 步骤2：创建基础业务表
文件：`create_tables_step2.sql`
- 创建失物招领表
- 创建课程表

### 步骤3：创建扩展业务表
文件：`create_tables_step3.sql`
- 创建二手书籍表
- 创建学习小组表

### 步骤4：创建关联表
文件：`create_tables_step4.sql`
- 创建学习小组成员表
- 创建课程评价表

### 步骤5：创建系统表
文件：`create_tables_step5.sql`
- 创建消息表
- 创建系统配置表

## 导入操作步骤

### 在Navicat中操作：

1. **连接到MySQL服务器**
   - 确保MySQL服务正在运行
   - 使用管理员权限连接

2. **设置字符编码**
   - 在Navicat中，右键点击连接 → 编辑连接
   - 在"高级"选项卡中，设置字符集为 `utf8mb4`

3. **逐步执行SQL文件**
   - 按顺序打开每个SQL文件
   - 确保文件编码为UTF-8
   - 逐个执行，观察是否有错误

4. **验证创建结果**
   - 刷新数据库列表
   - 检查所有表是否创建成功
   - 查看表结构是否正确

### 命令行操作（备选方案）：

```bash
# 1. 登录MySQL
mysql -u root -p

# 2. 按顺序执行文件
source e:/APP/kunqing/kunqing-campus/mysql/create_database_simple.sql
source e:/APP/kunqing/kunqing-campus/mysql/create_tables_step2.sql
source e:/APP/kunqing/kunqing-campus/mysql/create_tables_step3.sql
source e:/APP/kunqing/kunqing-campus/mysql/create_tables_step4.sql
source e:/APP/kunqing/kunqing-campus/mysql/create_tables_step5.sql
```

## 插入示例数据

表结构创建完成后，可以执行：
- `sample_data.sql` - 插入示例数据

## 其他可用文件

- `database_diagram.sql` - 查看数据库结构信息
- `reset_database.sql` - 重置数据库（删除所有数据）

## 故障排除

如果仍然遇到问题：

1. **检查MySQL版本**：确保使用MySQL 5.7+或8.0+
2. **检查权限**：确保用户有CREATE、DROP、ALTER权限
3. **检查字符集**：确保数据库和表都使用utf8mb4
4. **逐表创建**：如果批量创建失败，可以逐个表创建

## 联系支持

如果按照以上步骤仍然无法解决问题，请提供：
- MySQL版本信息
- 具体的错误消息
- 执行到哪一步出现问题