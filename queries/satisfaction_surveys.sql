SELECT
	distinct(uia.user_id),
    ins.id as 'institution_id',
	ins.name as 'institution_name',
    i.id as item_id,
    t.title as test_title,
    class_id,
    i.author_id,
    t.course_id as 'course_id',
	c.title as 'course_title',
	c.sence_net_code as 'sencenet',
    c.sence_code as 'sencecod',
	FROM_UNIXTIME(c.start_date) as 'start_course_date',
	FROM_UNIXTIME(c.end_date) as 'end_course_date',
	i.content as 'reactivo',
	ia.content as 'respuesta',
    max_ptje,
    min_ptje,
    FROM_UNIXTIME(t.create_time,  '%Y-%m-%d') as test_create_time, FROM_UNIXTIME(t.update_time,  '%Y-%m-%d') as test_update_time,
	FROM_UNIXTIME(i.create_time,  '%Y-%m-%d') as item_create_time, FROM_UNIXTIME(i.update_time,  '%Y-%m-%d') as item_update_time
from prod_classroomtv.ctv_courses as c
inner join prod_classroomtv.ctv_institutions as ins on c.institution_id = ins.id
inner join prod_classroomtv.ctv_tests as t on c.id = t.course_id
inner join prod_classroomtv.ctv_items as i on t.id = i.test_id
inner join prod_classroomtv.ctv_user_item_answers as uia on t.id = uia.test_id AND uia.item_id = i.id
inner join prod_classroomtv.ctv_item_alternatives as ia on uia.selected_alternative_ids = ia.id
left join (select item_id,i.content, max(ia.content) as max_ptje, min(ia.content) as min_ptje
		from prod_classroomtv.ctv_tests as t
		inner join prod_classroomtv.ctv_items as i on i.test_id = t.id
		inner join prod_classroomtv.ctv_item_alternatives as ia on ia.item_id = i.id
		where  t.settings like '%"isPoll":"1"%'
		group by item_id) possible_answers
on i.id = possible_answers.item_id
WHERE
	t.settings like '%"isPoll":"1"%'
	and
	c.sence_net_code > 0
	and
	c.start_date >= 1646103599
order by c.start_date, c.title, i.content asc;

