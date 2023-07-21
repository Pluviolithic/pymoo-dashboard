const evtSource = new EventSource("listen");

evtSource.onmessage = (event) => {

  data = JSON.parse(event.data)

  title = data.title

  // Create image if it doesn't already exist 
  if(document.getElementById("graph-image-" + title)  === null){

    // Image wrapper 
    var wrapperElement = document.createElement('div')
    wrapperElement.id = "plot-wrapper-" + title

    // Image element
    var imageElement = document.createElement('img');
    imageElement.src = "data:image/gif; base64," + data.image
    imageElement.id = "graph-image-" + title

    // Title element 
    var header = document.createElement('h2');
    var headerContent = document.createTextNode(title);
    header.appendChild(headerContent);

    // insert data into documeent
    document.getElementById("plot-container").appendChild(wrapperElement)
    document.getElementById("plot-wrapper-" + title).appendChild(header)
    document.getElementById("plot-wrapper-" + title).appendChild(imageElement)

  }else{
    document.getElementById("graph-image-" + title).src = "data:image/gif; base64," + data.image
  }

};

