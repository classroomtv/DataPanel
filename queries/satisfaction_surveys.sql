SELECT
	distinct(ia.user_id),
    ins.id as 'institution_id',
	ins.name as 'cliente',
    t.course_id as 'course_id',
	c.title as 'curso',
	c.sence_net_code as 'sencenet',
    c.sence_code as 'sencecod',
	FROM_UNIXTIME(c.start_date) as 'fecha inicio',
	FROM_UNIXTIME(c.end_date) as 'fecha termino',
	i.content as 'reactivo',
	a.content as 'respuesta'
    from ctv_courses as c
inner join ctv_institutions as ins on c.institution_id = ins.id
inner join ctv_tests as t on c.id = t.course_id
inner join ctv_items as i on t.id = i.test_id
inner join ctv_user_item_answers as ia on t.id = ia.test_id AND ia.item_id = i.id
inner join ctv_item_alternatives as a on ia.selected_alternative_ids = a.id
WHERE
	t.settings like '%"isPoll":"1"%'
	and
	c.sence_net_code >0
	and
	c.start_date >= 1646103599
order by c.start_date, c.title, i.content asc