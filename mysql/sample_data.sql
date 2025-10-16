-- 鲲擎校园管理系统示例数据插入脚本
-- 创建时间: 2024年
-- 描述: 包含各个功能模块的示例数据，用于系统测试和演示

USE kunqing_campus;

-- 清空现有数据（可选，用于重新初始化）
-- SET FOREIGN_KEY_CHECKS = 0;
-- TRUNCATE TABLE messages;
-- TRUNCATE TABLE course_reviews;
-- TRUNCATE TABLE study_group_members;
-- TRUNCATE TABLE study_groups;
-- TRUNCATE TABLE courses;
-- TRUNCATE TABLE books;
-- TRUNCATE TABLE lost_found;
-- TRUNCATE TABLE users;
-- SET FOREIGN_KEY_CHECKS = 1;

-- 插入示例用户数据
INSERT INTO users (student_id, email, password, real_name, college, major, grade, phone) VALUES
('2021001', 'zhangsan@kunqing.edu.cn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VjWZifHey', '张三', '计算机学院', '计算机科学与技术', '2021级', '13800138001'),
('2021002', 'lisi@kunqing.edu.cn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VjWZifHey', '李四', '数学学院', '数学与应用数学', '2021级', '13800138002'),
('2021003', 'wangwu@kunqing.edu.cn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VjWZifHey', '王五', '外国语学院', '英语', '2021级', '13800138003'),
('2022001', 'zhaoliu@kunqing.edu.cn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VjWZifHey', '赵六', '物理学院', '应用物理学', '2022级', '13800138004'),
('2022002', 'sunqi@kunqing.edu.cn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VjWZifHey', '孙七', '化学学院', '化学', '2022级', '13800138005'),
('2023001', 'admin@kunqing.edu.cn', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj/VjWZifHey', '管理员', '信息中心', '系统管理', '管理员', '13800138000');

-- 插入课程数据
INSERT INTO courses (course_code, course_name, teacher, college, description) VALUES
('CS101', '计算机科学导论', '王教授', '计算机学院', '介绍计算机科学的基本概念和发展历程'),
('MATH101', '高等数学A', '李教授', '数学学院', '微积分、线性代数等数学基础知识'),
('ENG101', '大学英语', '张教授', '外国语学院', '提高英语听说读写能力'),
('PHY101', '大学物理', '刘教授', '物理学院', '力学、热学、电磁学等物理基础'),
('CHEM101', '无机化学', '陈教授', '化学学院', '化学基本原理和无机化合物'),
('CS201', '数据结构与算法', '王教授', '计算机学院', '数据结构设计和算法分析'),
('MATH201', '线性代数', '李教授', '数学学院', '矩阵理论和线性变换'),
('CS301', '数据库系统', '赵教授', '计算机学院', '数据库设计和SQL语言');

-- 插入失物招领数据
INSERT INTO lost_found (user_id, type, title, description, location, contact, status) VALUES
(1, 'lost', '丢失校园卡', '在图书馆三楼丢失校园卡，卡号2021001，卡上贴有小熊贴纸', '图书馆三楼', '13800138001', 'open'),
(2, 'found', '捡到钥匙', '在第二食堂门口捡到一串钥匙，有三把钥匙和一个小挂件', '第二食堂', '13800138002', 'open'),
(3, 'lost', '丢失水杯', '蓝色保温杯，杯身有英文字母贴纸，在体育馆丢失', '体育馆', '13800138003', 'open'),
(4, 'found', '捡到手机', 'iPhone 12，黑色，屏幕有轻微划痕，在教学楼A座捡到', '教学楼A座', '13800138004', 'resolved'),
(1, 'found', '捡到眼镜', '黑框眼镜，度数较高，在图书馆阅览室捡到', '图书馆', '13800138001', 'open'),
(5, 'lost', '丢失笔记本', '红色笔记本，里面有化学实验记录，非常重要', '化学实验楼', '13800138005', 'open');

-- 插入二手书数据
INSERT INTO books (user_id, book_name, author, price, condition_desc, description, status) VALUES
(1, '高等数学（上册）', '同济大学数学系', 35.00, '八成新', '课本无笔记，保存完好，适合数学专业学生', 'available'),
(2, '大学英语综合教程1', '李荫华', 25.00, '九成新', '几乎全新，只用了一个学期', 'available'),
(3, '计算机网络', '谢希仁', 45.00, '七成新', '有少量笔记和标记，内容完整', 'available'),
(4, '普通物理学', '程守洙', 40.00, '八成新', '物理专业必备教材，无破损', 'sold'),
(5, '无机化学', '大连理工大学', 30.00, '九成新', '化学专业教材，保存良好', 'available'),
(1, '数据结构与算法分析', 'Mark Allen Weiss', 55.00, '八成新', 'C++版本，计算机专业经典教材', 'available'),
(2, '线性代数', '居余马', 28.00, '七成新', '有部分习题答案标记', 'reserved'),
(3, '大学物理实验', '复旦大学', 20.00, '八成新', '实验指导书，内容完整', 'available');

-- 插入学习小组数据
INSERT INTO study_groups (user_id, title, subject, goal, target_members, current_members, status) VALUES
(1, '高数学习互助小组', '高等数学', '期末考试复习，提高数学成绩，互相讨论难题', 6, 3, 'open'),
(2, '英语口语练习小组', '英语', '提高英语口语水平，练习日常对话和学术表达', 4, 2, 'open'),
(3, '计算机编程学习小组', '计算机科学', '学习Python和Java编程，完成课程项目', 8, 5, 'open'),
(4, '物理实验讨论组', '物理', '讨论物理实验方法，分享实验心得', 5, 4, 'open'),
(5, '化学竞赛备考小组', '化学', '准备全国大学生化学竞赛，系统复习化学知识', 6, 2, 'open'),
(1, '数据结构算法小组', '计算机科学', '深入学习数据结构和算法，提高编程能力', 6, 1, 'open');

-- 插入学习小组成员数据
INSERT INTO study_group_members (group_id, user_id, role) VALUES
(1, 1, 'creator'),
(1, 2, 'member'),
(1, 4, 'member'),
(2, 2, 'creator'),
(2, 3, 'member'),
(3, 3, 'creator'),
(3, 1, 'member'),
(3, 2, 'member'),
(3, 4, 'member'),
(3, 5, 'member'),
(4, 4, 'creator'),
(4, 1, 'member'),
(4, 3, 'member'),
(4, 5, 'member'),
(5, 5, 'creator'),
(5, 2, 'member'),
(6, 1, 'creator');

-- 插入课程评价数据
INSERT INTO course_reviews (course_id, user_id, rating, review_text) VALUES
(1, 1, 5, '王教授讲课很生动，内容丰富，对计算机科学入门很有帮助'),
(1, 2, 4, '课程内容不错，但是作业有点多'),
(2, 1, 4, '李教授的数学课很严谨，学到了很多'),
(2, 4, 5, '高等数学讲得很清楚，例题丰富'),
(3, 2, 5, '张教授的英语课很实用，口语练习很多'),
(3, 3, 4, '英语课氛围很好，同学们都很积极'),
(4, 4, 4, '物理实验很有趣，理论联系实际'),
(5, 5, 5, '化学课内容丰富，实验很精彩'),
(6, 1, 5, '数据结构课程很有挑战性，收获很大'),
(6, 3, 4, '算法部分讲得很详细，但需要多练习');

-- 插入系统消息数据
INSERT INTO messages (sender_id, receiver_id, title, content, type) VALUES
(6, 1, '欢迎使用鲲擎校园系统', '欢迎您使用鲲擎校园管理系统！请完善您的个人信息。', 'system'),
(6, 2, '欢迎使用鲲擎校园系统', '欢迎您使用鲲擎校园管理系统！请完善您的个人信息。', 'system'),
(6, 3, '欢迎使用鲲擎校园系统', '欢迎您使用鲲擎校园管理系统！请完善您的个人信息。', 'system'),
(1, 2, '关于高数学习小组', '你好，欢迎加入我们的高数学习小组！', 'user'),
(2, 1, '回复：关于高数学习小组', '谢谢邀请，很高兴能加入小组一起学习！', 'user'),
(3, 1, '询问编程小组', '请问编程小组还招收新成员吗？', 'user');

-- 插入系统配置数据
INSERT INTO system_config (config_key, config_value, description) VALUES
('site_name', '鲲擎校园', '网站名称'),
('site_description', '鲲擎校园管理系统 - 您的校园生活助手', '网站描述'),
('max_upload_size', '10485760', '最大上传文件大小（字节）'),
('email_smtp_host', 'smtp.kunqing.edu.cn', '邮件SMTP服务器'),
('email_smtp_port', '587', '邮件SMTP端口'),
('default_avatar', '/static/images/default_avatar.png', '默认头像路径'),
('system_maintenance', '0', '系统维护模式（0-正常，1-维护）'),
('user_registration', '1', '用户注册开关（0-关闭，1-开放）');

-- 更新用户最后登录时间（模拟用户活跃度）
UPDATE users SET last_login = DATE_SUB(NOW(), INTERVAL FLOOR(RAND() * 30) DAY) WHERE id <= 5;

-- 显示插入结果统计
SELECT 
    '用户' as 表名, COUNT(*) as 记录数 FROM users
UNION ALL
SELECT '课程', COUNT(*) FROM courses
UNION ALL
SELECT '失物招领', COUNT(*) FROM lost_found
UNION ALL
SELECT '二手书', COUNT(*) FROM books
UNION ALL
SELECT '学习小组', COUNT(*) FROM study_groups
UNION ALL
SELECT '小组成员', COUNT(*) FROM study_group_members
UNION ALL
SELECT '课程评价', COUNT(*) FROM course_reviews
UNION ALL
SELECT '消息', COUNT(*) FROM messages
UNION ALL
SELECT '系统配置', COUNT(*) FROM system_config;