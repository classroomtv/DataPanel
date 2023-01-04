SELECT id as text_id, title, institution_id, course_id ,author_id, membership,  FROM_UNIXTIME(create_time,  '%Y-%m-%d') as create_time, FROM_UNIXTIME(update_time,  '%Y-%m-%d') as update_time
 FROM prod_classroomtv.ctv_texts;
 