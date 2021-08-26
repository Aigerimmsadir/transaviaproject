# transaviaproject
SETUP:
USE VS Code__
open root folder, CTRL-Shift-P "Rebuild and Reopen in container"__

then in terminal:
python3 manage.py runserver

BASIC URLS:

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
get my tasks = api/task/get_my_tasks/ [GET]
    parameters:
        only_mine - Boolean, if you want to get only tasks assigned to you. Default = True. If set False, you will get also tasks you observe.

get all my task status changes - api/task_status_change/my_changes/ [GET]
