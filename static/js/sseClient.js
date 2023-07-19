
console.log("Hello world!")
const evtSource = new EventSource("listen");

evtSource.onmessage = (event) => {
  //const newElement = document.createElement("li");
  //const eventList = document.getElementById("list");

  //newElement.textContent = `message: ${event.data}`;
  //eventList.appendChild(newElement);
 
  var imageElement = document.createElement('img');

  imageElement.src = "data:image/gif; base64," + event.data
  imageElement.width = 300
  imageElement.height = 300
  imageElement.id = "graph-image"

  // Delete existing graphs
  if(document.getElementById("graph-image")  !== null){
    document.getElementById("graph-image").remove()
  }
  

  document.getElementById("po-container").appendChild(imageElement)
  

};
