-- 鲲擎校园管理系统 - 数据库关系查询脚本
-- 用于查看表结构和关系的SQL语句

USE kunqing_campus;

-- 查看所有表信息
SELECT 
    TABLE_NAME as '表名',
    TABLE_COMMENT as '表注释',
    TABLE_ROWS as '记录数',
    DATA_LENGTH as '数据大小(字节)',
    CREATE_TIME as '创建时间'
FROM information_schema.TABLES 
WHERE TABLE_SCHEMA = 'kunqing_campus'
ORDER BY TABLE_NAME;

-- 查看表字段详细信息
SELECT 
    TABLE_NAME as '表名',
    COLUMN_NAME as '字段名',
    DATA_TYPE as '数据类型',
    IS_NULLABLE as '允许空值',
    COLUMN_DEFAULT as '默认值',
    COLUMN_COMMENT as '字段注释'
FROM information_schema.COLUMNS 
WHERE TABLE_SCHEMA = 'kunqing_campus'
ORDER BY TABLE_NAME, ORDINAL_POSITION;

-- 查看外键关系
SELECT 
    CONSTRAINT_NAME as '约束名',
    TABLE_NAME as '子表',
    COLUMN_NAME as '子表字段',
    REFERENCED_TABLE_NAME as '父表',
    REFERENCED_COLUMN_NAME as '父表字段'
FROM information_schema.KEY_COLUMN_USAGE 
WHERE TABLE_SCHEMA = 'kunqing_campus' 
AND REFERENCED_TABLE_NAME IS NOT NULL;

-- 查看索引信息
SELECT 
    TABLE_NAME as '表名',
    INDEX_NAME as '索引名',
    COLUMN_NAME as '字段名',
    NON_UNIQUE as '非唯一',
    INDEX_TYPE as '索引类型'
FROM information_schema.STATISTICS 
WHERE TABLE_SCHEMA = 'kunqing_campus'
ORDER BY TABLE_NAME, INDEX_NAME, SEQ_IN_INDEX;

-- 数据统计查询
SELECT '用户总数' as '统计项', COUNT(*) as '数量' FROM users
UNION ALL
SELECT '活跃用户数', COUNT(*) FROM users WHERE last_login > DATE_SUB(NOW(), INTERVAL 30 DAY)
UNION ALL
SELECT '失物招领总数', COUNT(*) FROM lost_found
UNION ALL
SELECT '开放的失物招领', COUNT(*) FROM lost_found WHERE status = 'open'
UNION ALL
SELECT '二手书总数', COUNT(*) FROM books
UNION ALL
SELECT '可售二手书', COUNT(*) FROM books WHERE status = 'available'
UNION ALL
SELECT '课程总数', COUNT(*) FROM courses
UNION ALL
SELECT '学习小组总数', COUNT(*) FROM study_groups
UNION ALL
SELECT '开放的学习小组', COUNT(*) FROM study_groups WHERE status = 'open'
UNION ALL
SELECT '课程评价总数', COUNT(*) FROM course_reviews
UNION ALL
SELECT '消息总数', COUNT(*) FROM messages;

-- 用户活跃度分析
SELECT 
    college as '学院',
    COUNT(*) as '用户数',
    COUNT(CASE WHEN last_login > DATE_SUB(NOW(), INTERVAL 7 DAY) THEN 1 END) as '7天内活跃',
    COUNT(CASE WHEN last_login > DATE_SUB(NOW(), INTERVAL 30 DAY) THEN 1 END) as '30天内活跃'
FROM users 
WHERE college IS NOT NULL AND college != ''
GROUP BY college
ORDER BY COUNT(*) DESC;

-- 热门课程排行
SELECT 
    c.course_name as '课程名称',
    c.teacher as '授课教师',
    COUNT(cr.id) as '评价数量',
    ROUND(AVG(cr.rating), 2) as '平均评分'
FROM courses c
LEFT JOIN course_reviews cr ON c.id = cr.course_id
GROUP BY c.id, c.course_name, c.teacher
HAVING COUNT(cr.id) > 0
ORDER BY AVG(cr.rating) DESC, COUNT(cr.id) DESC;

-- 学习小组参与度
SELECT 
    sg.title as '小组名称',
    sg.subject as '学科',
    sg.current_members as '当前成员',
    sg.target_members as '目标成员',
    ROUND(sg.current_members / sg.target_members * 100, 1) as '完成度(%)',
    u.real_name as '创建者'
FROM study_groups sg
JOIN users u ON sg.user_id = u.id
ORDER BY sg.current_members DESC;

-- 失物招领状态分布
SELECT 
    type as '类型',
    status as '状态',
    COUNT(*) as '数量'
FROM lost_found
GROUP BY type, status
ORDER BY type, status;

-- 二手书价格分析
SELECT 
    CASE 
        WHEN price < 20 THEN '0-20元'
        WHEN price < 40 THEN '20-40元'
        WHEN price < 60 THEN '40-60元'
        ELSE '60元以上'
    END as '价格区间',
    COUNT(*) as '书籍数量',
    ROUND(AVG(price), 2) as '平均价格'
FROM books
GROUP BY 
    CASE 
        WHEN price < 20 THEN '0-20元'
        WHEN price < 40 THEN '20-40元'
        WHEN price < 60 THEN '40-60元'
        ELSE '60元以上'
    END
ORDER BY AVG(price);

-- 系统使用情况月度统计
SELECT 
    DATE_FORMAT(create_time, '%Y-%m') as '月份',
    COUNT(CASE WHEN TABLE_NAME = 'users' THEN 1 END) as '新用户',
    COUNT(CASE WHEN TABLE_NAME = 'lost_found' THEN 1 END) as '失物招领',
    COUNT(CASE WHEN TABLE_NAME = 'books' THEN 1 END) as '二手书',
    COUNT(CASE WHEN TABLE_NAME = 'study_groups' THEN 1 END) as '学习小组'
FROM (
    SELECT create_time, 'users' as TABLE_NAME FROM users
    UNION ALL
    SELECT create_time, 'lost_found' FROM lost_found
    UNION ALL
    SELECT create_time, 'books' FROM books
    UNION ALL
    SELECT create_time, 'study_groups' FROM study_groups
) combined
WHERE create_time >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
GROUP BY DATE_FORMAT(create_time, '%Y-%m')
ORDER BY 月份 DESC;