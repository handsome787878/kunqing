-- 鲲擎校园管理系统数据库创建脚本
-- 创建时间: 2024年
-- 描述: 包含用户管理、失物招领、二手书交易、课程管理、学习小组等功能模块

-- 创建数据库
CREATE DATABASE IF NOT EXISTS kunqing_campus 
DEFAULT CHARACTER SET utf8mb4 
DEFAULT COLLATE utf8mb4_unicode_ci;

USE kunqing_campus;

-- 删除已存在的表（如果存在）
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS course_reviews;
DROP TABLE IF EXISTS study_group_members;
DROP TABLE IF EXISTS study_groups;
DROP TABLE IF EXISTS books;
DROP TABLE IF EXISTS lost_found;
DROP TABLE IF EXISTS courses;
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS system_config;

-- 用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '用户ID',
    student_id VARCHAR(20) NOT NULL UNIQUE COMMENT '学号',
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
    password VARCHAR(255) NOT NULL COMMENT '密码(加密)',
    real_name VARCHAR(50) COMMENT '真实姓名',
    college VARCHAR(100) COMMENT '学院',
    major VARCHAR(100) COMMENT '专业',
    grade VARCHAR(20) COMMENT '年级',
    phone VARCHAR(20) COMMENT '手机号',
    avatar VARCHAR(255) COMMENT '头像路径',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    last_login TIMESTAMP NULL COMMENT '最后登录时间',
    is_active TINYINT(1) DEFAULT 1 COMMENT '是否激活',
    INDEX idx_student_id (student_id),
    INDEX idx_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- 失物招领表
CREATE TABLE lost_found (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    user_id INT NOT NULL COMMENT '发布用户ID',
    type ENUM('lost', 'found') NOT NULL COMMENT '类型：lost-寻物启事，found-失物招领',
    title VARCHAR(200) NOT NULL COMMENT '标题',
    description TEXT COMMENT '详细描述',
    location VARCHAR(200) COMMENT '丢失/拾取地点',
    contact VARCHAR(100) COMMENT '联系方式',
    status ENUM('open', 'closed', 'resolved') DEFAULT 'open' COMMENT '状态：open-开放，closed-关闭，resolved-已解决',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_type (type),
    INDEX idx_status (status),
    INDEX idx_create_time (create_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='失物招领表';

-- 二手书表
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '书籍ID',
    user_id INT NOT NULL COMMENT '发布用户ID',
    book_name VARCHAR(200) NOT NULL COMMENT '书名',
    author VARCHAR(100) COMMENT '作者',
    price DECIMAL(10,2) DEFAULT 0.00 COMMENT '价格',
    condition_desc VARCHAR(100) COMMENT '书籍状态描述',
    description TEXT COMMENT '详细描述',
    status ENUM('available', 'sold', 'reserved') DEFAULT 'available' COMMENT '状态：available-可售，sold-已售，reserved-预定',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_book_name (book_name),
    INDEX idx_status (status),
    INDEX idx_price (price),
    INDEX idx_create_time (create_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='二手书表';

-- 课程表
CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '课程ID',
    course_code VARCHAR(20) NOT NULL UNIQUE COMMENT '课程代码',
    course_name VARCHAR(200) NOT NULL COMMENT '课程名称',
    teacher VARCHAR(100) COMMENT '授课教师',
    college VARCHAR(100) COMMENT '开课学院',
    description TEXT COMMENT '课程描述',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_course_code (course_code),
    INDEX idx_course_name (course_name),
    INDEX idx_teacher (teacher),
    INDEX idx_college (college)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课程表';

-- 学习小组表
CREATE TABLE study_groups (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '小组ID',
    user_id INT NOT NULL COMMENT '创建者用户ID',
    title VARCHAR(200) NOT NULL COMMENT '小组标题',
    subject VARCHAR(100) COMMENT '学科',
    goal TEXT COMMENT '学习目标',
    target_members INT DEFAULT 5 COMMENT '目标成员数',
    current_members INT DEFAULT 1 COMMENT '当前成员数',
    status ENUM('open', 'closed', 'full') DEFAULT 'open' COMMENT '状态：open-开放，closed-关闭，full-已满',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_subject (subject),
    INDEX idx_status (status),
    INDEX idx_create_time (create_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习小组表';

-- 学习小组成员表
CREATE TABLE study_group_members (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '记录ID',
    group_id INT NOT NULL COMMENT '小组ID',
    user_id INT NOT NULL COMMENT '用户ID',
    role ENUM('creator', 'member') DEFAULT 'member' COMMENT '角色：creator-创建者，member-成员',
    join_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
    FOREIGN KEY (group_id) REFERENCES study_groups(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uk_group_user (group_id, user_id),
    INDEX idx_group_id (group_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习小组成员表';

-- 课程评价表
CREATE TABLE course_reviews (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '评价ID',
    course_id INT NOT NULL COMMENT '课程ID',
    user_id INT NOT NULL COMMENT '评价用户ID',
    rating INT NOT NULL CHECK (rating >= 1 AND rating <= 5) COMMENT '评分(1-5)',
    review_text TEXT COMMENT '评价内容',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uk_course_user (course_id, user_id),
    INDEX idx_course_id (course_id),
    INDEX idx_user_id (user_id),
    INDEX idx_rating (rating)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课程评价表';

-- 消息表
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '消息ID',
    sender_id INT NOT NULL COMMENT '发送者ID',
    receiver_id INT NOT NULL COMMENT '接收者ID',
    title VARCHAR(200) COMMENT '消息标题',
    content TEXT NOT NULL COMMENT '消息内容',
    type ENUM('system', 'user', 'group') DEFAULT 'user' COMMENT '消息类型',
    is_read TINYINT(1) DEFAULT 0 COMMENT '是否已读',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_sender_id (sender_id),
    INDEX idx_receiver_id (receiver_id),
    INDEX idx_is_read (is_read),
    INDEX idx_create_time (create_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='消息表';

-- 系统配置表
CREATE TABLE system_config (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '配置ID',
    config_key VARCHAR(100) NOT NULL UNIQUE COMMENT '配置键',
    config_value TEXT COMMENT '配置值',
    description VARCHAR(255) COMMENT '配置描述',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_config_key (config_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';