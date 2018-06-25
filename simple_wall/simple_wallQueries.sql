-- insert into users(first_name, username, password, date_registered) values ('Michael', 'mikeymike', 'User1', curdate());
-- insert into users(first_name, username, password, date_registered) values ('Alex', 'alexthegod', 'User2', curdate());
-- insert into users(first_name, username, password, date_registered) values ('David', 'epicdavid', 'User3', curdate());
-- insert into users(first_name, username, password, date_registered) values ('Lisa', 'monalisa', 'User4', curdate());
-- insert into users(first_name, username, password, date_registered) values ('Joe', 'joeycool', 'User5', curdate());

-- insert into messages (user_id, sent_user_id, content, date_sent) values (1,4,"Hello Lisa! It's Michael", '2017-08-23');
-- insert into messages (user_id, sent_user_id, content, date_sent) values (2,1,"Michael! Answer me! ~Alex", '2015-12-18');
-- insert into messages (user_id, sent_user_id, content, date_sent) values (3,1,"Hey Michael. It's David bruh", '2018-01-20');
-- insert into messages (user_id, sent_user_id, content, date_sent) values (3,5,"Joey. It's David. Call me when you get the chance", '2016-09-17');

-- SENDING PEOPLE MESSAGES
-- insert into messages (user_id, sent_user_id, content, date_sent) values (1,2,"Yo what's up my man Alex", now());


-- Messages sent from Michael
-- Length of this query would go in the __ section (outgoing msgs)
select messages.id, users.id as sender, messages.sent_user_id as sent_to, messages.content as content, messages.date_sent as date from messages
join users on messages.user_id = users.id
where users.id=1
order by date_sent desc;

-- Messages sent to Michael
-- Length of this query would go in the __ section (incoming msgs)
select messages.id, messages.user_id as sent_from, messages.content as content, messages.date_sent as date from messages
join users on messages.sent_user_id = users.id
where users.id = 1
order by messages.id desc;
select * from users;

-- Checking whether I can delete
select messages.id, messages.content from messages
join users on messages.sent_user_id = users.id
where users.id=1
order by messages.id desc;

-- All users besides Michael
select id,first_name from users
where users.id != 1;

select * from users;
select * from messages;


