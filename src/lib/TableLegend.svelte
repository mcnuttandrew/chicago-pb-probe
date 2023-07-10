<script lang="ts">
  import { scaleLinear } from "d3-scale";
  import type { ScaleLinear } from "d3-scale";
  export let format: (x: number) => string;
  export let width: number = 700;
  export let height: number = 50;
  export let colorScale: any;
  export let numSteps: number = 5;
  export let numScale: ScaleLinear<number, number, never>;
  //   const steps = [0, 0.25, 0.5, 0.75, 1];
  $: steps = [...new Array(numSteps + 1)].map((_, idx) => idx / numSteps);
  const xScale = scaleLinear().domain([0, 1]).range([0, width]);
  $: stepSize = xScale(steps[1]) - xScale(steps[0]);

  $: localScale = scaleLinear()
    .domain([0, 1])
    .range([...numScale.domain()])
    .nice();
</script>

<svg {width} {height} overflow="visible">
  {#each steps.slice(0, steps.length - 1) as step}
    <rect
      x={xScale(step)}
      y={0}
      height={20}
      width={stepSize}
      fill={colorScale(step)}
    />
  {/each}
  {#each steps as step}
    <text
      x={xScale(step) - 10}
      y={height}
      fill="black"
      font-size={12}
      text-anchor="center"
    >
      {format(localScale(step))}
    </text>
  {/each}
</svg>
