// 버튼 클릭 시 사진이 하나만 바뀌는 현상 있음

// 상의 (test)
$('#btn_top').click(function(){
    let imgurl = "/static/image/tshirt1.jpg"
    $.ajax({
        type:"GET",
        url: "",
        data: {},
        processData : false,
        contentType : false,
        success: function() {
            $('#img_1').attr('src', imgurl)
        }
    })
})

// 하의 (test)
$('#btn_pants').click(function(){
    let imgurl = "/static/image/profile.png"
    $.ajax({
        type:"GET",
        url: "",
        data: {},
        processData : false,
        contentType : false,
        success: function() {
            $('#img_1').attr('src', imgurl)
        }
    })
})