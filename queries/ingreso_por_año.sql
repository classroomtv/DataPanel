SELECT
		FROM_UNIXTIME(create_time,  '%Y-%c-%d') AS 'fecha' , institution_id, count(user_id) ,
        (
			SELECT COUNT(institution_id) FROM (SELECT user_id, institution_id FROM
(
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log201912 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log201911 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log201910 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log201909 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log201908 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log201907 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log201906 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log201905 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log201904 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log201903 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log201902 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log201901 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
) AS vt GROUP BY 1 ORDER BY user_id) AS vt2
WHERE institution_id = ci.id
		) as 'Usuarios con ingreso a plataforma 2019',
        (
			SELECT COUNT(institution_id) FROM (SELECT user_id, institution_id FROM
(
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202012 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202011 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202010 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202009 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202008 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202007 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202006 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202005 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202004 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202003 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202002 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202001 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
) AS vt GROUP BY 1 ORDER BY user_id) AS vt2
WHERE institution_id = ci.id
		) as 'Usuarios con ingreso a plataforma 2020',
		(
			SELECT COUNT(institution_id) FROM (SELECT user_id, institution_id FROM
(
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202112 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202111 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202110 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202109 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202108 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202107 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202106 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202105 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202104 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202103 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202102 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202101 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
) AS vt GROUP BY 1 ORDER BY user_id) AS vt2
WHERE institution_id = ci.id
		) as 'Usuarios con ingreso a plataforma 2021',
        (
			SELECT COUNT(institution_id) FROM (SELECT user_id, institution_id FROM
(
SELECT user_id, institution_id FROM prod_classroomtv.ctv_user_session_log where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202210 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202209 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202208 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202207 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202206 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202205 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202204 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202203 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202202 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
UNION ALL
SELECT user_id, institution_id FROM logs_classroomtv.ctv_user_session_log202201 where institution_id is not null or institution_id != '' GROUP BY institution_id, user_id
) AS vt GROUP BY 1 ORDER BY user_id) AS vt2
WHERE institution_id = ci.id
		) as 'Usuarios con ingreso a plataforma 2022'
FROM ctv_institutions ci