<script lang="ts">
  import { Link } from "svelte-routing";
  import { scaleBand, scaleLinear } from "d3-scale";
  import { explanations, buttonStyle, minimums } from "../lib/constants";
  import { format } from "d3-format";
  import ElicitHeader from "../lib/ElicitHeader.svelte";
  import { store } from "../lib/store";

  $: sortOrder = $store.sortOrder;
  $: allocations = $store.allocations;
  $: {
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
  }
  const MILLION = 1000000;
  const height = 600;
  const width = 1000;
  const margin = { left: 50, right: 50, top: 50, bottom: 50 };
  const innerHeight = height - margin.top - margin.bottom;
  const innerWidth = width - margin.left - margin.right;
  $: xScale = scaleBand().domain(sortOrder).range([0, innerWidth]).padding(0.1);
  const yScale = scaleLinear().domain([0, MILLION]).range([0, innerHeight]);
  const yScaleFormatter = format("~s");

  type State = "dragging" | "reading" | "double-check-tutorial";
  let state: State = "reading";
  $: doubleChecking = false;

  $: console.log(minimums);
  let target: string | null = null;
  $: totalAllocation = Object.values(allocations).reduce(
    (acc, x) => acc + x,
    0
  );
  $: budgetRemaining = MILLION - totalAllocation;

  const clamp = (x, lb, ub) => Math.max(Math.min(x, ub), lb);
  let openTooltip: { x: number; y: number; key: string } | null = null;
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

    <svg {width} {height}>
      <g transform={`translate(${margin.left}, ${margin.top})`}>
        {#each sortOrder as key}
          <rect
            class="stroke-1"
            x={xScale(key)}
            y={innerHeight -
              yScale(allocations[key]) -
              (allocations[key] ? 0 : 1)}
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
            on:mouseleave={() => {
              // target = null;
            }}
            on:mousedown={() => {
              state = "dragging";
            }}
            on:mousemove={(e) => {
              if (state === "dragging") {
                // @ts-ignore
                const bbox = e.target.getBoundingClientRect();
                const yVal = e.y - bbox.y;
                store.setAllocationKey(key, yScale.invert(innerHeight - yVal));
                // allocations[key] = yScale.invert(innerHeight - yVal);
              }
            }}
            on:mouseup={() => {
              state = "reading";
            }}
          />
          {#if key === target}
            <g
              transform={`translate(${xScale(key)},${
                innerHeight - yScale(allocations[key]) - 20
              })`}
            >
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              {#if allocations[key] > 0}
                <g
                  transform={`translate(${xScale.bandwidth() * 0})`}
                  class="cursor-pointer"
                  on:click={() => {
                    store.setAllocationKey(key, 0);
                    // allocations[key] = 0;
                  }}
                >
                  <text
                    alignment-baseline="central"
                    text-anchor="start"
                    font-size="10"
                  >
                    Clear
                  </text>
                </g>
              {/if}
              {#if doubleChecking && minimums[key]}
                <!-- svelte-ignore a11y-click-events-have-key-events -->
                <g
                  transform={`translate(${xScale.bandwidth() * 0.5}, 10)`}
                  class="cursor-pointer"
                  font-size="10"
                  on:click={() => {
                    store.setPostAllocationKey(key, minimums[key]);
                  }}
                >
                  <text alignment-baseline="central" text-anchor="middle">
                    Set to min
                  </text>
                </g>
              {/if}
              <!-- svelte-ignore a11y-click-events-have-key-events -->
              {#if budgetRemaining > 0}
                <g
                  transform={`translate(${xScale.bandwidth() * 1})`}
                  class="cursor-pointer"
                  font-size="10"
                  on:click={() => {
                    store.setAllocationKey(
                      key,
                      allocations[key] + budgetRemaining
                    );
                    // allocations[key] += budgetRemaining;
                  }}
                >
                  <text alignment-baseline="central" text-anchor="end">
                    Fill Up
                  </text>
                </g>
              {/if}
            </g>
          {/if}
        {/each}
        {#if doubleChecking}
          {#each Object.entries(minimums) as [key, minimum]}
            {#if minimum > 0}
              <g
                transform={`translate(${xScale(key)},
                ${innerHeight - yScale(minimum)})`}
              >
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
            <g
              transform={`translate(${xScale(key)}, ${yScale.range().at(-1)})`}
            >
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
          <line
            stroke="black"
            x1={0}
            y1={0}
            x2={0}
            y2={yScale.range().at(-1)}
          />
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
    </svg>
  </div>
  {#if state === "double-check-tutorial"}
    <div>
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div
        class="fixed left-0 right-0 top-0 bottom-0 bg-gray-100 opacity-50"
        on:click={() => {
          if (state === "double-check-tutorial") {
            state = "reading";
            doubleChecking = true;
          }
        }}
      />
      <div
        class="absolute bg-gray-100 border-2 rounded shadow-lg p-2 max-w-md"
        style={`left: calc(50% - 220px); top: 50%`}
      >
        {#if state === "double-check-tutorial"}
          Let's add a little bit of context and see how much each of these
          projects asked for! You are free to change your allocations if you
          wish.
        {/if}
      </div>
    </div>
  {/if}
  {#if budgetRemaining === 0 && !doubleChecking}
    <button
      class={buttonStyle}
      on:click={() => {
        // state = "allocating-tutorial";
        state = "double-check-tutorial";
      }}
    >
      I'm happy with this allocation amount
    </button>
  {/if}

  {#if budgetRemaining === 0 && doubleChecking}
    <Link to="/demographics" class={buttonStyle}>
      I'm now actually happy with my allocations
    </Link>
  {/if}
</div>
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
