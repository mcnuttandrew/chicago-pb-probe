<script lang="ts">
  export let setAllocationValue: (key: string, val: number) => void;
  export let key: string;
  export let allocations: Record<string, number>;
  export let minimums: Record<string, number>;
  export let doubleChecking: boolean;
  export let budgetRemaining: number;
  export let xPos: number;
  export let yPos: number;
  $: menuItems = [
    {
      name: "Clear",
      action: () => setAllocationValue(key, 0),
      criterion: () => allocations[key] > 0,
      width: 40,
    },
    {
      name: "Set to min",
      action: () => setAllocationValue(key, minimums[key]),
      criterion: () => doubleChecking && minimums[key],
      width: 65,
    },
    {
      name: "Fill Up",
      action: () => setAllocationValue(key, allocations[key] + budgetRemaining),
      criterion: () => budgetRemaining > 0,
      width: 45,
    },
  ].filter((x) => x.criterion());
</script>

<g transform={`translate(${xPos},${yPos - menuItems.length * 30})`}>
  {#if menuItems.length}
    <text font-size={10} font-weight={"bold"}>Actions</text>
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
        rx={5}
        stroke="black"
      />
      <text font-size="10">{menuItem.name}</text>
    </g>
  {/each}
</g>
