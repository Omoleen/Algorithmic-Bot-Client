function riskprofilecheck(){
    if (!document.getElementById('apicheck').innerHTML.includes("<i class='bi bi-check-lg'></i>")){
        document.getElementById('apicheck').innerHTML += "<i class='bi bi-check-lg'></i>"
    }
}

