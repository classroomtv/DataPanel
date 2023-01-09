SELECT 	id, 
		name,
		city,
        collaborator_users,
        admin_users,
		classes_count,
		text_count,
		scorm_count,
		programs_count,
        created_tests_count,
        created_news_count,
        new_views_count,
        courses_count,
        finished_courses,
        answered_questions_count,
        correct_answers_count,
        incorrect_answers_count,
        likes_count,
        created_questions,
        created_questions,
        comments_count,
        attempts_count
FROM prod_classroomtv.ctv_institutions inst
LEFT JOIN ( SELECT  class.institution_id, count(id) as classes_count
			FROM prod_classroomtv.ctv_classes as class
			group by class.institution_id) classes 
ON classes.institution_id = inst.id
LEFT JOIN ( SELECT institution_id, count(id) as text_count
			FROM prod_classroomtv.ctv_texts
			group by institution_id) texts
ON texts.institution_id = inst.id
LEFT JOIN ( SELECT institution_id, count(id) as scorm_count
			FROM prod_classroomtv.ctv_scorm 
			group by institution_id) scorm
			ON scorm.institution_id = inst.id
LEFT JOIN ( SELECT institution_id,count(iu.id) AS programs_count
			FROM prod_classroomtv.ctv_institution_degrees as iu 
			group by institution_id) programs 
			ON programs.institution_id = inst.id
LEFT JOIN ( SELECT institution_id, count(id) as created_tests_count
			FROM prod_classroomtv.ctv_tests
			GROUP BY institution_id) tests
ON tests.institution_id = inst.id
LEFT JOIN ( SELECT institution_id, count(*) AS created_news_count 
			FROM prod_classroomtv.ctv_news
			GROUP BY institution_id) news
			ON news.institution_id = inst.id
LEFT JOIN ( SELECT institution_id, count(*) AS new_views_count
			FROM prod_classroomtv.ctv_user_navigation_logs 
			WHERE PAGE LIKE 'Vista de noticia%'
			GROUP BY institution_id) new_views
ON new_views.institution_id = inst.id
LEFT JOIN ( SELECT institution_id, count(id) AS courses_count
			FROM prod_classroomtv.ctv_courses
			GROUP BY institution_id) courses
ON courses.institution_id = inst.id
LEFT JOIN ( SELECT institution_id, sum(finished_courses) as finished_courses FROM (
			SELECT ubi.institution_id, ctv_user_course_histories.user_id ,count(distinct ctv_user_course_histories.id) as finished_courses
			FROM prod_classroomtv.ctv_user_course_histories
			INNER JOIN prod_classroomtv.ctv_user_belongs_institution AS ubi 
			ON ubi.user_id = ctv_user_course_histories.user_id
            WHERE is_finish = 1
			group by ctv_user_course_histories.user_id) a
		   group by institution_id) finished
ON finished.institution_id = inst.id
LEFT JOIN ( SELECT 	institution_id,
			SUM(CASE WHEN is_admin != 1 THEN 1 ELSE 0 END) AS collaborator_users,
			SUM(CASE WHEN is_admin = 1 THEN 1 ELSE 0 END) AS admin_users
			FROM prod_classroomtv.ctv_users as u 
			INNER JOIN prod_classroomtv.ctv_user_belongs_institution as ubi 
            ON (ubi.user_id = u.id)
			GROUP BY institution_id) users
ON users.institution_id = inst.id
LEFT JOIN ( SELECT institution_id, sum(answered_questions) as answered_questions_count,sum(correct_answers) as correct_answers_count, sum(incorrect_answers) as incorrect_answers_count FROM (
			SELECT ubi.institution_id,  uia.user_id ,
            count(distinct (CASE WHEN is_answered = 1 THEN uia.id END)) AS answered_questions,
			count(distinct (CASE WHEN is_answered = 1 AND is_correct = 1 THEN uia.id END)) AS correct_answers,
			count(distinct (CASE WHEN is_answered = 1 AND is_correct = 0 THEN uia.id END)) AS incorrect_answers
			FROM prod_classroomtv.ctv_user_item_answers uia
			INNER JOIN prod_classroomtv.ctv_user_belongs_institution AS ubi 
			ON  ubi.user_id = uia.user_id
			group by  uia.user_id) a
		   group by institution_id) questions
ON questions.institution_id = inst.id
LEFT JOIN (SELECT institution_id, sum(likes) as likes_count FROM (
			SELECT ubi.institution_id, ctv_user_likes_news.user_id ,count(distinct ctv_user_likes_news.id) as likes
			FROM prod_classroomtv.ctv_user_likes_news
			INNER JOIN prod_classroomtv.ctv_user_belongs_institution AS ubi 
			ON ubi.user_id = ctv_user_likes_news.user_id
            WHERE news_id IS NOT NULL
			group by ctv_user_likes_news.user_id
			order by institution_id) a
		   group by institution_id) likes
ON likes.institution_id = inst.id
LEFT JOIN (SELECT institution_id, sum(items_count) as created_questions FROM (
			SELECT ubi.institution_id, author_id ,count(distinct ctv_items.id) as items_count
			FROM prod_classroomtv.ctv_items
			INNER JOIN prod_classroomtv.ctv_user_belongs_institution AS ubi 
			ON ubi.user_id = ctv_items.author_id
			group by author_id
			order by institution_id) a
		   group by institution_id) items
ON items.institution_id = inst.id
LEFT JOIN (SELECT institution_id, sum(comments) as comments_count FROM (
			SELECT ubi.institution_id, author_id ,count(distinct ctv_questions.id) as comments
			FROM prod_classroomtv.ctv_questions
			INNER JOIN prod_classroomtv.ctv_user_belongs_institution AS ubi 
			ON ubi.user_id = ctv_questions.author_id
            WHERE news_id IS NOT NULL
			group by author_id
			order by institution_id) a
		   group by institution_id) comments
ON comments.institution_id = inst.id
LEFT JOIN ( SELECT institution_id, sum(attempts) as attempts_count FROM (
			SELECT ubi.institution_id, ctv_user_test_attempts.user_id ,count(distinct ctv_user_test_attempts.id) as attempts
			FROM prod_classroomtv.ctv_user_test_attempts
			INNER JOIN prod_classroomtv.ctv_user_belongs_institution AS ubi 
			ON ubi.user_id = ctv_user_test_attempts.user_id
			group by ctv_user_test_attempts.user_id) a
		   group by institution_id) attemps 
ON attemps.institution_id = inst.id
WHERE inst.custom_settings LIKE '%"blockedInstitution":"0"%';




            
            





