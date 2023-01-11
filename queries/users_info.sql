SELECT FROM_UNIXTIME(ubi.create_time,  '%Y-%m-%d') AS 'create_time' , ubi.institution_id, ubi.user_id, ubi.is_admin, ubi.active, ubi.status
FROM prod_classroomtv.ctv_user_belongs_institution ubi
ORDER by create_time;