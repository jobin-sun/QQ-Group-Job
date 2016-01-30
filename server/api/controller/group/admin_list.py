
"""
get:
    输入:
        {
            "groupId":"xxxx"
        }

    验证管理员权限:
        是

    保存:
        相关表: modules.Resume,modules.Rank, modules.User

    返回:
        {
            "status":"success",#必需
            "msg":"xxxx",#必需
            "data":[
                "id":111,
                "adminName":"xxx",
                "groupId":"xxx",
                "userType":1|2|3
                ]

        }
post:
    输入:
        {
            "adminName":'xxx',//必需
            "password":'xxx'//必需
        }

    验证管理员权限:
        是

    保存:
        相关表: modules.GroupAdmin

    返回:
        {
            "status":"success",#必需
            "msg":"xxxx",#必需
        }
put:
    输入:
        {
            "adminName":'xxx',//必需
            "password":'xxx'//必需
        }

    验证管理员权限:
        是

    保存:
        相关表: modules.GroupAdmin

    返回:
        {
            "status":"success",#必需
            "msg":"xxxx",#必需
        }
delete:
    输入:
        {
            "id":'xxx',//必需
        }

    验证管理员权限:
        是

    保存:
        相关表: modules.GroupAdmin

    返回:
        {
            "status":"success",#必需
            "msg":"xxxx",#必需
        }
"""