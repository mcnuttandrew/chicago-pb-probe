<script lang="ts">
  import { Link } from "svelte-routing";
  import { scaleBand, scaleLinear } from "d3-scale";
  import { explanations, buttonStyle } from "../lib/constants";
  import { format } from "d3-format";

  // import SortableList from "../lib/SortableList.svelte";

  import SortableList from "svelte-sortable-list";

  let sortOrder = Object.keys(explanations);
  $: allocations = Object.fromEntries(sortOrder.map((x) => [x, 0])) as Record<
    keyof typeof explanations,
    number
  >;
  const MILLION = 1000000;
  const height = 600;
  const width = 1000;
  const margin = { left: 50, right: 50, top: 50, bottom: 50 };
  const innerHeight = height - margin.top - margin.bottom;
  const innerWidth = width - margin.left - margin.right;
  $: xScale = scaleBand().domain(sortOrder).range([0, innerWidth]).padding(0.1);
  const yScale = scaleLinear().domain([0, MILLION]).range([0, innerHeight]);
  const yScaleFormatter = format("~s");

  type State =
    | "sorting-tutorial"
    | "sorting"
    | "allocating-tutorial"
    | "allocating-dragging"
    | "allocating-reading"
    | "double-check-tutorial"
    | "double-check-reading"
    | "double-check-dragging";
  let state: State = "sorting-tutorial";

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
  <h3 class="text-blue-400 font-bold">
    How were the project proposals selected?
  </h3>
  <p class="my-2">
    All listed projects were suggested and vetted by 49th Ward residents. From
    August to September 2022, community representatives met regularly in
    committees to determine which project proposals to place on this year’s
    ballot.
  </p>
  <p class="my-2 italic">
    Participation in the 49th Ward participatory budgeting process as a
    community representative and/or as an attendee at a neighborhood assembly
    was entirely voluntary and open to all 49th Ward residents, regardless of
    citizenship or voter registration.
  </p>
  <div class="my-8">
    {#if state === "allocating-dragging" || state === "allocating-reading" || state === "allocating-tutorial"}
      <div>
        <h1 class="text-lg">
          You have {format(",.2r")(budgetRemaining)}$ remaining
        </h1>
        <h1 class="text-lg">
          {#if budgetRemaining < 0}
            You can not allocate more than $1 million total
          {/if}
        </h1>
      </div>
    {/if}

    <!-- sort stage -->
    {#if state === "sorting" || state === "sorting-tutorial"}
      <SortableList
        list={sortOrder.map((name, id) => ({ name, id }))}
        let:item
        key="name"
        on:sort={(ev) => {
          sortOrder = ev.detail.map((x) => x.name);
        }}
      >
        <div class="border-2 border-gray-500 px-3 rounded flex flex-col">
          <span class="bolder italic">
            {#if item.id === 0}Most Important:
            {/if}{#if item.id === sortOrder.length - 1}Least Important:
            {/if}{item.name}
          </span>
          <span class="text-sm">{explanations[item.name]}</span>
        </div>
      </SortableList>
    {/if}

    <!-- allocate stage -->
    {#if state === "allocating-dragging" || state === "allocating-reading" || state === "allocating-tutorial"}
      <svg {width} {height}>
        <g transform={`translate(${margin.left}, ${margin.top})`}>
          {#each sortOrder as key}
            <rect
              class="stroke-1"
              x={xScale(key)}
              y={innerHeight -
                yScale(allocations[key]) -
                (allocations[key] ? 0 : 1)}
              fill="steelblue"
              stroke={key === target ? "black" : "white"}
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
                state = "allocating-dragging";
              }}
              on:mousemove={(e) => {
                if (state === "allocating-dragging") {
                  // @ts-ignore
                  const bbox = e.target.getBoundingClientRect();
                  const yVal = e.y - bbox.y;
                  allocations[key] = yScale.invert(innerHeight - yVal);
                }
              }}
              on:mouseup={() => {
                state = "allocating-reading";
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
                    transform={`translate(${xScale.bandwidth() / 3})`}
                    class="cursor-pointer"
                    on:click={() => {
                      allocations[key] = 0;
                    }}
                  >
                    <text
                      alignment-baseline="central"
                      text-anchor="middle"
                      font-size="10"
                    >
                      Clear
                    </text>
                  </g>
                {/if}

                <!-- svelte-ignore a11y-click-events-have-key-events -->
                {#if budgetRemaining > 0}
                  <g
                    transform={`translate(${(xScale.bandwidth() * 2) / 3})`}
                    class="cursor-pointer"
                    font-size="10"
                    on:click={() => {
                      allocations[key] += budgetRemaining;
                    }}
                  >
                    <text alignment-baseline="central" text-anchor="middle">
                      Fill Up
                    </text>
                  </g>
                {/if}
              </g>
            {/if}
          {/each}
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
                transform={`translate(${xScale(key)}, ${yScale
                  .range()
                  .at(-1)})`}
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
    {/if}
  </div>
  {#if state === "allocating-tutorial" || state === "sorting-tutorial" || state === "double-check-tutorial"}
    <div>
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <div
        class="fixed left-0 right-0 top-0 bottom-0 bg-gray-100 opacity-50"
        on:click={() => {
          if (state === "allocating-tutorial") {
            state = "allocating-reading";
          }
          if (state === "sorting-tutorial") {
            state = "sorting";
          }
        }}
      />
      <div
        class="absolute bg-gray-100 border-2 rounded shadow-lg p-2 max-w-md"
        style={`left: calc(50% - 220px); top: 50%`}
      >
        {#if state === "allocating-tutorial"}
          Now let's allocate funds. Draw bars to distribute money among your top
          4 preferred projects.
        {/if}
        {#if state === "sorting-tutorial"}
          Drag project labels to rank your preferences from most important on
          the left to least important on the right.
        {/if}
        {#if state === "double-check-tutorial"}
          Let's add a little bit of context and see how much each of these
          projects asked for! You are free to change your allocations if you
          wish.
        {/if}
      </div>
    </div>
  {/if}
  {#if budgetRemaining === 0}
    <button
      class={buttonStyle}
      on:click={() => {
        // state = "allocating-tutorial";
        state = "double-check-tutorial";
      }}
    >
      Im happy with this allocation amount
    </button>
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

{#if state === "sorting"}
  <button
    class={buttonStyle}
    on:click={() => {
      state = "allocating-tutorial";
    }}
  >
    Im happy with this sort order
  </button>
{/if}
