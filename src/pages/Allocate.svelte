<script lang="ts">
  import { Link } from "svelte-routing";
  import { onMount } from "svelte";

  import { explanations, buttonStyle, minimums } from "../lib/constants";
  import Chart from "../lib/Chart.svelte";
  import { format } from "d3-format";
  import ElicitHeader from "../lib/ElicitHeader.svelte";
  import { store } from "../lib/store";

  $: sortOrder = $store.sortOrder;
  $: allocations = $store.allocations;

  onMount(() => {
    setTimeout(() => {
      let localSort = sortOrder;
      if (localSort.length !== Object.keys(explanations).length) {
        localSort = Object.keys(explanations);
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

  $: console.log(allocations, budgetRemaining);
</script>

<div>
  <ElicitHeader />
  <div class="my-8">
    <h1 class="text-2xl">
      Now let's allocate funds. Draw bars to distribute money among your top 4
      preferred projects.
    </h1>

    <div class="flex w-full justify-between">
      <h1 class="text-lg">
        You have {format(",.2r")(budgetRemaining)}$ remaining
      </h1>
      <h1 class="text-lg text-red-400">
        {#if budgetRemaining < 0}
          You can not allocate more than $1 million total
        {/if}
      </h1>
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
  </div>

  {#if budgetRemaining === 0}
    <Link
      class={buttonStyle}
      to="/check-allocate"
      on:click={() => store.setPostAllocation(allocations)}
    >
      I'm happy with this allocation amount
    </Link>
  {/if}
</div>
