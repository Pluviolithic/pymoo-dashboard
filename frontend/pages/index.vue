<template>
  <div id="app" class="page-wrapper">
  
    <!-- Table widgets -->
    <div v-for="(tableContent, title) in tableWidgets" id="overview-tab-wrapper" class="widget">
      <h2>
        {{title}}
      </h2>
      <table id="overview-tab">
        <tr class="overview-tab-r" v-for="(val, key) in tableContent">
          <td class="tab-item-key">{{key}}</td>
          <td class="tab-item-val">{{val}}</td>
        </tr>
      </table>
    </div>

    <!-- Image widgets --> 
    <div 
      class="widget"
      v-for="(imageContent, title) in imageWidgets" 
      v-bind:id="'plot-wrapper-' + slugify(title)"
      @click="highlightWidget(title)"
      :class="{highlighted : widgetIsHighlighted(title)}"
      >

      <h2>
        {{title}}
      </h2>
      <img 
        v-bind:src="'data:image/gif; base64,' + imageContent"
        v-bind:id="'graph-image-' + slugify(title)"
        > </img>
    </div>

  </div>

</template>

<script>

import { useEventSource } from '@vueuse/core'

import VueSSE from 'vue-sse';


export default {
  components: {
  },
  data(){
    return {
      imageWidgets : { }, 
      tableWidgets : { },
      highlightedWidget : ""
    }
  },
  // Created hook 
  created(){

    //const evtSource = useEventSource("listen");
    
    //console.log("HI") 
    //evtSource.onmessage = (event) => {

    //  console.log("I've got something!") 
    //  let data = JSON.parse(event.data)
    //
    //  let title = data.title
    //
    //  if(title == "Overview"){
    //    this.tableWidgets["Overview"] = data.content
    //  } else {
    //    this.imageWidgets[title] = data.content
    //  }

    //};

  },
  methods: {
    slugify(str){
     return str.toLowerCase().trim().replace(/[^\w\s-]/g, '').replace(/[\s_-]+/g, '-').replace(/^-+|-+$/g, '');
    }, 
    highlightWidget(title){
      this.highlightedWidget = title;
    },
    widgetIsHighlighted(title){
      return title === this.highlightedWidget
    }
  },
  computed: {
  }
}
</script>
<style>

  html {
    font-family: Open Sans,sans-serif;
  }

  body {
    margin: 0;
  }

  h1 {
    font-size: 3rem;
  }

  h2 {
    text-align: center; 
  }

  .page-wrapper{
    max-width: calc(100% - 5rem);
    padding: 5rem;
    margin: auto;
    background-color: #e8e8e8;

  }

  #overview-tab, .overview-tab-r, .overview-tab-r > td  {
    border: 1px solid black;
    border-collapse: collapse;
  }

  #overview-tab{
    font-size: 1.2rem;
  }


  .overview-tab-r > td {
    padding: 0.4rem;  
  }


  #widget-wrapper {
    display: flex;
    flex-direction: row; 
    flex-wrap: wrap;
    justify-content: space-between;
  }

  .widget {
    width: 20rem;
    padding: 2rem;
    box-shadow: 5px 5px #c6c6c6;
    background-color: white;
    margin: 2rem 0 2rem 0;
    cursor: pointer;
  }

  .widget > img {
    width: 100%;
  }

  .highlighted {
   
    /* Center in view port */ 
    position: fixed; 
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    
    width: calc(90vw - 2rem);
    height: calc(90vh - 2rem);
    margin: 0;
  }

  .highlighted.widget > img {
    height: 100%;
    width: auto;
  }



</style>
