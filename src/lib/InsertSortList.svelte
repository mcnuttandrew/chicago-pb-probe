<!-- copied and modified from https://github.com/brunomolteni/svelte-sortable-list/blob/master/SortableList.svelte -->
<script>
    import { quintOut } from "svelte/easing";
    import { crossfade } from "svelte/transition";
    import { flip } from "svelte/animate";
    import { createEventDispatcher } from "svelte";
    
    // DISPATCH
    const dispatch = createEventDispatcher();
  
    // FLIP ANIMATION
    const [send, receive] = crossfade({
      duration: d => Math.sqrt(d * 200),
  
      fallback(node, params) {
        const style = getComputedStyle(node);
        const transform = style.transform === "none" ? "" : style.transform;
  
        return {
          duration: 600,
          easing: quintOut,
          css: t => `
                      transform: ${transform} scale(${t});
                      opacity: ${t}
                  `
        };
      }
    });

    // SOURCE AND TARGET NAME FORMATTING
    const trimName = name => name.indexOf(".") > -1 ? name.slice(3) : name
  
    // DRAG AND DROP
    let isOver = false;
    const getDraggedParent = node =>
      node.dataset && node.dataset.index
        ? node.dataset
        : getDraggedParent(node.parentNode);
    const start = ev => {
      console.log("start event", ev);
      ev.dataTransfer.setData("source", ev.target.dataset.index);
      ev.dataTransfer.setData("sourceName", ev.target.childNodes[0].childNodes[0].innerHTML);
    };
    const over = ev => {
      ev.preventDefault();
      let dragged = getDraggedParent(ev.target);
      if (isOver !== dragged.id) isOver = JSON.parse(dragged.id);
    };
    const leave = ev => {
      let dragged = getDraggedParent(ev.target);
      if (isOver === dragged.id) isOver = false;
    };
    const drop = ev => {
      // are we changing lists?
      let sourceName = trimName(ev.dataTransfer.getData("sourceName"));
      let target = ev.target.parentElement;
      let targetName = trimName(target.childNodes[0].innerHTML)
      let targetInOrdered = Object.values(target.classList).some(cl => cl === "ordered");
      console.log("drag event", ev);
      console.log("source", sourceName);
      console.log("target", targetName);
      console.log("target ordered?", targetInOrdered);
      
      // where are we moving within lists?
      isOver = false;
      ev.preventDefault();
      let dragged = getDraggedParent(ev.target);
      let from = ev.dataTransfer.getData("source");
      let to = dragged.index;

      reorder(targetInOrdered, sourceName, targetName, from, to)
        .then(newList => {
          console.log("newList", newList);
          dispatch("sort", newList);
        });
      
      // // reorder
      // if (targetInOrdered && group === "unordered") {
      //   let newList = [...switchToOrdered(sourceName, targetName, list)];
      //   console.log("New list", newList);
        
      //   dispatch("sort", newList);
      // } else if (!targetInOrdered && group === "ordered") {
      //   let newList = [...switchToUnordered(sourceName, targetName, list)];
      //   console.log("New list", newList);
        
      //   dispatch("sort", newList);
      // } else {
      //   let newList = [...list];
        
      //   // insert sort
      //   const movedItem = newList.splice(from, 1)[0];
      //   newList.splice(to, 0, movedItem);

      //   dispatch("sort", newList);
      // }

      // reorder({ from, to });
    };

    // reorder
    async function reorder(targetInOrdered, sourceName, targetName, from, to) {
      let newList;
      if (targetInOrdered && group === "unordered") {
        newList = [...switchToOrdered(sourceName, targetName, list)];
        console.log("New list", newList);
      } else if (!targetInOrdered && group === "ordered") {
        newList = [...switchToUnordered(sourceName, targetName, list)];
        console.log("New list", newList);
      } else {
        newList = [...list];
        // insert sort
        const movedItem = newList.splice(from, 1)[0];
        newList.splice(to, 0, movedItem);
      }
      return await Promise.resolve(newList);
    }
    // // DISPATCH REORDER
    // import { createEventDispatcher } from "svelte";
    // const dispatch = createEventDispatcher();
    // const reorder = ({ from, to }) => {
    //   let newList = [...list];
    //   console.log("wft is the list here?", list, to, from);

    //   // AMK: modification changes the sort operation from a swap to an insert
    //   const movedItem = newList.splice(from, 1)[0];
    //   newList.splice(to, 0, movedItem);

    //   dispatch("sort", newList);
    // };
  
    // UTILS
    const getKey = item => (key ? item[key] : item);
  
    // PROPS
    export let list;
    export let key;
    export let group;
    export let switchToOrdered;
    export let switchToUnordered;
  </script>
  
  <style>
    ul {
      list-style: none;
      padding: 0;
    }
    li {
      border: 2px dotted transparent;
      transition: border 0.1s linear;
    }
    .over {
      border-color: rgba(48, 12, 200, 0.2);
    }
  </style>
  
  {#if list && list.length}
    <ul>
      {#each list as item, index (getKey(item))}
        <li
          data-index={index}
          data-id={JSON.stringify(getKey(item))}
          draggable={(getKey(item) !== "Placeholder")}
          on:dragstart={start}
          on:dragover={over}
          on:dragleave={leave}
          on:drop={drop}
          in:receive={{ key: getKey(item) }}
          out:send={{ key: getKey(item) }}
          animate:flip={{ duration: 300 }}
          class:over={getKey(item) === isOver}>
          <slot {item} {index}>
            <p>{getKey(item)}</p>
          </slot>
        </li>
      {/each}
    </ul>
  {/if}