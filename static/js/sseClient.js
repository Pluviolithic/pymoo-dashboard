
console.log("Hello world!")
const evtSource = new EventSource("listen");

evtSource.onmessage = (event) => {
  //const newElement = document.createElement("li");
  //const eventList = document.getElementById("list");

  //newElement.textContent = `message: ${event.data}`;
  //eventList.appendChild(newElement);
 

  // Delete existing graphs
  if(document.getElementById("graph-image")  === null){

    var imageElement = document.createElement('img');

    imageElement.src = "data:image/gif; base64," + event.data

    imageElement.id = "graph-image"

    document.getElementById("po-container").appendChild(imageElement)

  }else{
    document.getElementById("graph-image").src = "data:image/gif; base64," + event.data
  }
  

  

};
