use new_schema;
-- create table course(CNO char(8) primary key,
--          NAME VARCHAR(40) NOT NULL,
--          TNO CHAR(7) NOT NULL)
-- create table student(SNO char(11) primary key,
--                     NAME varchar(4) not null,
-- 						GENDER char(6) not null,
--                       BIRTHDAY datetime not null,
--                       DEPART int not null);
-- create table teacher(TNO CHAR(7) primary key,
-- 					NAME VARCHAR(4) not null,
--                     GENDER char(6) not null,
--                     BIRTHDAY datetime not null,
--                     POSITION char(25) not null,
--                     DEPART INT not null)
-- create table score(SNO char(11),
--                    CNO char(8) ,
--                    DEGREE int, 
-- 				   foreign key(SNO) references student(SNO),
--                    foreign key(CNO) references course(CNO))
-- LOAD DATA INFILE 'Course.csv' 
-- INTO TABLE course 
-- FIELDS TERMINATED BY ',';
-- LOAD DATA INFILE 'Student.csv' 
-- INTO TABLE student 
-- FIELDS TERMINATED BY ',';
-- LOAD DATA INFILE 'Score.csv' 
-- INTO TABLE score
-- FIELDS TERMINATED BY ',';
-- LOAD DATA INFILE 'Teacher.csv' 
-- INTO TABLE teacher
-- FIELDS TERMINATED BY ',';

-- alter table student add AGE int not null;

-- update student
-- set AGE=2023-year(BIRTHDAY);

-- update student
-- set AGE=AGE+2;

-- alter table student
-- modify AGE CHAR(2);

-- alter table student
-- drop AGE;

-- create table teacher_course(TNO CHAR(7),
-- 								  NUM_COURSE INT);
--  
-- alter table teacher_course
-- add primary key(TNO);

-- insert into teacher_course(TNO,NUM_COURSE)
-- select teacher.TNO,temp.NUM_COURSE
-- from teacher left outer join
-- (select TNO,count(CNO) from course group by TNO) as temp(TNO,NUM_COURSE)
-- on teacher.TNO=temp.TNO;

-- delete from teacher_course where NUM_COURSE is null;

-- drop table teacher_course;

-- insert into student(SNO,NAME,GENDER,BIRTHDAY,DEPART)
-- values('PB21000224','CHX','male','2004-2-24 00:00:00',229);

-- insert into student(SNO,NAME,GENDER,BIRTHDAY,DEPART)
-- values('PB21000227','jjy','male','2004-3-3 00:00:00',229);

-- insert into student(SNO,NAME,GENDER,BIRTHDAY,DEPART)
-- values('PB21000211','py','male','2004-12-24 00:00:00',229);

-- insert into score(SNO,CNO,DEGREE)
-- values('PB21000224','20230402',95);
-- insert into score(SNO,CNO,DEGREE)
-- values('PB21000224','20230410',97);
-- insert into score(SNO,CNO,DEGREE)
-- values('PB21000224','20230412',99);

-- delete from score
-- where score.SNO='PB21000224' and
--       score.DEGREE<=ALL(select temp.DEGREE
--               from (select DEGREE
-- 			        from score
--                     where SNO='PB21000224') 
--                     as temp(DEGREE));

-- create index NAME_INDEX ON course(NAME);

-- create unique index TNO_INDEX ON teacher(TNO);

-- create index RECORD_INDEX on score(SNO DESC,DEGREE ASC)

-- show index from score;

-- drop index TNO_INDEX on teacher;

-- select SNO,NAME
-- from student
-- where DEPART=
-- 	(select DEPART
--    from student
--     where SNO='PB21000224')
 
-- select SNO,NAME
-- from student
-- where DEPART=
-- 	(select DEPART
--     from student
--     where SNO='PB21000224')
--     and SNO<>'PB21000224';

-- select SNO,NAME
-- from student
-- where DEPART=
-- 	(select DEPART
--     from student
--     where NAME='jjy');

-- select SNO,NAME
-- from student
-- where DEPART not in
-- 	(select DEPART
--     from student
--     where SNO='PB21000227' or SNO='PB21000211')

-- select TNO,NAME
-- from teacher
-- where TNO in
-- (select TNO
-- from course
-- where CNO in
-- (select CNO
-- from score
-- where SNO='PB21000224'));

-- select count(*)
-- from (select TNO
-- from teacher
-- where DEPART=11 or DEPART=229) as temp(TNO);

-- select score.SNO,NAME,DEGREE
-- from score,student
-- where CNO in
-- (select CNO from course where NAME='DB_Design')
-- and DEGREE>=89 and score.SNO=student.SNO;

-- select distinct student.SNO,NAME
-- from student,score
-- where (score.CNO in
-- (select CNO
-- from teacher
-- where NAME='ZDH')
-- and score.SNO=student.SNO);

-- select  SNO, DEGREE
-- from score
-- where CNO in
-- (select CNO
-- from course
-- where NAME='operating_system')
-- order by DEGREE desc;

-- select course.CNO,NAME,avg(DEGREE)
-- from course left join score on(course.CNO=score.CNO)
-- group by CNO;

-- select course.CNO,NAME,max(DEGREE),min(DEGREE),max(DEGREE)-min(DEGREE)
-- from course,score
-- where course.CNO=score.CNO
-- group by CNO;

-- select distinct teacher.TNO,teacher.NAME
-- from teacher,score,course
-- where course.CNO=score.CNO and DEGREE<72 and course.TNO=teacher.TNO;

-- select student.SNO,NAME
-- from student,score    
-- where student.SNO=score.SNO
-- group by SNO
-- having count(CNO)>=2

-- select temp.SNO,avg(temp.DEGREE)
-- from (select student.SNO,DEGREE
-- from student left join score on(student.SNO=score.SNO)) as temp(SNO,DEGREE)
-- group by temp.SNO;

-- select temps.DEPART,count(temps.SNO),avg(temps.DEGREE)
-- from (select temp.DEPART,temp.SNO,avg(temp.DEGREE)
-- from (select DEPART,student.SNO,DEGREE
-- from student left join score on(student.SNO=score.SNO)) as temp(DEPART,SNO,DEGREE)
-- group by temp.SNO) as temps(DEPART,SNO,DEGREE)
-- group by DEPART

-- select NAME
-- from student x
-- where not exists(
-- select *
-- from score
-- where score.SNO=x.SNO and score.CNO in(
-- select CNO
-- from course
-- where NAME='Data_Mining'))

-- select course.NAME,avg(2023-year(student.BIRTHDAY))
-- from course left join score on(score.CNO=course.CNO)
-- left join student on(score.SNO=student.SNO)
-- group by course.NAME




-- select student.SNO,student.NAME
-- from student,score
-- where student.SNO=score.SNO and score.CNO in (
-- select CNO
-- from course
-- where NAME like "%Computer%");

-- select SNO,CNO,DEGREE
-- from score x
-- where x.DEGREE-12 >
-- (select avg(DEGREE) from score y where y.CNO=x.CNO group by CNO) ;

-- create view db_female_student(SNO,NAME,GENDER,BIRTHDAY,DEPART)
-- as select * from student where GENDER='female'
-- with check option

-- update db_female_student
-- set NAME='CHX'
-- where SNO='PB210000016'

-- select SNO,NAME
-- from db_female_student
-- where 2023-year(BIRTHDAY)<21;

-- insert into db_female_student
-- values('SA210110021',' QXY','female','1997-07-27 00:00:00','12');
-- select * from  db_female_student

-- insert into db_female_student
-- values('SA210110023',' DPC','male','1997-04-27 00:00:00','11');

-- drop view db_female_student


-- create table teacher_salary(
-- TNO char(7) primary key,
-- SAL float
-- )

-- DELIMITER //
-- create trigger TS_T1
-- BEFORE insert on teacher_salary 
-- for each row
-- if new.TNO not in (select TNO from teacher) then
-- 	SIGNAL SQLSTATE '45000'
--     SET MESSAGE_TEXT = "have no such TNO";
-- END IF//
-- DELIMITER ;

-- DELIMITER //
-- create trigger TS_T2
-- BEFORE update on teacher_salary 
-- for each row
-- if new.TNO not in (select TNO from teacher) then
-- 	SIGNAL SQLSTATE '45000'
--     SET MESSAGE_TEXT = "have no such TNO";
-- END IF//
-- DELIMITER ;

-- insert into teacher_salary
-- values("TA9002",7000);
-- insert into teacher_salary
-- values("TA90022",7000);
-- update teacher_salary
-- set TNO="TA9002"
-- where TNO="TA90022"

-- DELIMITER //
-- create trigger TS_T3
-- BEFORE update on teacher_salary 
-- for each row
-- if (new.SAL < 4000 and (select position from teacher where new.TNO=teacher.TNO)="Instructor") or
--    (new.SAL < 5000 and (select position from teacher where new.TNO=teacher.TNO)="Associate Professor") or
--    (new.SAL < 6000 and (select position from teacher where new.TNO=teacher.TNO)="Professor") then
-- 	SIGNAL SQLSTATE '45000'
--     SET MESSAGE_TEXT = "the salary is not correct";
-- END IF//
-- DELIMITER ;

-- DELIMITER //
-- create trigger TS_T4
-- BEFORE insert on teacher_salary 
-- for each row
-- if (new.SAL < 4000 and (select position from teacher where new.TNO=teacher.TNO)="Instructor") or
--    (new.SAL < 5000 and (select position from teacher where new.TNO=teacher.TNO)="Associate Professor") or
--    (new.SAL < 6000 and (select position from teacher where new.TNO=teacher.TNO)="Professor") then
-- 	SIGNAL SQLSTATE '45000'
--     SET MESSAGE_TEXT = "the salary is not correct";
-- END IF//
-- DELIMITER ;

-- insert into teacher_salary
-- values("TA90023",2000)

-- insert into teacher_salary
-- values("TA90023",5000);

-- update teacher_salary
-- set SAL="1000"
-- where TNO="TA90023"

-- drop trigger TS_T1;
-- drop trigger TS_T2;
-- drop trigger TS_T3;
-- drop trigger TS_T4;

-- 将 score 表中的 Data_Mining 课程成绩设为空值，然后在 score 表查询学生学号和分数，
-- 并按分数升序展示。观察 NULL 在 MySQL 中的大小是怎样的？

-- update score
-- set DEGREE=NULL
-- where CNO in 
-- (select CNO from course where score.CNO=course.CNO and course.NAME="Data_Mining");

-- select SNO,DEGREE
-- from score
-- order by DEGREE ASC;

-- null不参与比较大小，但是在数据排序的时候排在最小值的前面

-- 查看比DB_DESIGN课程平均分高的人
-- select student.NAME
-- from score x,student
-- where student.SNO=x.SNO and 
-- (x.DEGREE > (select avg(DEGREE) from score y,course where course.NAME="DB_DESIGN" and course.CNO=y.CNO))
-- and (x.CNO in (select course.CNO from score z,course where course.NAME="DB_DESIGN" and course.CNO=z.CNO));

-- 将DB_DESIGN课程的成绩由高到低排出一个试图，随后删除
-- create view DB_DESIGN_SCORE(SNO,DEGREE)
-- as
-- select score.SNO, score.DEGREE 
-- from score,course
-- where score.CNO=course.CNO and course.NAME="DB_DESIGN"
-- order by  score.DEGREE desc;
-- drop view DB_DESIGN_SCORE

-- 求出所有有成绩的同学平均成绩排名,只显示学号
-- select SNO,avg(score.DEGREE) avg_degree
-- from score
-- group by SNO
-- order by avg_degree desc

