<script lang="ts">
  import ElicitHeader from "../lib/ElicitHeader.svelte";
  import { projects, buttonStyle } from "../lib/constants";
  // import SortableList from "svelte-sortable-list";
  import SortableList from "../lib/InsertSortList.svelte";
  import { store } from "../lib/store";

  $: sortOrder = $store.sortOrder;
  $: showNext = sortOrder.length === Object.keys(projects).length;
</script>

<div>
  <ElicitHeader />
  <div class="my-8">
    <h1> 
      <b>
        <i>Please order the following projects by your preference for them.</i>
      </b>
    </h1>
    <div class="italic h-20">Click and drag a project to reorder its importance.</div>
   
    <SortableList
      projects={projects}
      list={sortOrder.map((name, id) => ({ name, id }))}
      let:item
      key="name"
      on:sort={(ev) => {
          console.log(ev.detail);
          store.setSort(ev.detail.map((x) => x.name))
        }
      }
    >
      <div
        class="border-2 border-gray-500 px-3 rounded flex flex-col cursor-pointer"
      >
        <span class="bolder italic">
          {item.id + 1}. {item.name}
        </span>
        <span class="text-sm">{projects[item.name].description}</span>
      </div>
    </SortableList>
  </div>
</div>

{#if showNext}
  <!-- hard linked (rather than using soft Links bc of animation sync bugs that cause faulty renders) -->
  <a href="/allocate" class={buttonStyle}>I'm happy with this sort order</a>
{/if}
