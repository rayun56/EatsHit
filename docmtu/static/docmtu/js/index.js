window.addEventListener("DOMContentLoaded", (event) => {
    document.body.addEventListener("updateInfo", function(){
        let info = document.getElementById("menuData")
        let loc = info.getAttribute("location_id");
        localStorage.setItem("location_id", loc);
        let date = info.getAttribute("date_id");
        for (let i = 0; i < document.getElementsByClassName("date-dropdown-item").length; i++) {
            let id = document.getElementsByClassName("date-dropdown-item")[i].id;
            if (id.slice(0, 9) === "location-") {
                id = id.slice(id.indexOf("date-"))
            }
            document.getElementsByClassName("date-dropdown-item")[i].id = "location-" + loc + "-" + id;
        }
        for (let i  = 0; i < document.getElementsByClassName("location-dropdown-item").length; i++) {
            let id = document.getElementsByClassName("location-dropdown-item")[i].id;
            if (id.split('-').includes("date")) {
                id = id.slice(0, id.indexOf("date-") - 1)
            }
            document.getElementsByClassName("location-dropdown-item")[i].id = id + "-date-" + date;
        }
        document.getElementById("dropdown-main").innerHTML = info.getAttribute("location_name");
        document.getElementById("date-dropdown-main").innerHTML = info.getAttribute("date_str");
        document.getElementById("date-dropdown-main").style.display = "block";
    });

    // Check for location_id in local storage
    if (!(localStorage.getItem("location_id") === null)) {
        // POST request to get menu info
        let loc = localStorage.getItem("location_id");
        document.body.dispatchEvent(new CustomEvent("doLoc-" + loc));
    }
});