--Query con toda la info
SELECT cour.institution_id, users.name ,
users.city,
count(course_id) AS created_courses,
SUM(CASE WHEN is_finish = 1 THEN 1 ELSE 0 END) AS finished_courses,
users.active_users,
users.admin_users,
news.cant_news
FROM ctv_courses cour
INNER JOIN ctv_user_course_histories uch
ON  cour.id = uch.course_id
LEFT JOIN (
		SELECT institution_id,
		i.city,
		i.name, 
		SUM(CASE WHEN is_admin != 1 THEN 1 ELSE 0 END) AS active_users,
		SUM(CASE WHEN is_admin = 1 THEN 1 ELSE 0 END) AS admin_users
		FROM ctv_user_belongs_institution ubi
		INNER JOIN ctv_institutions as i 
		ON (ubi.institution_id = i.id) 
		WHERE ubi.active = 1
		GROUP BY institution_id) 
users on users.institution_id = cour.institution_id
LEFT JOIN ( SELECT institution_id, 
			count(id) as cant_news
			FROM ctv_news
			group by institution_id) 
news ON news.institution_id = cour.institution_id
GROUP by institution_id

--Usuarios activos y usuarios administradores activos
SELECT institution_id,i.name, 
	  SUM(CASE WHEN is_admin != 1 THEN 1 ELSE 0 END) AS collaborators_users,
      SUM(CASE WHEN is_admin = 1 THEN 1 ELSE 0 END) AS admin_users
from ctv_user_belongs_institution ubi
LEFT JOIN ctv_institutions as i 
 on (ubi.institution_id = i.id) 
WHERE ubi.active = 1
GROUP BY institution_id;

--Test realizadas (Como relaciono esto a las instituciones?)-> por medio de tests!!!!FALTAAAAAAAAAAAAAAA
SELECT institution_id,count(*) 
FROM ctv_user_test_attempts
group by institution_id;

--Cantidad de programas creados global
SELECT institution_id,count(iu.id) AS 'Programas'
FROM ctv_institution_degrees as iu 
group by institution_id

--Cantidad de contenidos globales LISTO
--Clases
SELECT institution_id, classes_count from (
SELECT  class.institution_id, count(id) as classes_count
FROM ctv_classes as class
group by class.institution_id) t;
--Textos
SELECT institution_id, text_count FROM(
SELECT institution_id, count(id) as text_count
FROM ctv_texts
group by institution_id) t;
--Scorm
SELECT institution_id, scorm_count FROM(
SELECT institution_id, count(id) as scorm_count
FROM ctv_scorm 
group by institution_id) t;

--Evaluaciones creadas global
SELECT institution_id, count(id) as created_tests
FROM ctv_tests
GROUP BY institution_id

--Evaluaciones realizadas global (Como relaciono esto a las instituciones?)
SELECT * FROM ctv_user_test_attempts;

--Preguntas creadas global (Como relaciono esto a las instituciones?)
SELECT * FROM ctv_items;

--Preguntas respondidas global (Como relaciono esto a las instituciones?)
SELECT * FROM ctv_user_item_answers where is_answered = 1;

--Preguntas respondidas correctamente global (Como relaciono esto a las instituciones?)
SELECT * FROM prod_classroomtv.ctv_user_item_answers where is_answered = 1 and is_correct = 1;

--Preguntas respondidas incorrectamente global (Como relaciono esto a las instituciones?)
SELECT count(*) FROM prod_classroomtv.ctv_user_item_answers where is_answered = 1 and is_correct = 0;

--Cantidad de noticias creadas global
SELECT institution_id, count(*) AS total 
FROM ctv_news
GROUP BY institution_id;

--Cantidad de noticias vistas
SELECT institution_id, count(*) 
FROM prod_classroomtv.ctv_user_navigation_logs 
WHERE PAGE LIKE 'Vista de noticia%'
GROUP BY institution_id;

--Cantdad de likes noticias  (Como relaciono esto a las instituciones?)
SELECT * 
FROM prod_classroomtv.ctv_user_likes_news;

--Cantidad de comentarios noticias global (Como relaciono esto a las instituciones?) 
SELECT *
FROM ctv_questions 
WHERE news_id IS NOT NULL



Select @@version


SELECT *
FROM ctv_users as u 
inner join ctv_user_belongs_institution as ubi on (ubi.user_id = u.id)
where ubi.is_admin != 1


SELECT *
FROM ctv_user_course_histories
where is_finish = 1

--Questions
SELECT institution_id, count(uia.id) as count_questions,
SUM(CASE WHEN is_answered = 1 THEN 1 ELSE 0 END) AS answered_questions,
SUM(CASE WHEN is_answered = 1 AND is_correct = 1 THEN 1 ELSE 0 END) AS correct_answers,
SUM(CASE WHEN is_answered = 1 AND is_correct = 0 THEN 1 ELSE 0 END) AS incorrect_answers
FROM ctv_user_item_answers  uia
INNER JOIN ctv_user_belongs_institution AS ubi 
ON ubi.user_id = uia.user_id
GROUP BY institution_id


SELECT count(ctv_user_item_answers.id) 
FROM ctv_user_item_answers 
where is_answered = 1 and is_correct = 1 and ctv_user_item_answers.user_id not in (select user_id from ctv_user_belongs_institution) 
group by user_id

