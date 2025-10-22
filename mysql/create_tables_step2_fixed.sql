-- 第四步：创建失物招领表
CREATE TABLE lost_found (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '物品ID',
    user_id INT NOT NULL COMMENT '发布者用户ID',
    title VARCHAR(200) NOT NULL COMMENT '物品标题',
    description TEXT COMMENT '物品描述',
    category VARCHAR(50) COMMENT '物品类别',
    location VARCHAR(200) COMMENT '丢失/拾取地点',
    contact_info VARCHAR(200) COMMENT '联系方式',
    image_path VARCHAR(255) COMMENT '图片路径',
    type ENUM('lost', 'found') NOT NULL COMMENT '类型：lost-寻物，found-招领',
    status ENUM('open', 'closed', 'resolved') DEFAULT 'open' COMMENT '状态',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='失物招领表';

-- 为失物招领表添加索引
ALTER TABLE lost_found ADD INDEX idx_user_id (user_id);
ALTER TABLE lost_found ADD INDEX idx_category (category);
ALTER TABLE lost_found ADD INDEX idx_type (type);
ALTER TABLE lost_found ADD INDEX idx_status (status);
ALTER TABLE lost_found ADD INDEX idx_create_time (create_time);

-- 第五步：创建课程表
CREATE TABLE courses (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '课程ID',
    course_code VARCHAR(20) NOT NULL UNIQUE COMMENT '课程代码',
    course_name VARCHAR(200) NOT NULL COMMENT '课程名称',
    teacher_name VARCHAR(100) COMMENT '教师姓名',
    credits DECIMAL(3,1) COMMENT '学分',
    semester VARCHAR(20) COMMENT '学期',
    department VARCHAR(100) COMMENT '开课院系',
    description TEXT COMMENT '课程描述',
    schedule VARCHAR(500) COMMENT '上课时间安排',
    location VARCHAR(200) COMMENT '上课地点',
    capacity INT COMMENT '容量',
    enrolled INT DEFAULT 0 COMMENT '已选人数',
    status ENUM('active', 'inactive') DEFAULT 'active' COMMENT '状态',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课程表';

-- 为课程表添加索引
ALTER TABLE courses ADD INDEX idx_course_code (course_code);
ALTER TABLE courses ADD INDEX idx_course_name (course_name);
ALTER TABLE courses ADD INDEX idx_teacher_name (teacher_name);
ALTER TABLE courses ADD INDEX idx_semester (semester);
ALTER TABLE courses ADD INDEX idx_department (department);
ALTER TABLE courses ADD INDEX idx_status (status);