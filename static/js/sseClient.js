
console.log("Hello world!")
const evtSource = new EventSource("listen");

evtSource.onmessage = (event) => {
  //const newElement = document.createElement("li");
  //const eventList = document.getElementById("list");

  //newElement.textContent = `message: ${event.data}`;
  //eventList.appendChild(newElement);
  console.log(`message: ${event.data}`)

};
