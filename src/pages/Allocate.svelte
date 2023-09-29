<script lang="ts">
  import { Link } from "svelte-routing";
  import { onMount } from "svelte";

  import { projects, buttonStyle } from "../lib/constants";
  import Chart from "../lib/Chart.svelte";
  import { format } from "d3-format";
  import ElicitHeader from "../lib/ElicitHeader.svelte";
  import { store } from "../lib/store";

  $: sortOrder = $store.sortOrder;
  $: allocations = $store.allocations;

  onMount(() => {
    setTimeout(() => {
      let localSort = sortOrder;
      if (localSort.length !== Object.keys(projects).length) {
        localSort = Object.keys(projects);
        store.setSort(localSort);
      }
      if (!localSort.every((key) => Number.isFinite(allocations[key]))) {
        const newAllocations = {
          ...Object.fromEntries(localSort.map((x) => [x, 0])),
          ...allocations,
        };
        store.setAllocation(newAllocations);
      }
    }, 600);
  });

  const MILLION = 1000000;
  const sum = (arr: number[]) => arr.reduce((x, y) => x + y, 0);
  $: totalAllocation = sum(Object.values(allocations));
  $: budgetRemaining = MILLION - totalAllocation;

  $: loading = Object.keys(allocations).length === 0;
</script>

<div>
  <ElicitHeader />
  <div class="my-8 flex flex-col items-center w-full">
    <h1 class="text-2xl">
      Now let's allocate funds! Drag the bars below to sketch how you would 
      distribute money among these projects.
    </h1>

    <div class="flex flex-col w-full items-center">
      <h1 class="text-lg">
        You have {format(",.2r")(budgetRemaining)}$ remaining
      </h1>
      {#if budgetRemaining < 0}
        <h1 class="border-red-600 border-2 rounded bg-red-400 px-8 py-4">
          You can not allocate more than $1 million total
        </h1>
      {/if}
    </div>
    {#if !loading}
      <Chart
        {sortOrder}
        {allocations}
        doubleChecking={false}
        setAllocationValue={(key, val) => store.setAllocationKey(key, val)}
      />
    {:else}
      <h1 class="text-5xl">Loading</h1>
    {/if}
    {#if budgetRemaining === 0}
      <Link
        class={buttonStyle}
        to="/check-allocate"
        on:click={() => store.setPostAllocation(allocations)}
      >
        I'm happy with my allocation amounts
      </Link>
    {/if}
  </div>
</div>
