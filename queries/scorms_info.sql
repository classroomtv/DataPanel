SELECT id as scorm_id, institution_id ,title, author_id, course_id, membership, view_count, FROM_UNIXTIME(create_time,  '%Y-%m-%d') as create_time
FROM prod_classroomtv.ctv_scorm;