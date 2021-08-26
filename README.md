# transaviaproject

registration:
 /api/user/  [POST]
required fields:
username, email, password
login - /api/login
параметры: 
username, password

list of tasks: api/task/ [GET]
new task: api/task/ [POST]
update task with ID=i api/task/i/ [PUT]
delete task with ID=i api/task/i/ [DELETE]
change status of task with ID i = api/task/i/change_status/ [POST]


