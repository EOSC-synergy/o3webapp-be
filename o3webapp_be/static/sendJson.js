function sendJSON(){ 
               
    var opID_select = document.getElementById("opID")
    var opID = opID_select.options[opID_select.selectedIndex].text
    var url = "/plot/" + opID
    // Creating a XHR object 
    var xhr = new XMLHttpRequest(); 

    // open a connection 
    xhr.open("POST", url, true); 

    // Set the request header i.e. which type of content you are sending 
    xhr.setRequestHeader("Content-Type", "application/json"); 

    // Create a state change callback 
    xhr.onreadystatechange = function () { 
        if (xhr.readyState === 4 && xhr.status === 200) { 

            // Print received data from server 
            document.getElementById("response").innerHTML = this.responseText; 

        } 
    }; 

    // Converting JSON data to string 
    var jsonData = JSON.stringify($("#plot").serializedArray()); 
    document.getElementById("request_url").innerHTML = jsonData;
    document.getElementById("response").innerHTML = "waiting for response";
    // Sending data with the request 
    xhr.send(jsonData); 
} 