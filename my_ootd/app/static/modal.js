// 모달 띄우기
const modal = document.getElementById("modal_daily_code_img");
const buttonAddFeed = document.getElementById("daily_code_img");
buttonAddFeed.addEventListener("click", e => {
    modal.style.top = window.pageYOffset + 'px'
    modal.style.display = "flex";
    document.body.style.overflowY = "hidden"
    
});

// 모달 닫기
const modalCloseButton = document.getElementById("close_modal")
modalCloseButton.addEventListener("click", e => {
    modal.style.display = "none"
    document.body.style.overflowY = "visible"
})

// 수정 버튼 클릭 시 데일리 코디 수정 (test)
$('#daily_code_img_to_update').click(function(){
    let imgurl = "/static/image/style1.jpg"
    $.ajax({
        type:"GET",
        url: "",
        data: {},
        processData : false,
        contentType : false,
        success: function() {
            $('#daily_code_img').attr('src', imgurl)
            modal.style.display = "none"
            document.body.style.overflowY = "visible"
        }
    })
})