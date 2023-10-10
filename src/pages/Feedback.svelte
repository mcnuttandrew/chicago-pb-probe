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
    // fetch("./data/table_data_updated.json")
    fetch("./data/demo_table_data.json")
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

  let mode: "demographics" | "strip" = "demographics";

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
  <h3 class="text-lg text-400 font-bold">Thank you for participating!</h3>
  <p class="italic">
    This page provides information for you to explore about who has voted so far in each ward.
    You can also see people's preferred allocations in participating wards.
  </p>

  <p>Click the buttons below to start exploring!</p>
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
        Allocations
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
        <option value={null}>(no selection)</option>
        {#each wards as ward}
          <option value={ward}>Ward {ward}</option>
        {/each}
      </select>
      <select
        bind:value={blueSelect}
        class="border-2 border-black py-2 px-1 rounded mr-2"
      >
        <option value={null}>(no selection)</option>
        {#each wards as ward}
          <option value={ward}>Ward {ward}</option>
        {/each}
      </select>
    </div>
  </div>
</div>

{#if mode === "demographics"}
  <div class="px-8" style="padding: 20px 0px;">
    <p>
      Here you can compare participation across Wards, relative to each Ward's overall
      demographics during the 2022/2023 Participatory Budgeting cycle.
    </p>
  </div>
  <div
    class="flex flex-col items-center lg:flex-row lg:justify-between lg:items-start h-full w-full max-w-4xl"
  >
    <Map
      height={500}
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
<div class="px-8" style="padding: 20px 0px;">
  <p>
    Here you can explore the kinds of projects that received the most votes in each ward and the allocations
    proposed by residents.
  </p>
</div>
  <div
    class="flex flex-col items-center md:flex-row md:justify-between lg:items-start h-full w-full max-w-4xl"
  >
    <Map
      height={500}
      width={400}
      {features}
      {redSelect}
      {blueSelect}
      {selectWard}
    />
    <div class="flex flex-row">
      {#if redSelect}
        <div class="flex-col">
          <StripPlot
            color="#7e62c4"
            ward={redSelect}
            inputData={stripData.filter((x) => x.ward === redSelect)}
          />
        </div>
      {/if}
      {#if blueSelect}
        <div class="flex-col">
          <StripPlot
            ward={blueSelect}
            inputData={stripData.filter((x) => x.ward === blueSelect)}
            color={"#ed963c"}
          />
        </div>
      {/if}
    </div>
  </div>
{/if}
