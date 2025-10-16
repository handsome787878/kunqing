-- 鲲擎校园管理系统数据库重置脚本
-- 创建时间: 2024年
-- 描述: 用于完全重置数据库，删除所有表和数据

-- 使用数据库
USE kunqing_campus;

-- 禁用外键检查
SET FOREIGN_KEY_CHECKS = 0;

-- 删除所有表（按依赖关系逆序删除）
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS course_reviews;
DROP TABLE IF EXISTS study_group_members;
DROP TABLE IF EXISTS study_groups;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS lost_found;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS system_config;

-- 启用外键检查
SET FOREIGN_KEY_CHECKS = 1;

-- 显示删除结果
SELECT 'Database reset completed successfully!' AS status;
SHOW TABLES;