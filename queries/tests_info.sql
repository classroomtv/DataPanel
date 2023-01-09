SELECT id as test_id, institution_id,title, author_id, class_id, membership ,course_id, FROM_UNIXTIME(create_time,  '%Y-%m-%d') as create_time, FROM_UNIXTIME(update_time,  '%Y-%m-%d') as update_time 
FROM prod_classroomtv.ctv_tests
where  ctv_tests.settings not like '%"isPoll":"1"%'
AND author_id IS NOT NULL;


