<script lang="ts">
  import ElicitHeader from "../lib/ElicitHeader.svelte";
  import { explanations, buttonStyle } from "../lib/constants";
  import SortableList from "svelte-sortable-list";
  import { store } from "../lib/store";
  $: sortOrder = $store.sortOrder;
  $: showNext = sortOrder.length === Object.keys(explanations).length;
</script>

<div>
  <ElicitHeader />
  <div class="my-8">
    {#if !showNext}
      <h1>Click a project to add it</h1>
    {/if}
    <div class="flex flex-wrap">
      {#each Object.keys(explanations).filter((x) => !sortOrder.find((y) => x === y)) as item}
        <!-- svelte-ignore a11y-click-events-have-key-events -->
        <div
          class="h-32 w-32 border-2 border-black rounded text-center flex items-center justify-center cursor-pointer"
          on:click={() => {
            store.setSort([...sortOrder, item]);
          }}
        >
          {item}
        </div>
      {/each}
    </div>
  </div>
  <div class="my-8">
    {#if sortOrder.length}
      <h1>Click and drag a project to reorder its importance</h1>
    {/if}
    <SortableList
      list={sortOrder.map((name, id) => ({ name, id }))}
      let:item
      key="name"
      on:sort={(ev) => store.setSort(ev.detail.map((x) => x.name))}
    >
      <div
        class="border-2 border-gray-500 px-3 rounded flex flex-col cursor-pointer"
      >
        <span class="bolder italic">
          {#if item.id === 0}Most Important:
          {/if}{#if item.id === sortOrder.length - 1}Least Important:
          {/if}{item.name}
        </span>
        <span class="text-sm">{explanations[item.name]}</span>
      </div>
    </SortableList>
  </div>
</div>

{#if showNext}
  <!-- hard linked (rather than using soft Links bc of animation sync bugs that cause faulty renders) -->
  <a href="/allocate" class={buttonStyle}>Im happy with this sort order</a>
{/if}
