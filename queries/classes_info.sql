SELECT id as class_id,institution_id ,title, FROM_UNIXTIME(create_time,  '%Y-%m-%d') as create_time, FROM_UNIXTIME(update_time,  '%Y-%m-%d') as update_time, view_count, course_id, author_id
FROM prod_classroomtv.ctv_classes; 