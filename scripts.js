document.addEventListener("DOMContentLoaded", function() {
    const image = document.getElementsByClassName("images");
    const overlay = document.querySelector(".onclick-overlay");
    const closeBtn = document.getElementsByClassName("close-btn");
    const doneBtn = document.getElementById("done-btn");
    const successful = document.querySelector(".successful");
    const numberForm = document.querySelector(".number-fill");
    const datePicker = document.getElementById("date-picker");
    const homeBtn = document.querySelector(".home");
    const voilationBtn = document.querySelector(".voilation");
    const main = document.querySelector(".main-container");
    const voilationLog = document.querySelector(".voilation-container");
    const sendMail =document.querySelector(".send-mail-container");
    const viewBtn = document.getElementsByClassName("view-btn");
    datePicker.valueAsDate = new Date();
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
        let number = " "
        let zonalCode = document.getElementById("zonalCodeSelect").value;
        let lotNumber = document.getElementById("lotNumberInput").value;
        let vehicleType = document.getElementById("vehicleTypeSelect").value;
        let vehicleId = document.getElementById("vehicleIdInput").value;
        number = zonalCode+"-"+lotNumber+"-"+vehicleType+" "+vehicleId;    
        console.log(number);
        successful.style.display ="flex";
        numberForm.style.display ="none";
    });

    homeBtn.addEventListener("click",function(){
        main.style.display="flex";
        voilationLog.style.display="none";
        voilationBtn.classList.remove("active")
        homeBtn.classList.add("active")
        sendMail.style.display="none";
    });
    voilationBtn.addEventListener("click",function(){
        main.style.display="none";
        sendMail.style.display="none";
        voilationLog.style.display="flex";
        voilationBtn.classList.add("active")
        homeBtn.classList.remove("active")

    });
    for(var i= 0;i<viewBtn.length;i++){
        viewBtn[i].addEventListener("click",function(){
            voilationLog.style.display="none";
            sendMail.style.display="flex";
        });
    }
    
    
});


// function updateImages(images) {
//     const imagesContainer = document.querySelector('.number-img');
//     imagesContainer.innerHTML='';
//     images.forEach(image => {
//         const imgElement = document.createElement('img');
//         imgElement.classList.add("images")
//         const timestamp = new Date().getTime();  // Add a timestamp to force reload
//         // Use the correct path to retrieve the image
//         imgElement.src = `/number_plate_images/${image}?t=${timestamp}`;
//         imgElement.alt = 'Number Plate Image';

//         imagesContainer.appendChild(imgElement);
        
//     });
// }


