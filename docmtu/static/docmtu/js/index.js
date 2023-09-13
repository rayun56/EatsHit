window.addEventListener("DOMContentLoaded", (event) => {
    document.body.addEventListener("updateInfo", function(){
        let info = document.getElementById("menuData")
        let loc = info.getAttribute("location_id");
        for (let i = 0; i < document.getElementsByClassName("date-dropdown-item").length; i++) {
            let id = document.getElementsByClassName("date-dropdown-item")[i].id;
            if (id.slice(0, 9) === "location-") {
                id = id.slice(id.indexOf("date-"))
            }
            document.getElementsByClassName("date-dropdown-item")[i].id = "location-" + loc + "-" + id;
        }
        document.getElementById("dropdown-main").innerHTML = info.getAttribute("location_name");
        document.getElementById("date-dropdown-main").innerHTML = info.getAttribute("date_str");
        document.getElementById("date-dropdown-main").style.display = "block";
    });
});