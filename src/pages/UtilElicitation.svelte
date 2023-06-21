<script lang="ts">
  import { Link } from "svelte-routing";
  import { scaleLinear, scaleBand } from "d3-scale";
  import { format } from "d3-format";

  const explanations = {
    "Street Resurfacing":
      "Street resurfacing is determined by a percentage of the budget. 100% of the budget allows for 16 streets to be resurfaced, while 50% covers resurfacing for 9 streets.",
    "Bike Lanes":
      "The bike lanes would run with traffic on Maplewood from Montrose to Wilson; with traffic on Campbell from Wilson to Montrose. They would connect with the future Leland Greenway on Campbell. The bike lanes would not impact parking.",
    "School Improvements":
      "A nature play space at Bateman would be a dream come true for the school, parents, and students. Bateman’s community is working collaboratively to design natural play and learning areas for the children. These funds would help make this proposal feasible and allow them to give their students a new and educational play area.",
    "Picnic Tables":
      "This proposal includes new pool tables with umbrellas as well as picnic tables outside of the California Park pool area, and ADA accessible picnic tables near the softball field to create pleasant gathering spots for all.",
    "Street Lights":
      "This project focuses on improving safety at W. Belmont Ave and N. Narragansett Ave. Turn signals and refreshed crosswalks would dramatically improve the busy intersection!",
    "Food Pantry":
      "During the pandemic, neighbors came together to create a food pantry out of a plastic shed at the Drake Garden. This proposal is would fund the creation of permanent structure which will hold food pantry items, serve as a shed for neighbors and volunteers to store tools & supplies, and a fold-out stand to hold small event sales.",
    "Street Murals":
      "In partnership with the Green Star Movement, this mural would go along the South-west side of the school by the main entrance on Lincoln Avenue.",
    "Curb Cuts":
      "Install curb cuts and crosswalk at 7557 N. Paulina to allow people with strollers or mobility impairments to access the north end of the train station.",
  };
  let allocations = Object.fromEntries(
    Object.keys(explanations).map((x) => [x, 0])
  ) as Record<keyof typeof explanations, number>;
  const MILLION = 1000000;
  const height = 600;
  const width = 1000;
  const margin = { left: 50, right: 50, top: 50, bottom: 50 };
  const innerHeight = height - margin.top - margin.bottom;
  const innerWidth = width - margin.left - margin.right;
  const xScale = scaleBand()
    .domain(Object.keys(explanations))
    .range([0, innerWidth])
    .padding(0.1);
  const yScale = scaleLinear().domain([0, MILLION]).range([0, innerHeight]);
  const yScaleFormatter = format("~s");

  let state: "tutorial" | "dragging" | "allocating-reading" = "tutorial";
  let target: keyof typeof explanations | null = null;
  let openTooltip: { x: number; y: number; key: string } | null = null;

  $: totalAllocation = Object.values(allocations).reduce(
    (acc, x) => acc + x,
    0
  );
  $: budgetRemaining = MILLION - totalAllocation;

  const clamp = (x, lb, ub) => Math.max(Math.min(x, ub), lb);
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
    <div>
      <h1 class="text-lg">You have {budgetRemaining}$ remaining</h1>
      <h1 class="text-lg">
        {#if budgetRemaining < 0}
          You can not allocate more than $1 million total
        {/if}
      </h1>
    </div>
    <svg {width} {height}>
      <g transform={`translate(${margin.left}, ${margin.top})`}>
        {#each Object.entries(allocations) as [key, value]}
          <rect
            class="stroke-1"
            x={xScale(key)}
            y={innerHeight - yScale(value) - (allocations[key] ? 0 : 1)}
            fill="steelblue"
            stroke={key === target ? "black" : "white"}
            height={clamp(
              yScale(value) + (allocations[key] ? 0 : 5),
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
                innerHeight - yScale(value) - 20
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
          {#each Object.entries(explanations) as [key, explanation]}
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
  {#if openTooltip}
    <div>
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
  {#if state === "tutorial"}
    <div>
      <div
        class="fixed left-0 right-0 top-0 bottom-0 bg-gray-100 opacity-50"
        on:click={() => {
          state = "allocating-reading";
        }}
      />
      <div
        class="absolute bg-gray-100 border-2 rounded shadow-lg p-2 max-w-md"
        style={`left: calc(50% - 220px); top: 50%`}
      >
        Drag project labels to rank your preferences from most important on the
        left to least important on the right.
      </div>
    </div>
  {/if}
  {#if budgetRemaining === 0}
    <Link to="/demographics">Next</Link>
  {/if}
</div>

<style>
</style>
