SELECT create_time , institution_id, logged_users
FROM (
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201712 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201711 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201710 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201709 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201708 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201707 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201706 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201705 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201704 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201703 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201702 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201701 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201812 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201811 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201810 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201809 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201808 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201807 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201806 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201805 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201804 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201803 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201802 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201801 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time', count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201912 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201911 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201910 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201909 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201908 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201907 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201906 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201905 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201904 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201903 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201902 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log201901 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL 
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202012 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202011 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202010 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202009 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202008 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202007 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202006 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202005 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202004 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202003 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202002 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202001 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202112 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202111 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202110 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202109 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202108 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202107 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202106 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202105 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202104 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202103 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202102 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202101 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202210 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202209 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202208 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202207 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202206 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202205 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202204 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202203 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202202 where institution_id is not null or institution_id != '' GROUP BY institution_id
UNION ALL
SELECT FROM_UNIXTIME(create_time,  '%Y-%m-%d') AS 'create_time',count(user_id) as logged_users, institution_id FROM logs_classroomtv.ctv_user_session_log202201 where institution_id is not null or institution_id != '' GROUP BY institution_id
) as V
ORDER by create_time;
