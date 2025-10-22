-- 鲲擎校园管理系统数据库创建脚本（简化版）
-- 建议分步骤执行

-- 第一步：创建数据库
CREATE DATABASE IF NOT EXISTS kunqing_campus 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE kunqing_campus;

-- 第二步：删除已存在的表（如果有）
SET FOREIGN_KEY_CHECKS = 0;
DROP TABLE IF EXISTS system_config;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS course_reviews;
DROP TABLE IF EXISTS study_group_members;
DROP TABLE IF EXISTS study_groups;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS lost_found;
DROP TABLE IF EXISTS users;
SET FOREIGN_KEY_CHECKS = 1;

-- 第三步：创建用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    real_name VARCHAR(50) COMMENT '真实姓名',
    student_id VARCHAR(20) COMMENT '学号',
    phone VARCHAR(20) COMMENT '手机号',
    avatar VARCHAR(255) COMMENT '头像路径',
    role ENUM('student', 'teacher', 'admin') DEFAULT 'student' COMMENT '角色',
    status ENUM('active', 'inactive', 'banned') DEFAULT 'active' COMMENT '状态',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    last_login TIMESTAMP NULL COMMENT '最后登录时间',
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_student_id (student_id),
    INDEX idx_role (role),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';