document.addEventListener("DOMContentLoaded", function() {
    const image = document.getElementsByClassName("images")
    const overlay = document.querySelector(".onclick-overlay")
    const closeBtn = document.getElementsByClassName("close-btn")
    const doneBtn = document.getElementById("done-btn")
    const successful = document.querySelector(".successful")
    const numberForm = document.querySelector(".number-fill")
    for (var i = 0; i < image.length; i++) {
        image[i].addEventListener("click", function() {
            overlay.style.display = "block";
            successful.style.display ="none";
            numberForm.style.display ="flex";
        });
    }

    for (var i=0;i<closeBtn.length;i++){
        closeBtn[i].addEventListener("click",function(){
            overlay.style.display ="none";
        });
    }
    doneBtn.addEventListener("click",function(){
        successful.style.display ="flex";
        numberForm.style.display ="none";
    });
    
});
