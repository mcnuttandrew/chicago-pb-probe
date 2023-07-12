<script lang="ts">
  import { geoMercator, geoPath } from "d3-geo";
  export let features: any[] = [];
  export let height: number;
  export let width: number;
  export let redSelect: string;
  export let blueSelect: string;
  export let selectWard: (ward: string) => void;
  let projection = geoMercator()
    .center([-87.723177, 41.778832])
    .translate([width / 2, height * 0.7])
    .scale(50000);
  let path = geoPath().projection(projection);
  let hovered: false | string = false;

  const wards = ["29", "35", "36", "49"];
  const allowedWard = new Set(wards);

  $: evalColorForWard = (ward: string) => {
    if (ward === redSelect) {
      return "#7e62c4";
    }
    if (ward === blueSelect) {
      return "#ed963c";
    }
    if (allowedWard.has(ward)) {
      return "cadetblue";
    }
    return "white";
  };
  $: hoveredFeature = features.find((x) => x.properties.ward === hovered);
  $: hoveredCentroid = hovered ? path.centroid(hoveredFeature) : false;
</script>

<div class="flex flex-col items-center">
  <svg {height} {width} class="overflow-visible">
    {#each features as feature}
      <!-- svelte-ignore a11y-click-events-have-key-events -->
      <path
        on:click={() => selectWard(feature.properties.ward)}
        d={path(feature)}
        class="cursor-pointer"
        fill={evalColorForWard(feature.properties.ward)}
        stroke="dimgray"
        fill-opacity={hovered === feature.properties.ward ? 0.6 : 1}
        id={feature.properties.ward}
        on:mouseenter={() => {
          hovered = feature.properties.ward;
        }}
      />
    {/each}
    {#if hovered}
      <text
        class="pointer-events-none"
        x={hoveredCentroid[0]}
        y={hoveredCentroid[1]}
        text-anchor="middle"
        alignment-baseline="central"
      >
        {hovered}
      </text>
    {/if}
  </svg>
  <span class="text-sm italic">Selectable wards are shaded</span>
</div>
