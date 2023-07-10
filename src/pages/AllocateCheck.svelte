<script lang="ts">
  import { Link } from "svelte-routing";

  import { buttonStyle } from "../lib/constants";
  import Chart from "../lib/Chart.svelte";
  import { format } from "d3-format";
  import ElicitHeader from "../lib/ElicitHeader.svelte";
  import { store } from "../lib/store";

  $: sortOrder = $store.sortOrder;
  $: allocations = $store.postCheckAllocations;
  const MILLION = 1000000;
  const sum = (arr: number[]) => arr.reduce((x, y) => x + y, 0);
  $: totalAllocation = sum(Object.values(allocations));
  $: budgetRemaining = MILLION - totalAllocation;
</script>

<div>
  <ElicitHeader />
  <div class="my-8 flex flex-col items-center w-full">
    <h1 class="text-2xl">
      Let's add a little bit of context and see how much each of these projects
      asked for! You are free to change your allocations if you wish.
    </h1>
    <h3 class="italic">
      The lines indicate the minimum each project asked for. If there isn't a
      line then there is not minimum for that project.
    </h3>

    <div class="flex flex-col w-full items-center">
      <h1 class="text-lg">
        You have {format(",.2r")(budgetRemaining)}$ remaining
      </h1>
      {#if budgetRemaining < 0}
        <h1 class={`${buttonStyle} bg-red-400 border-red-600`}>
          You can not allocate more than $1 million total
        </h1>
      {/if}
    </div>

    <Chart
      {sortOrder}
      {allocations}
      doubleChecking={true}
      setAllocationValue={(key, val) => store.setPostAllocationKey(key, val)}
    />
    {#if budgetRemaining === 0}
      <Link to="/demographics" class={buttonStyle}>
        I'm now actually happy with my allocations
      </Link>
    {/if}
  </div>
</div>
