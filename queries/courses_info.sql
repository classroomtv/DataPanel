SELECT courses.id, title, name, institution_id, FROM_UNIXTIME(create_time,  '%Y-%m-%d') as create_time, FROM_UNIXTIME(update_time,  '%Y-%m-%d') as update_time, view_count, author_id, user_finished_courses,  signed_users,  user_failed_courses
FROM prod_classroomtv.ctv_institutions inst
LEFT JOIN prod_classroomtv.ctv_courses courses
ON courses.institution_id = inst.id
LEFT JOIN (SELECT course_id, count(distinct (CASE WHEN status = 'Cursado' OR status = 'Aprobado' THEN user_id END)) AS user_finished_courses,
count(distinct(user_id)) AS signed_users,
count(distinct (CASE WHEN status = 'Incompleto' OR status = 'Reprobado' THEN user_id END)) AS user_failed_courses
FROM prod_classroomtv.ctv_user_course_finish
GROUP BY course_id) signed_info
ON courses.id = signed_info.course_id
AND view_count IS NOT NULL;

