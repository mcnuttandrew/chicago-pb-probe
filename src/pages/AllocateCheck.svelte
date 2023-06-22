<script lang="ts">
  import { Link } from "svelte-routing";

  import { explanations, buttonStyle, minimums } from "../lib/constants";
  import Chart from "../lib/Chart.svelte";
  import { format } from "d3-format";
  import ElicitHeader from "../lib/ElicitHeader.svelte";
  import { store } from "../lib/store";

  $: sortOrder = $store.sortOrder;
  $: allocations = $store.postCheckAllocations;
  $: {
    // let localSort = sortOrder;
    // if (localSort.length !== Object.keys(explanations).length) {
    //   localSort = Object.keys(explanations);
    //   store.setSort(localSort);
    // }
    // if (!localSort.every((key) => Number.isFinite(allocations[key]))) {
    //   const newAllocations = {
    //     ...Object.fromEntries(localSort.map((x) => [x, 0])),
    //     ...allocations,
    //   };
    //   store.setAllocation(newAllocations);
    // }
  }
  const MILLION = 1000000;
  const sum = (arr: number[]) => arr.reduce((x, y) => x + y, 0);
  $: totalAllocation = sum(Object.values(allocations));
  $: budgetRemaining = MILLION - totalAllocation;
</script>

<div>
  <ElicitHeader />
  <div class="my-8">
    <h1 class="text-2xl">
      Let's add a little bit of context and see how much each of these projects
      asked for! You are free to change your allocations if you wish.
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

    <Chart
      {sortOrder}
      {allocations}
      doubleChecking={true}
      setAllocationValue={(key, val) => store.setPostAllocationKey(key, val)}
    />
  </div>

  {#if budgetRemaining === 0}
    <Link to="/demographics" class={buttonStyle}>
      I'm now actually happy with my allocations
    </Link>
  {/if}
</div>
