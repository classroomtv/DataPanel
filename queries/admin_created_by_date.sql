SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS create_time, institution_id, COUNT( DISTINCT( user_id))
FROM prod_classroomtv.ctv_user_belongs_institution 
WHERE is_admin=1
group by create_time


