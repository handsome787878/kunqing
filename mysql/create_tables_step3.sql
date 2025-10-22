-- 第六步：创建二手书籍表
CREATE TABLE books (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '书籍ID',
    user_id INT NOT NULL COMMENT '发布者用户ID',
    title VARCHAR(200) NOT NULL COMMENT '书籍标题',
    author VARCHAR(100) COMMENT '作者',
    isbn VARCHAR(20) COMMENT 'ISBN',
    publisher VARCHAR(100) COMMENT '出版社',
    publish_year INT COMMENT '出版年份',
    original_price DECIMAL(10,2) COMMENT '原价',
    selling_price DECIMAL(10,2) NOT NULL COMMENT '售价',
    condition_desc VARCHAR(50) COMMENT '新旧程度',
    description TEXT COMMENT '书籍描述',
    image_path VARCHAR(255) COMMENT '图片路径',
    category VARCHAR(50) COMMENT '书籍类别',
    contact_info VARCHAR(200) COMMENT '联系方式',
    status ENUM('available', 'sold', 'reserved') DEFAULT 'available' COMMENT '状态',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_title (title),
    INDEX idx_author (author),
    INDEX idx_isbn (isbn),
    INDEX idx_category (category),
    INDEX idx_status (status),
    INDEX idx_selling_price (selling_price),
    INDEX idx_create_time (create_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='二手书籍表';

-- 第七步：创建学习小组表
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