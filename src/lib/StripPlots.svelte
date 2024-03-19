<script lang="ts">
  import { scaleBand, scaleLinear } from "d3-scale";
  import { format } from "d3-format";
  import { projects } from "./constants";
  import { store } from "../lib/store";
  type Table = Record<string, number | string>[];
  export let inputData: Record<string, number | string>[] = [];
  export let ward: string;
  export let color: string;

  $: allocations = $store.postCheckAllocations;
  $: allocationCategories = Object.entries(allocations).reduce(
    (acc, [key, val]) => {
      acc[projects[key].category] += val;
      return acc;
    },
    Object.fromEntries(
      Object.values(projects).map(({ category }) => [category, 0])
    )
  );
  $: allocationRows = Object.entries(allocationCategories).map(
    ([item, allocation]) => ({ ward: "49", item, allocation, mine: true })
  );

  $: data = (
    ward === "49" ? [...inputData, ...allocationRows] : inputData
  ) as Table;

  let height = 300;
  let width = 400;
  let margin = { left: 50, right: 50, top: 5, bottom: 33 };
  let innerHeight = height - margin.top - margin.bottom;
  let innerWidth = width - margin.left - margin.right;
  const yScaleFormatter = format("~s");
  const MILLION = 1000000;

  $: xDomain = Array.from(new Set(data.map((x) => x.item))).sort() as string[];
  $: yDomain = [0, Math.max(...data.map((x) => Number(x.allocation)))];
  $: xScale = scaleBand().domain(xDomain).range([0, innerWidth]);
  $: yScale = scaleLinear().domain(yDomain).range([0, innerHeight]);
</script>

<div class="mb-4">
  <h3 class="p-0 m-0">Ward {ward}</h3>
  <svg {height} {width}>
    <!-- marks -->
    <g transform={`translate(${margin.left}, ${margin.top})`}>
      {#each data as row}
        <g
          transform={`translate(${xScale(row.item)}, ${
            innerHeight - yScale(Number(row.allocation))
          })`}
        >
          <line
            y1={0}
            y2={0}
            x1={3}
            x2={xScale.bandwidth() - 3}
            stroke={row.mine ? "black" : color}
            stroke-width={row.mine ? 4 : 2}
          />
        </g>
      {/each}
    </g>
    <g transform={`translate(${margin.left}, ${margin.top})`}>
      <!-- x axis -->
      <line
        stroke="black"
        x1={-5}
        y1={yScale.range().at(-1)}
        x2={xScale.range().at(-1)}
        y2={yScale.range().at(-1)}
      />
      {#each xDomain as key}
        <g
          transform={`translate(${xScale(key)}, ${yScale.range().at(-1) - 20})`}
        >
          <g transform={`translate(30, ${xScale.bandwidth() / 2})`}>
            {#each key.split(" ") as word, idx}
              <text y={idx * 10} font-size="10" text-anchor="middle">
                {word}
              </text>
            {/each}
          </g>
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
  </svg>
  {#if ward === "49"}
    <span class="text-xs italic" style={`margin-left: ${margin.left}px`}>
      Large black bars show your allocations
    </span>
  {/if}
</div>
