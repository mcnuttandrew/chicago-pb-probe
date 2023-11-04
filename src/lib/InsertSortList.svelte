<!-- copied and modified from https://github.com/brunomolteni/svelte-sortable-list/blob/master/SortableList.svelte -->
<script>
    import { quintOut } from "svelte/easing";
    import { crossfade } from "svelte/transition";
    import { flip } from "svelte/animate";
    import { createEventDispatcher } from "svelte";
    import { onMount } from "svelte";
    
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
      let sourceInOrdered = list.findIndex(d => d.name === sourceName) !== -1;
      let targetName = trimName(ev.target.parentElement.childNodes[0].innerHTML);
      let targetInOrdered = list.findIndex(d => d.name === targetName) !== -1;
      console.log("drag event", ev);
      console.log("source", sourceName);
      console.log("source ordered?", sourceInOrdered);
      console.log("target", targetName);
      console.log("target ordered?", targetInOrdered);
      
      // where are we moving within lists?
      isOver = false;
      ev.preventDefault();
      let dragged = getDraggedParent(ev.target);
      let from = ev.dataTransfer.getData("source");
      let to = dragged.index;

      reorder(sourceInOrdered, targetInOrdered, sourceName, targetName, from, to)
        .then(newList => {
          console.log("new ordered list", newList);
          dispatch("sort", newList);
        });
    };

    // reorder
    async function reorder(sourceInOrdered, targetInOrdered, sourceName, targetName, from, to) {
      let newList = [...list];
      if (!sourceInOrdered && targetInOrdered) {
        // remove from unordered list
        let removeIdx = unordered.findIndex(el => el === sourceName);
        let movedItem = unordered.splice(removeIdx, 1)[0];
        console.log("moving", movedItem)

        // add to ordered list
        let addIdx = newList.findIndex(el => el === targetName);
        newList.splice(addIdx, 0, movedItem);
      } else if (sourceInOrdered && !targetInOrdered) {
        // remove from ordered list
        let removeIdx = newList.findIndex(el => el === sourceName);
        let movedItem = newList.splice(removeIdx, 1)[0];
        // store.setSort([...sortOrder]);
        console.log("moving", movedItem)

        // add to unordered list
        let addIdx = unordered.findIndex(el => el === targetName);
        unordered.splice(addIdx, 0, movedItem);
      } else {
        // insert sort within same list
        const movedItem = newList.splice(from, 1)[0];
        newList.splice(to, 0, movedItem);
      }
      
      return await Promise.resolve(newList);
    }
    // const switchToOrdered = (item, targetName, listIn) => {
    //   // figure out which list we are modifying
    //   let listInOrdered = listIn.length === list.length;

    //   // remove from unordered list
    //   let removeIdx = unordered.findIndex(el => el === item);
    //   let movedItem = unordered.splice(removeIdx, 1)[0];
    //   console.log(movedItem)

    //   // add to ordered list
    //   let addIdx = list.findIndex(el => el === targetName);
    //   list.splice(addIdx, 0, movedItem);
    //   // store.setSort([...sortOrder]);

    //   // replace input list
    //   if (listInOrdered) {
    //     return list.map((name, id) => ({ name, id }));
    //   } else {
    //     return unordered.map((name, id) => ({ name, id }));
    //   }
    // }
    // const switchToUnordered = (item, targetName, listIn) => {
    //   // figure out which list we are modifying
    //   let listInOrdered = listIn.length === list.length;

    //   // remove from ordered list
    //   let removeIdx = list.findIndex(el => el === item);
    //   let movedItem = list.splice(removeIdx, 1)[0];
    //   // store.setSort([...sortOrder]);
    //   console.log(movedItem)

    //   // add to unordered list
    //   let addIdx = unordered.findIndex(el => el === targetName);
    //   unordered.splice(addIdx, 0, movedItem);

    //   // replace input list
    //   if (listInOrdered) {
    //     return list.map((name, id) => ({ name, id }));
    //   } else {
    //     return unordered.map((name, id) => ({ name, id }));
    //   }
    // }
  
    // UTILS
    const getKey = item => (key ? item[key] : item);
    const updateUnordered = (ordered) => {
      let newUnordered = [];
      let idx = 0;
      Object.keys(projects).forEach(item => {
        if (!ordered.some(el => el == item)) {
          // unordered = [...unordered, item];
          newUnordered.push({name: item, id: idx});
          idx++;
        }
      });

      return newUnordered
    }
  
    // PROPS
    export let projects;
    export let list;
    export let key;

    $: unordered = updateUnordered(list);

    onMount(() => {
      if (list.length === 0) {
        list.push({name: "Placeholder", id: 0});
        // store.setSort([...sortOrder]);
      } 
      console.log(unordered);
      console.log(list);
    });
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

  <h3>Budget items you haven't ordered yet</h3>
  {#if unordered && unordered.length === 0}
    <div class="italic h-20">No unordered items remaining. Drop items here to remove them from your order.</div>
  {/if}
  {#if unordered && unordered.length}
    <ul>
      {#each unordered as item, index (getKey(item))}
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

  <h3>Ordered budget items</h3>
  {#if list && list.length === 0}
    <div class="italic h-20">No ordered items yet. Drop items here to order them.</div>
  {/if}
  {#if list && list.length >= 2}
    <b>Most Important</b>
  {/if}
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
  {#if list && list.length >= 2}
    <b>Least Important</b>
  {/if}