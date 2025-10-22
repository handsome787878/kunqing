-- 第八步：创建学习小组成员表
CREATE TABLE study_group_members (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '成员ID',
    group_id INT NOT NULL COMMENT '小组ID',
    user_id INT NOT NULL COMMENT '用户ID',
    role ENUM('leader', 'member') DEFAULT 'member' COMMENT '角色：leader-组长，member-成员',
    join_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
    status ENUM('active', 'inactive') DEFAULT 'active' COMMENT '状态',
    FOREIGN KEY (group_id) REFERENCES study_groups(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    UNIQUE KEY uk_group_user (group_id, user_id),
    INDEX idx_group_id (group_id),
    INDEX idx_user_id (user_id),
    INDEX idx_role (role),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='学习小组成员表';

-- 第九步：创建课程评价表
CREATE TABLE course_reviews (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '评价ID',
    user_id INT NOT NULL COMMENT '评价者用户ID',
    course_id INT NOT NULL COMMENT '课程ID',
    rating INT NOT NULL COMMENT '评分（1-5分）',
    difficulty INT COMMENT '难度（1-5分）',
    workload INT COMMENT '作业量（1-5分）',
    attendance_required BOOLEAN COMMENT '是否需要考勤',
    review_text TEXT COMMENT '评价内容',
    semester VARCHAR(20) COMMENT '上课学期',
    is_anonymous BOOLEAN DEFAULT FALSE COMMENT '是否匿名',
    helpful_count INT DEFAULT 0 COMMENT '有用数',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_course_id (course_id),
    INDEX idx_rating (rating),
    INDEX idx_semester (semester),
    INDEX idx_create_time (create_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='课程评价表';