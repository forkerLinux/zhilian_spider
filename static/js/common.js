function change_div(user_id){
    var str = "#div_changepass"+user_id.toString();
    var str2 = "#div_submitpass"+user_id.toString();
    $(str).attr("hidden", "True");
    $(str2).removeAttr("hidden");
}

function submit_pass(user_id) {
    var str = "#newpasswd"+user_id.toString();
    var passwd = $(str).val();

    var post_data = {
        "user_id":user_id, 
        "passwd":passwd
    };

    $.ajax({
        url: "/api/modify_passwd",         
        type: "POST",
        data: JSON.stringify(post_data),
        contentType:"application/json;charset=utf-8",
        dataType:"json",
        success:function(resp){
            if(resp['errcode'] == 0) {
                location.reload(); 
            }
            else {
                console.log(resp); 
                alert(resp['errmsg']);
            }
        },
        fail:function() {
        }
    });
}


function modify_role(user_id, type){
    var post_data = {
        "user_id":user_id,
        "type":type
    };

    $.ajax({
        url: "/api/modify_role",
        type: "POST",
        data: JSON.stringify(post_data),
        contentType:"application/json; charset=utf-8",
        dataType:"json",
        success: function(resp){
            if(resp['errcode'] == 0) {
                location.reload(); 
            }
            else {
                console.log(resp); 
                alert(resp['errmsg']);
            }
        },
        fail: function() {
        } 
    });
    /*
       修改角色
    */

}

function modify_access(user_id) {
    var post_data = {
        "user_id":user_id
    };

    $.ajax({
        url: "/api/access",         
        type: "POST",
        data: JSON.stringify(post_data),
        contentType:"application/json; charset=utf-8",
        dataType:"json",
        success: function(resp){
            if(resp['errcode'] == 0) {
                location.reload();
            }
            else {
                console.log(resp); 
                alert(resp['errmsg']);
            }
        },
        fail: function(){

        }
    });
}

