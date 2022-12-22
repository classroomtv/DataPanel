SELECT courses.id, title, name ,institution_id, FROM_UNIXTIME(create_time,  '%Y-%m-%d') as create_time, FROM_UNIXTIME(update_time,  '%Y-%m-%d') as update_time, view_count, author_id 
FROM prod_classroomtv.ctv_institutions inst
LEFT JOIN prod_classroomtv.ctv_courses courses
ON courses.institution_id = inst.id