<script lang="ts">
  import { onMount } from "svelte";

  import { csvParse } from "d3-dsv";

  import Map from "../lib/Map.svelte";
  import DemoTables from "../lib/Tables.svelte";
  import StripPlot from "../lib/StripPlots.svelte";

  let features = [];
  let tableData: Record<string, Record<string, number | string>[]> = {};
  let stripData: Record<string, number | string>[] = [];

  onMount(() => {
    fetch("./data/ward_boundaries.geojson")
      .then((x) => x.json())
      .then((x) => {
        features = x.features;
      });
    fetch("./data/table_data_updated.json")
      .then((x) => x.json())
      .then((x) => {
        tableData = x;
      });
    fetch("./data/allocation_simulation.csv")
      .then((x) => x.text())
      .then((x) => csvParse(x))
      .then((x) => {
        stripData = x;
      });
  });
  const wards = ["29", "35", "36", "49"];
  let blueSelect = "49";
  let redSelect = "29";

  let mode: "demographics" | "strip" = "strip";

  let lastWasRed = false;
  const allowedWards = new Set(wards);
  function selectWard(ward: string) {
    if (!allowedWards.has(ward)) {
      return;
    }
    if (lastWasRed) {
      blueSelect = ward;
      lastWasRed = false;
    } else {
      redSelect = ward;
      lastWasRed = true;
    }
  }
</script>

<div class="px-8">
  <!-- <p>Voting has concluded for the 2022/2023 Participatory Budgeting cycle.</p> -->
  <p>
    Thank you for participating! You can explore some of the context of these
    values below
  </p>

  <p>
    Explore the projects that received the most votes and the allocations
    proposed by the residents.
  </p>

  <p>
    Here you can compare participation across Wards, relative to each Ward's
    demographics for the 2022/2023 Participatory Budgeting.
  </p>
</div>

<div class="flex items-center justify-between px-8 mt-8 w-full max-w-4xl">
  <div class="flex flex-col">
    Pick a mode to view
    <div class="flex">
      <button
        on:click={() => {
          mode = "demographics";
        }}
        class={`border-black border-2 cursor-pointer py-2 px-1 rounded mr-2`}
        class:bg-black={mode === "demographics"}
        class:text-white={mode === "demographics"}
      >
        Demographics
      </button>
      <button
        on:click={() => {
          mode = "strip";
        }}
        class={`  border-black border-2 cursor-pointer py-2 px-1 rounded mr-2`}
        class:bg-black={mode === "strip"}
        class:text-white={mode === "strip"}
      >
        Responses
      </button>
    </div>
  </div>
  <div class="flex flex-col">
    Pick two wards to compare
    <div class="flex">
      <select
        bind:value={redSelect}
        class="border-2 border-black py-2 px-1 rounded mr-2"
      >
        {#each wards as ward}
          <option value={ward}>Ward {ward}</option>
        {/each}
      </select>
      <select
        bind:value={blueSelect}
        class="border-2 border-black py-2 px-1 rounded mr-2"
      >
        {#each wards as ward}
          <option value={ward}>Ward {ward}</option>
        {/each}
      </select>
    </div>
  </div>
</div>

{#if mode === "demographics"}
  <div
    class="flex flex-col items-center lg:flex-row lg:justify-between lg:items-start h-full w-full max-w-4xl"
  >
    <Map
      height={600}
      width={400}
      {features}
      {redSelect}
      {blueSelect}
      {selectWard}
    />
    <DemoTables {tableData} {redSelect} {blueSelect} />
  </div>
{/if}
{#if mode === "strip"}
  <div
    class="flex flex-col items-center md:flex-row md:justify-between lg:items-start h-full w-full max-w-4xl"
  >
    <Map
      height={600}
      width={400}
      {features}
      {redSelect}
      {blueSelect}
      {selectWard}
    />
    <div class="flex flex-col">
      <StripPlot
        color="#7e62c4"
        ward={redSelect}
        inputData={stripData.filter((x) => x.ward === redSelect)}
      />
      <StripPlot
        ward={blueSelect}
        inputData={stripData.filter((x) => x.ward === blueSelect)}
        color={"#ed963c"}
      />
    </div>
  </div>
{/if}
