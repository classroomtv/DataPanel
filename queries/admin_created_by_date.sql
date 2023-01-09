SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS create_time, institution_id , count(user_id) as created_admins
FROM prod_classroomtv.ctv_user_belongs_institution 
WHERE is_admin = 1
GROUP BY institution_id
ORDER BY create_time;
