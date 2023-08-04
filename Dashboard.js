
const { createApp, reactive, ref } = Vue;

createApp({
  // Data 
  data(){
    return {
      imageWidgets : new Set()
        

      , 
      tableWidgets : { }


    }
  }, 
  // Created hook 
  created(){

    const evtSource = new EventSource("listen");
    
    evtSource.onmessage = (event) => {
    
      let data = JSON.parse(event.data)
    
      let title = data.title
    
      // Append to the overview table first off
      if(title == "Overview"){
  
        this.tableWidgets["Overview"] = data.content

        //var tableContent = data.content
        //
        //var tabWrapper = document.getElementById("overview-tab-wrapper") 
    
        //if(document.getElementById("overview-tab")  !== null){
        //  document.getElementById("overview-tab").remove()
        //}else{
        //  var header = document.createElement('h2');
        //  var headerContent = document.createTextNode("Overview");
        //  header.appendChild(headerContent)
        //  tabWrapper.appendChild(header)
        //}
    
        //tableElement = overview2htmltab(tableContent)
    
        //tabWrapper.appendChild(tableElement)
    
    
      // Create image if it doesn't already exist 
      } else {
    
        if(document.getElementById("graph-image-" + title)  === null){
    
          // Image wrapper 
          var wrapperElement = document.createElement('div')
          wrapperElement.id = "plot-wrapper-" + title
          wrapperElement.classList.add("widget")
    
          // Image element
          var imageElement = document.createElement('img');
          imageElement.src = "data:image/gif; base64," + data.content
          imageElement.id = "graph-image-" + title
    
          // Title element 
          var header = document.createElement('h2');
          var headerContent = document.createTextNode(title);
          header.appendChild(headerContent);
    
          // Insert data into document
          document.getElementById("widget-wrapper").appendChild(wrapperElement)
          document.getElementById("plot-wrapper-" + title).appendChild(header)
          document.getElementById("plot-wrapper-" + title).appendChild(imageElement)
    
          
    
        }else{
          document.getElementById("graph-image-" + title).src = "data:image/gif; base64," + data.content
        }
    
      }
    
    };
    console.log("Setup completed")

  },
  // Setup
  setup() {
    const counter = reactive({ count: 0 });
    const message = ref('Hello World!');

    return {
      counter,
      message
    }
  }, 
  // Methods
  methods : {

  }
}).mount('#app');

