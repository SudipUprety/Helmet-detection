document.addEventListener("DOMContentLoaded", function() {
    const image = document.getElementsByClassName("images")
    const overlay = document.querySelector(".onclick-overlay")
    const closeBtn = document.getElementsByClassName("close-btn")
    const doneBtn = document.getElementById("done-btn")
    const successful = document.querySelector(".successful")
    const numberForm = document.querySelector(".number-fill")
    const datePicker = document.getElementById("date-picker")
    const homeBtn = document.querySelector(".home")
    const voilationBtn = document.querySelector(".voilation")
    const main = document.querySelector(".main-container")
    const voilationLog = document.querySelector(".voilation-container")

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
        successful.style.display ="flex";
        numberForm.style.display ="none";
    });

    homeBtn.addEventListener("click",function(){
        main.style.display="flex";
        voilationLog.style.display="none";
        voilationBtn.classList.remove("active")
        homeBtn.classList.add("active")
    });
    voilationBtn.addEventListener("click",function(){
        main.style.display="none";
        voilationLog.style.display="flex";
        voilationBtn.classList.add("active")
        homeBtn.classList.remove("active")

    });
    
});


// function updateImages(images) {
//     const imagesContainer = document.getElementById('number-img');
//     // Create an unordered list for the image
//     imagesContainer.innerHTML='';
//     images.forEach(image => {
//         const imgElement = document.createElement('img');
//         imgElement.classList.add("images")
//         const timestamp = new Date().getTime();  // Add a timestamp to force reload
//         // Use the correct path to retrieve the image
//         imgElement.src = /number_plate_images/${image}?t=${timestamp};
//         imgElement.alt = 'Number Plate Image';
//           // Attach click event to each image

//         imagesContainer.appendChild(imgElement);
        
//     });
// }