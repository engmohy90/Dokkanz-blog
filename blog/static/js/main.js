var webSocketBridge;
var ws_path = window.location.pathname + "stream/";
var username;
$(function () {
    getSocketData();
    setTimeout(function () {
        $(".alert-success").hide()
    }, 3000);

});

function getSocketData(sendData) {
    console.log("Connecting to " + ws_path);
    username = username;
    if (sendData) {
        webSocketBridge.send(sendData);
    } else {
        webSocketBridge = new channels.WebSocketBridge();
        webSocketBridge.connect(ws_path);
        webSocketBridge.listen(function (data) {
            if(Object.keys(data).indexOf('click')!=-1){
                //$('#myModal'+data['id']).modal('hide');
                $('#myModal'+data['id']).modal('show');
                return false;

            }
            if (data.error) {
                alert(data.error)
            } else {

                if (data.deleted == true) {
                    $("#post" + data.id).hide();
                } else {
                    drawBlog(data);
                }
            }
        });
    }
}

function drawBlog(data) {
    debugger;
    var content = "<div class='post' id='post" + data.id
        + "'><div><h1><a href='/blog/post/" + data.id + "'><span id='title"
        + data.id
        + "'>"
        + data.title
        + "</span>"
        + "</a></h1><small style='color: gray'> by "
        + data.author
        + "</small><small class='date'>"
        + data.created_date
        + "</small></div><br><p id='text" + data.id + "'>"
        + data.text + "<br></p>"
        + "<div id='owner"
        + data.id
        + "'><button type='button' class='btn' data-toggle='modal' data-target='#deModal"
        + data.id
        + "'> delete </button> <div class='modal fade' id='deModal"
        + data.id
        + "' role='dialog'><div class='modal-dialog'><!-- Modal content--><div class='modal-content'><div class='modal-header'><button type='button' class='close' data-dismiss='modal'>&times;</button></div><p>are you sure you want to delete this post</p><div class='modal-footer'><button type='button' class='btn btn-default' data-dismiss='modal'>no</button>"
        + "<button type='button' class='btn btn-default' onclick='deletePost(" + data.id + ")'>yes</button></div></div></div></div><button type='button' class='btn' data-toggle='modal' data-target='#myModal"
        + data.id
        + "'>edit</button><div class='modal fade' id='myModal"
        + data.id
        + "' role='dialog'><div class='modal-dialog'><!-- Modal content--><div class='modal-content'><div class='modal-header'><button type='button' class='close' data-dismiss='modal'>&times;</button><table><tr><td><label>title</label></td></tr><tr><td><input value='"
        + data.title
        + "' class='title" + data.id + "'></td></tr><td><label>post</label></td><tr><td><textarea class='text" + data.id + "'>"
        + data.text
        + "</textarea></td></tr><tr id='" + data.id + "'><td><button id='editPost"
        + data.id + "' onclick='addEditPost(this.closest(\"tr\"))'>save</button></td></tr></table><div class='modal-footer'><button type='button' class='btn' data-dismiss='modal'>Close</button></div></div></div></div></div>"
        + "</div> <hr ></div> <script> if ('"
        + username + "' != '"
        + data.author + "'){ document.getElementById('owner"
        + data.id + "').style.display = 'none';}</script>"

    if ($("#post" + data.id).length) {
        $("#post" + data.id).html(content);
    } else {
        $("#to-append-data").append(content);
    }
}

function addEditPost(post) {
    if ($(".title" + $(post).attr('id')).val() == "" || $(".text" + $(post).attr('id')).val() == "") {
        alert("Empty text");
    }
    else {
        var title = $(post).parent().find('input').val();
        var text = $(post).parent().find('textarea').val();
        var author = username;
        var method = ($(post).attr('id') ? "UPDATE" : "POST");
        var id = $(post).attr('id') || 'empty';
        d_send = {
            "id": id,
            "method": method,
            "title": title,
            "author": author,
            "text": text
        };
        getSocketData(d_send);
        if ($(post).attr('id')) {
            $('#myModal' + $(post).attr('id')).modal('hide')
        } else {
            $(".title-post").val('');
            $(".text-post").val('');
        }
    }
}

function deletePost(id) {
    d_send = {
        "id": id,
        "method": "DELETE",
        "title": "",
        "author": username,
        "text": ""
    };
    getSocketData(d_send);
    $('#deModal' + id).modal('hide')
}

 function sendClick(id){
         d_send = {
            "id": id,
            "id-click": id,
            "author": username,
             "method": "",
            "text": "trest",
            "title": "title"
        };
        getSocketData(d_send);
    }