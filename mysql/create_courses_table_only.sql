-- 单独创建课程表
USE kunqing_campus;

-- 删除课程表（如果存在）
DROP TABLE IF EXISTS courses;

-- 创建课程表
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

-- 添加索引
ALTER TABLE courses ADD INDEX idx_course_code (course_code);
ALTER TABLE courses ADD INDEX idx_course_name (course_name);
ALTER TABLE courses ADD INDEX idx_teacher_name (teacher_name);
ALTER TABLE courses ADD INDEX idx_semester (semester);
ALTER TABLE courses ADD INDEX idx_department (department);
ALTER TABLE courses ADD INDEX idx_status (status);

-- 验证表创建
SHOW CREATE TABLE courses;