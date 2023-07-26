const evtSource = new EventSource("listen");

overview2htmltab = (overview) => {

  var tableElement = document.createElement('table');
  tableElement.id = "overview-tab";

  for(let k in overview){

    var rowElement = document.createElement("tr");
    rowElement.classList.add("overview-tab-r")

    var keyElement = document.createElement("td");
    keyElement.classList.add("tab-item-key")
    keyElement.appendChild(document.createTextNode(k))

    var valElement = document.createElement("td");
    valElement.classList.add("tab-item-val")
    valElement.appendChild(document.createTextNode(overview[k]))

    rowElement.appendChild(keyElement)
    rowElement.appendChild(valElement)

    tableElement.appendChild(rowElement)

  }

  return tableElement;

}

evtSource.onmessage = (event) => {

  data = JSON.parse(event.data)

  title = data.title

  // Append to the overview able first off
  if(title == "Overview"){

    var tableContent = data.content

    if(document.getElementById("overview-tab")  !== null){
      document.getElementById("overview-tab").remove()
    }

    tableElement = overview2htmltab(tableContent)
    
    var tabWrapper = document.getElementById("overview-tab-wrapper") 
    
    tabWrapper.appendChild(tableElement)


  // Create image if it doesn't already exist i
  } else {

    if(document.getElementById("graph-image-" + title)  === null){

      // Image wrapper 
      var wrapperElement = document.createElement('div')
      wrapperElement.id = "plot-wrapper-" + title

      // Image element
      var imageElement = document.createElement('img');
      imageElement.src = "data:image/gif; base64," + data.content
      imageElement.id = "graph-image-" + title

      // Title element 
      var header = document.createElement('h2');
      var headerContent = document.createTextNode(title);
      header.appendChild(headerContent);

      // insert data into document
      document.getElementById("plot-container").appendChild(wrapperElement)
      document.getElementById("plot-wrapper-" + title).appendChild(header)
      document.getElementById("plot-wrapper-" + title).appendChild(imageElement)

    }else{
      document.getElementById("graph-image-" + title).src = "data:image/gif; base64," + data.content
    }

  }

};

