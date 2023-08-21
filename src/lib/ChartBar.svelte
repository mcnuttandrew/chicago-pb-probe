<script lang="ts">
  import { projects } from "./constants";
  export let setAllocationValue: (key: string, val: number) => void;
  export let key: string;
  export let allocations: Record<string, number>;
  export let doubleChecking: boolean;
  export let budgetRemaining: number;
  export let xPos: number;
  export let yPos: number;

  $: menuItems = [
    {
      name: "Clear",
      action: () => setAllocationValue(key, 0),
      criterion: () => allocations[key] > 0,
      width: 35,
    },
    {
      name: "Set to cost",
      action: () => setAllocationValue(key, projects[key].est), // assumes projects have integer cost; otherwise, need to round here
      criterion: () => doubleChecking && projects[key].est,
      width: 60,
    },
    // {
    //   name: "Set to min",
    //   action: () => setAllocationValue(key, projects[key].min),
    //   criterion: () => doubleChecking && projects[key].min,
    //   width: 60,
    // },
    // {
    //   name: "Set to max",
    //   action: () => setAllocationValue(key, projects[key].max),
    //   criterion: () => doubleChecking && projects[key].max,
    //   width: 60,
    // },
    {
      name: "Fill Up",
      action: () => setAllocationValue(key, allocations[key] + budgetRemaining), // assumes all integer valued allocations to avoid rounding errors
      criterion: () => budgetRemaining > 0,
      width: 40,
    },
  ].filter((x) => x.criterion());
</script>

<g transform={`translate(${xPos + 20},${yPos})`}>
  {#if menuItems.length}
    <text font-size={10} font-weight={"bold"}>Actions</text>
  {:else}
    <text class="italic" font-size={8}>No actions</text>
    <text class="italic" font-size={8} y={8} x={2}>available</text>
  {/if}
  {#each menuItems as menuItem, idx}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <g
      transform={`translate(8, ${(idx + 1) * 20})`}
      class="cursor-pointer"
      on:click={() => menuItem.action()}
    >
      <rect
        x={-7}
        y={-11}
        width={menuItem.width}
        height={16}
        fill="white"
        rx={2}
        stroke="black"
      />
      <text font-size="9">{menuItem.name}</text>
    </g>
  {/each}
</g>
