<script lang="ts">
  import { scaleBand, scaleLinear } from "d3-scale";
  import { format } from "d3-format";
  import { minimums, explanations, maximums } from "./constants";
  import ChartBar from "./ChartBar.svelte";

  export let sortOrder: string[];
  export let allocations: Record<string, number>;
  export let doubleChecking: boolean;
  export let setAllocationValue: (key: string, val: number) => void;

  const height = 600;
  const width = 800;
  const margin = { left: 50, right: 50, top: 100, bottom: 50 };
  const innerHeight = height - margin.top - margin.bottom;
  const innerWidth = width - margin.left - margin.right;
  const MILLION = 1000000;

  let state: "dragging" | "reading" = "reading";

  $: xScale = scaleBand().domain(sortOrder).range([0, innerWidth]).padding(0.1);
  const yScale = scaleLinear().domain([0, MILLION]).range([0, innerHeight]);
  const yScaleFormatter = format("~s");
  const clamp = (x, lb, ub) => Math.max(Math.min(x, ub), lb);

  let openTooltip: { x: number; y: number; key: string } | null = null;

  $: totalAllocation = Object.values(allocations).reduce(
    (acc, x) => acc + x,
    0
  );
  $: budgetRemaining = MILLION - totalAllocation;

  let target: string | null = null;
  let tutorialDismissed = false;
</script>

<svg {width} {height}>
  <g transform={`translate(${margin.left}, ${margin.top})`}>
    {#each sortOrder as key}
      <rect
        class="stroke-1"
        x={xScale(key)}
        y={innerHeight - yScale(allocations[key]) - (allocations[key] ? 0 : 1)}
        stroke="#4f46e5"
        stroke-width={2}
        fill="#c7d2fe"
        height={clamp(
          yScale(allocations[key]) + (allocations[key] ? 0 : 5),
          0,
          innerHeight
        )}
        width={xScale.bandwidth()}
      />
      <rect
        x={xScale(key)}
        y={0}
        fill="red"
        fill-opacity={0}
        {height}
        width={xScale.bandwidth()}
        on:mouseenter={() => {
          target = key;
        }}
        on:mousedown={() => {
          state = "dragging";
        }}
        on:mousemove={(e) => {
          if (state === "dragging") {
            // @ts-ignore
            const bbox = e.target.getBoundingClientRect();
            const yVal = e.y - bbox.y;
            setAllocationValue(key, yScale.invert(innerHeight - yVal));
          }
        }}
        on:mouseup={() => {
          state = "reading";
        }}
      />
      {#if key === target}
        <ChartBar
          {setAllocationValue}
          {key}
          {allocations}
          {minimums}
          {doubleChecking}
          {budgetRemaining}
          minYPos={innerHeight - yScale(minimums[key])}
          xPos={xScale(key)}
          yPos={innerHeight - yScale(allocations[key])}
        />
      {/if}
    {/each}
    {#if doubleChecking}
      {#each Object.entries(minimums) as [key, minimum]}
        {#if minimum > 0}
          <g
            transform={`translate(${xScale(key)},
                ${innerHeight - yScale(minimum)})`}
          >
            {#if key === target}
              <text
                font-size={10}
                y={-10}
                stroke={minimum > allocations[key] ? "#b91c1c" : "#16a34a"}
              >
                Min: {yScaleFormatter(minimum)}
              </text>
            {/if}
            <line
              x1={0}
              x2={xScale.bandwidth()}
              y1={0}
              y2={0}
              stroke={minimum > allocations[key] ? "#b91c1c" : "#16a34a"}
              stroke-width={5}
            />
          </g>
        {/if}
      {/each}
    {/if}
    <g>
      <!-- x axis -->
      <line
        stroke="black"
        x1={-10}
        y1={yScale.range().at(-1)}
        x2={xScale.range().at(-1)}
        y2={yScale.range().at(-1)}
      />
      {#each sortOrder as key}
        <g transform={`translate(${xScale(key)}, ${yScale.range().at(-1)})`}>
          <text
            x={xScale.bandwidth() / 2}
            y={20}
            font-size="10"
            text-anchor="middle"
          >
            {key}
          </text>
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <text
            font-size="12"
            class="cursor-pointer"
            on:click={(e) => {
              openTooltip = { key, x: e.pageX, y: e.pageY };
            }}
            x={xScale.bandwidth() / 2}
            y={35}
            text-anchor="middle"
          >
            ⓘ
          </text>
        </g>
      {/each}
      <!-- y axis -->
      <line stroke="black" x1={0} y1={0} x2={0} y2={yScale.range().at(-1)} />
      {#each [...new Array(11)].map((_, i) => i) as index}
        <text
          x={-5}
          y={yScale(((10 - index) / 10) * MILLION)}
          text-anchor="end"
          alignment-baseline="central"
          font-size="10"
        >
          {yScaleFormatter((index / 10) * MILLION)}
        </text>
      {/each}
    </g>
  </g>
  {#if !tutorialDismissed && doubleChecking}
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <rect
      x="0"
      y={margin.top - 5}
      height={innerHeight + margin.bottom}
      {width}
      fill="black"
      opacity={0.3}
    />
    <g transform={`translate(${width * 0.3}, ${height * 0.5})`}>
      <rect
        x="-5"
        y="-15"
        width="400"
        height="50"
        stroke="#dc2626"
        stroke-width="2"
        fill="#f87171"
        rx={2}
        ry={2}
      />
      <text class="pointer-events-none">
        These bars show the min and max each project asked
      </text>
      <text class="pointer-events-none" y={20}>
        for. Click anywhere to dismiss
      </text>
      <rect
        {height}
        {width}
        fill="red"
        on:click={() => {
          tutorialDismissed = true;
        }}
        opacity={0}
        class="cursor-pointer"
      />
    </g>
  {/if}
</svg>
{#if openTooltip}
  <div>
    <!-- svelte-ignore a11y-click-events-have-key-events -->
    <div
      class="fixed left-0 right-0 top-0 bottom-0 bg-red opacity-0"
      on:click={() => {
        openTooltip = null;
      }}
    />
    <div
      class="absolute bg-gray-100 border-2 rounded shadow-lg p-2 max-w-md"
      style={`left: ${openTooltip.x}px; top: ${openTooltip.y}px`}
    >
      {explanations[openTooltip.key]}
    </div>
  </div>
{/if}
