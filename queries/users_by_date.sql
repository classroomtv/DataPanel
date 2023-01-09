SELECT 
    ci.id,
    ci.`name` AS Cliente,
    (SELECT 
            COUNT(*)
        FROM
            prod_classroomtv.ctv_user_belongs_institution ubia
        WHERE
            ubia.institution_id = ci.id) AS 'Usuarios totales',
    (SELECT 
            COUNT(*)
        FROM
            prod_classroomtv.ctv_user_belongs_institution ubib
        WHERE
            ubib.institution_id = ci.id
                AND ubib.active = 1) AS 'Usuarios activos',
    (SELECT 
            COUNT(*)
        FROM
            prod_classroomtv.ctv_user_belongs_institution ubic
        WHERE
            ubic.institution_id = ci.id
                AND ubic.create_time >= 1514775599
                AND ubic.create_time < 1546311599) AS 'Usuarios cargados 2018',
    (SELECT 
            COUNT(*)
        FROM
            prod_classroomtv.ctv_user_belongs_institution ubic
        WHERE
            ubic.institution_id = ci.id
                AND ubic.create_time >= 1546311599
                AND ubic.create_time < 1577847599) AS 'Usuarios cargados 2019',
    (SELECT 
            COUNT(*)
        FROM
            prod_classroomtv.ctv_user_belongs_institution ubic
        WHERE
            ubic.institution_id = ci.id
                AND ubic.create_time >= 1577847599
                AND ubic.create_time < 1609469999) AS 'Usuarios cargados 2020',
    (SELECT 
            COUNT(*)
        FROM
            prod_classroomtv.ctv_user_belongs_institution ubic
        WHERE
            ubic.institution_id = ci.id
                AND ubic.create_time >= 1609469999
                AND ubic.create_time < 1641006000) AS 'Usuarios cargados 2021',
    (SELECT 
            COUNT(*)
        FROM
            prod_classroomtv.ctv_user_belongs_institution ubic
        WHERE
            ubic.institution_id = ci.id
                AND ubic.create_time >= 1641006000) AS 'Usuarios cargados 2022',
    (SELECT 
            COUNT(institution_id)
        FROM
            (SELECT 
                user_id, institution_id
            FROM
                (SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log201912
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log201911
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log201910
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log201909
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log201908
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log201907
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log201906
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log201905
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log201904
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log201903
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log201902
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log201901
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id) AS vt
            GROUP BY 1
            ORDER BY user_id) AS vt2
        WHERE
            institution_id = ci.id) AS 'Usuarios con ingreso a plataforma 2019',
    (SELECT 
            COUNT(institution_id)
        FROM
            (SELECT 
                user_id, institution_id
            FROM
                (SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202012
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202011
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202010
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202009
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202008
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202007
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202006
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202005
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202004
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202003
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202002
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202001
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id) AS vt
            GROUP BY 1
            ORDER BY user_id) AS vt2
        WHERE
            institution_id = ci.id) AS 'Usuarios con ingreso a plataforma 2020',
    (SELECT 
            COUNT(institution_id)
        FROM
            (SELECT 
                user_id, institution_id
            FROM
                (SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202112
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202111
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202110
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202109
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202108
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202107
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202106
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202105
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202104
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202103
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202102
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202101
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id) AS vt
            GROUP BY 1
            ORDER BY user_id) AS vt2
        WHERE
            institution_id = ci.id) AS 'Usuarios con ingreso a plataforma 2021',
    (SELECT 
            COUNT(institution_id)
        FROM
            (SELECT 
                user_id, institution_id
            FROM
                (SELECT 
                user_id, institution_id
            FROM
                prod_classroomtv.ctv_user_session_log
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202210
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202209
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202208
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202207
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202206
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202205
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202204
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202203
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202202
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id UNION ALL SELECT 
                user_id, institution_id
            FROM
                logs_classroomtv.ctv_user_session_log202201
            WHERE
                institution_id IS NOT NULL
                    OR institution_id != ''
            GROUP BY institution_id , user_id) AS vt
            GROUP BY 1
            ORDER BY user_id) AS vt2
        WHERE
            institution_id = ci.id) AS 'Usuarios con ingreso a plataforma 2022'
FROM
    prod_classroomtv.ctv_institutions ci;