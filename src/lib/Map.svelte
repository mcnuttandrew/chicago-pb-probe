<script lang="ts">
  import { geoMercator, geoPath } from "d3-geo";
  export let features: any[] = [];
  export let height: number;
  export let width: number;
  export let redSelect: string;
  export let blueSelect: string;
  let projection = geoMercator()
    .center([-87.723177, 41.778832])
    .translate([width / 2, height * 0.7])
    .scale(50000);
  let path = geoPath().projection(projection);

  const evalColorForWard = (ward: string) => {
    if (ward === redSelect) {
      return "#7e62c4";
    }
    if (ward === blueSelect) {
      return "#ed963c";
    }
    return "white";
  };
</script>

<svg {height} {width} class="overflow-visible">
  {#each features as feature}
    <path
      d={path(feature)}
      fill={evalColorForWard(feature.properties.ward)}
      stroke="dimgray"
      id={feature.properties.ward}
    />
  {/each}
</svg>
