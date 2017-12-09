import MySQLdb

mysql = MySQLdb
connection = mysql.connect(host = "localhost", user = "root", passwd = "HiGroup6!", db = "Easycook")
cursor=connection.cursor()

query='''
CREATE PROCEDURE get_rec(
IN uid INT
)
BEGIN
	
CREATE TEMPORARY TABLE w1
SELECT ii.name_R AS rname, SUM(weight) AS wt1
FROM Ingre ii,
(SELECT i.name_I AS iname,count(*) as weight
FROM EC_user u, Recipe r, Favorite_R f, Ingre i
WHERE u.User_id=uid and u.User_id=f.id_U and f.id_R=r.id_R and r.name_R=i.name_R
GROUP BY i.name_I) irec
WHERE ii.name_I=irec.iname
GROUP BY ii.name_R;
	
CREATE TEMPORARY TABLE w2
SELECT r.id_R AS id, r.name_R AS rname, count(f.id_U) AS wt2, AVG(rating) AS wt3
FROM Recipe r, Favorite_R f
WHERE r.id_R=f.id_R
GROUP BY r.id_R, r.name_R;

SELECT w2.id AS rid, w1.rname AS rname, w1.wt1/5+w2.wt2/10+w2.wt3 AS weight
FROM w1, w2
WHERE w1.rname NOT IN 
(SELECT r.name_R 
FROM Recipe r, Favorite_R f
WHERE f.id_U=uid and f.id_R=r.id_R)
And w1.rname=w2.rname
ORDER BY w1.wt1/5+w2.wt2/10+w2.wt3
DESC
LIMIT 20;

DROP TABLE IF EXISTS w1;
DROP TABLE IF EXISTS w2;

END
'''

cursor.execute(query)
connection.commit()
cursor.close()
connection.close()
