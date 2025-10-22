-- 第十步：创建消息表
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '消息ID',
    sender_id INT NOT NULL COMMENT '发送者用户ID',
    receiver_id INT NOT NULL COMMENT '接收者用户ID',
    title VARCHAR(200) COMMENT '消息标题',
    content TEXT NOT NULL COMMENT '消息内容',
    type ENUM('system', 'user', 'notification') DEFAULT 'user' COMMENT '消息类型',
    is_read BOOLEAN DEFAULT FALSE COMMENT '是否已读',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    read_time TIMESTAMP NULL COMMENT '阅读时间',
    FOREIGN KEY (sender_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (receiver_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_sender_id (sender_id),
    INDEX idx_receiver_id (receiver_id),
    INDEX idx_type (type),
    INDEX idx_is_read (is_read),
    INDEX idx_create_time (create_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='消息表';

-- 第十一步：创建系统配置表
CREATE TABLE system_config (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '配置ID',
    config_key VARCHAR(100) NOT NULL UNIQUE COMMENT '配置键',
    config_value TEXT COMMENT '配置值',
    description VARCHAR(500) COMMENT '配置描述',
    type ENUM('string', 'int', 'boolean', 'json') DEFAULT 'string' COMMENT '值类型',
    is_public BOOLEAN DEFAULT FALSE COMMENT '是否公开',
    create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_config_key (config_key),
    INDEX idx_type (type),
    INDEX idx_is_public (is_public)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='系统配置表';