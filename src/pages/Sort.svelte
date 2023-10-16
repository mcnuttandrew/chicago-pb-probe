<script lang="ts">
  import ElicitHeader from "../lib/ElicitHeader.svelte";
  import { projects, buttonStyle } from "../lib/constants";
  // import SortableList from "svelte-sortable-list";
  import SortableList from "../lib/InsertSortList.svelte";
  import { store } from "../lib/store";
  import { onMount } from "svelte";

  $: sortOrder = $store.sortOrder;
  $: showNext = sortOrder.length === Object.keys(projects).length;
  // let hoveredItem: false | string = false;
  let unordered = [];

  const switchToOrdered = (item, targetName, listIn) => {
    // figure out which list we are modifying
    let listInOrdered = listIn.length === sortOrder.length;

    // remove from unordered list
    let removeIdx = unordered.findIndex(el => el === item);
    let movedItem = unordered.splice(removeIdx, 1)[0];
    console.log(movedItem)

    // add to ordered list
    let addIdx = sortOrder.findIndex(el => el === targetName);
    sortOrder.splice(addIdx, 0, movedItem);
    store.setSort([...sortOrder]);

    // replace input list
    if (listInOrdered) {
      return sortOrder.map((name, id) => ({ name, id }));
    } else {
      return unordered.map((name, id) => ({ name, id }));
    }
  }
  const switchToUnordered = (item, targetName, listIn) => {
    // figure out which list we are modifying
    let listInOrdered = listIn.length === sortOrder.length;

    // remove from ordered list
    let removeIdx = sortOrder.findIndex(el => el === item);
    let movedItem = sortOrder.splice(removeIdx, 1)[0];
    store.setSort([...sortOrder]);
    console.log(movedItem)

    // add to unordered list
    let addIdx = unordered.findIndex(el => el === targetName);
    unordered.splice(addIdx, 0, movedItem);

    // replace input list
    if (listInOrdered) {
      return sortOrder.map((name, id) => ({ name, id }));
    } else {
      return unordered.map((name, id) => ({ name, id }));
    }
  }

  onMount(() => {
    Object.keys(projects).forEach(item => {
      if (!sortOrder.some(el => el == item)) {
        unordered = [...unordered, item];
      }
    });

    if (sortOrder.length === 0) {
      sortOrder.push("Placeholder");
      store.setSort([...sortOrder]);
    } 

  })
</script>

<div>
  <ElicitHeader />
  <!-- <div class="my-8">
    {#if !showNext}
      <h1> 
        <b>
          <i>Please order the following projects by your preference for them.</i>
        </b>
      </h1>
      <div class="italic h-20">Click each project below to begin ordering them.</div>
    {/if}
    <div class="flex flex-wrap justify-between">
      {#each Object.keys(projects).filter((x) => !sortOrder.find((y) => x === y)) as item} -->
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <!-- <div
          class="h-32 w-32 border-2 border-black rounded text-center flex items-center justify-center cursor-pointer bg-violet-200 my-2"
          on:click={() => {
            store.setSort([...sortOrder, item]);
          }}
          on:mouseenter={() => {
            hoveredItem = item;
          }}
          on:mouseleave={() => {
            hoveredItem = false;
          }}
        >
          {item}
        </div>
      {/each}
    </div>
    {#if !showNext}
      <div class="italic h-20">
        {#if hoveredItem}
          {projects[hoveredItem].description}
        {:else}
          Hover over a card to see an explanation for it.
        {/if}
      </div>
    {/if}
  </div> -->
  <div class="my-8">
    <h1> 
      <b>
        <i>Please order the following projects by your preference for them.</i>
      </b>
    </h1>
    <div class="italic h-20">Click and drag a project to reorder its importance.</div>

    <h3>Budget items you haven't ordered yet</h3>
    {#if unordered.length === 0}
      <div class="italic h-20">No unordered items remaining. Drop items here to remove them from your order.</div>
    {/if}
    <SortableList
      list={unordered.map((name, id) => ({ name, id }))}
      let:item
      key="name"
      group="unordered"
      switchToOrdered={switchToOrdered}
      switchToUnordered={switchToUnordered}
      on:sort={(ev) => {
        console.log("unordered sort event", ev.detail);
          // store.setSort(ev.detail.map((x) => x.name))
        }
      }
    >
      <div
        class="border-2 border-gray-500 px-3 rounded flex flex-col cursor-pointer unordered"
      > 
        <span class="bolder italic">
          {item.name}
        </span>
        <span class="text-sm">{projects[item.name].description}</span>
      </div>
    </SortableList>

    <h3>Ordered budget items</h3>
    {#if sortOrder.length === 0}
      <div class="italic h-20">No ordered items yet. Drop items here to order them.</div>
    {/if}
    {#if sortOrder.length >= 2}
      <b>Most Important</b>
    {/if}
    <SortableList
      list={sortOrder.map((name, id) => ({ name, id }))}
      let:item
      key="name"
      group="ordered"
      switchToOrdered={switchToOrdered}
      switchToUnordered={switchToUnordered}
      on:sort={(ev) => {
          console.log(ev.detail);
          store.setSort(ev.detail.map((x) => x.name))
        }
      }
    >
      <div
        class="border-2 border-gray-500 px-3 rounded flex flex-col cursor-pointer ordered"
      >
        <span class="bolder italic">
          <!-- {#if item.id === 0}
            Most Important:
          {/if}
          {#if item.id === sortOrder.length - 1}
            Least Important:
          {/if} -->
          <!-- {#if interactLookup[item.name]}
            {item.id + 1}.
          {:else} 
            <span style="width: 5px; height: 5px; background-color: grey"></span>
          {/if} {item.name} -->
          {item.id + 1}. {item.name}
        </span>
        <span class="text-sm">{projects[item.name].description}</span>
      </div>
    </SortableList>
    {#if sortOrder.length >= 2}
      <b>Least Important</b>
    {/if}
  </div>
</div>

{#if showNext}
  <!-- hard linked (rather than using soft Links bc of animation sync bugs that cause faulty renders) -->
  <a href="/allocate" class={buttonStyle}>I'm happy with this sort order</a>
{/if}
