SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS create_time, institution_id , count(user_id) as created_users
FROM prod_classroomtv.ctv_user_belongs_institution
GROUP BY create_time;
