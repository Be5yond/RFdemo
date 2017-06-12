# RFdemo
robot framework for RESTful API test demo


# 说明
* 功能分层
   1. Req.py  public library 实现基本的send逻辑和一些公共方法
   2. OpenPhp.py   project library 继承自Req，实现get post delete等方法，根据项目不同，带一些项目默认参数（用户， token，签名，时间戳等）。  
   3. conf.txt  robot resource 文件。根据项目具体功能，项目公共业务逻辑Keywords。例如：
       ```
       *** Keywords ***
       CREATE
           [Arguments]    &{args}
           ${result}=    POST    method=demo.activity.create    &{args}
           [Return]    ${result.json().get('activityId')}

       MODIFY
           [Arguments]    &{args}
           POST    method=demo.activity.modify    activityId=${ac_id}    &{args}
       ```
   4. demo.robot  testcase。 具体的testcase

   
