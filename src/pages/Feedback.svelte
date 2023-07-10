<script lang="ts">
  import { onMount } from "svelte";
  import { format } from "d3-format";
  import { scaleLinear } from "d3-scale";
  import { interpolateYlOrRd, interpolateGnBu } from "d3-scale-chromatic";
  import { store } from "../lib/store";
  import Map from "../lib/Map.svelte";
  import TableLegend from "../lib/TableLegend.svelte";
  let features = [];
  let tableData: Record<string, Record<string, number | string>[]> = {};

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
  });
  const wards = ["29", "35", "36", "49"];
  let blueSelect = "49";
  let redSelect = "29";
  const shortToLongName = { race: "Race", educ: "Education", income: "Income" };
  const demographicsOptions = Object.keys(shortToLongName);
  let demographicSelected = demographicsOptions[0];

  $: demos = $store.demographics;
  let demoToCat = {
    race: "How would you identify your race or ethnicity?",
    age: "What is your age?",
    income: "What is your estimated yearly household income?",
    educ: "What is your highest level of education?",
  };
  $: yourDemoValue = demos[demoToCat[demographicSelected]];

  const getDomain = (x: number[]) => [Math.min(...x), Math.max(...x)];

  $: scales = Object.fromEntries(
    Object.entries(tableData || {}).map(
      ([name, data]: [string, Record<string, number>[]]) => {
        const buildDomain = (str: string) =>
          [redSelect, blueSelect].flatMap((x) =>
            data.map((el) => el[`Ward ${x} ${str}`])
          );

        //   use a clipped range to make sure the text stays legible
        const popLin = scaleLinear()
          .domain(getDomain(buildDomain("Pop")))
          .range([0, 0.8]);
        const partLin = scaleLinear()
          .domain(getDomain(buildDomain("Part")))
          .range([0, 0.8]);
        const popScale = (v: number) => interpolateYlOrRd(popLin(v));
        const partScale = (v: number) => interpolateGnBu(partLin(v));
        return [name, { popScale, partScale, popLin, partLin }];
      }
    )
  );

  $: tableCols = [
    { scale: "popScale", key: `Ward ${redSelect} Pop`, format: (x) => x },
    {
      scale: "partScale",
      key: `Ward ${redSelect} Part`,
      format: (x) => `${x}%`,
    },
    { scale: "popScale", key: `Ward ${blueSelect} Pop`, format: (x) => x },
    {
      scale: "partScale",
      key: `Ward ${blueSelect} Part`,
      format: (x) => `${x}%`,
    },
  ];

  let mode: "demographics" | "strip" = "demographics";
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

<div class="flex flex-col items-center lg:flex-row">
  <Map height={600} width={400} {features} {redSelect} {blueSelect} />
  <div class="flex flex-col items-center">
    <div>
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
      {#if mode === "demographics"}
        <div class="flex">
          <div class="flex flex-col mr-2">
            Pick a demographic
            <select
              bind:value={demographicSelected}
              class="border-2 border-black"
            >
              {#each demographicsOptions as demo}
                <option value={demo}>{shortToLongName[demo]}</option>
              {/each}
            </select>
          </div>
          <div class="flex flex-col">
            Pick two wards to compare
            <div class="flex">
              <div class="mr-1">
                <select bind:value={redSelect} class="border-2 border-black">
                  {#each wards as ward}
                    <option value={ward}>Ward {ward}</option>
                  {/each}
                </select>
              </div>
              <div>
                <select bind:value={blueSelect} class="border-2 border-black">
                  {#each wards as ward}
                    <option value={ward}>Ward {ward}</option>
                  {/each}
                </select>
              </div>
            </div>
          </div>
        </div>
      {/if}
    </div>
    {#if mode === "demographics"}
      <!-- {#each Object.entries(tableData) as [key, rows]} -->
      <div class="mt-6 mb-28">
        <table>
          <col />
          <colgroup span="2" />
          <colgroup span="2" />
          <tr>
            <th rowspan="2">{shortToLongName[demographicSelected]}</th>
            <th
              colspan="2"
              scope="colgroup"
              class="mx-4 border-2 border-white"
              style="background: #7e62c4"
            >
              Ward {redSelect}
            </th>
            <th
              colspan="2"
              scope="colgroup"
              class="mx-4 border-2 border-white"
              style="background: #ed963c"
            >
              Ward {blueSelect}
            </th>
          </tr>
          <tr>
            <th class="px-4 py-1" scope="col">Population</th>
            <th class="px-4 py-1" scope="col">Participation</th>
            <th class="px-4 py-1" scope="col">Population</th>
            <th class="px-4 py-1" scope="col">Participation</th>
          </tr>
          {#each tableData[demographicSelected] || [] as dataRow}
            <tr
              class:border-black={dataRow.category === yourDemoValue}
              class:border-2={dataRow.category === yourDemoValue}
            >
              <th style="width: 211px" scope="row" class="font-normal">
                {dataRow.category}
              </th>
              {#each tableCols as column}
                <td
                  class="mx-4 text-center"
                  class:text-white={false}
                  style={`background: ${scales[demographicSelected][
                    column.scale
                  ](dataRow[column.key])}`}
                >
                  {column.format(dataRow[column.key])}
                </td>
              {/each}
            </tr>
          {/each}
        </table>
        <span class="text-xs pl-52 italic">
          Boxed line shows the demographic you selected on the previous page
        </span>
        <!-- legends -->
        <div class="pl-52">
          {#if scales[demographicSelected]?.popScale}
            <div class="flex flex-col w-1/3 p-0">
              <span class="font-bold text-xs w-64">Population (count)</span>
              <TableLegend
                numScale={scales[demographicSelected].popLin}
                colorScale={interpolateYlOrRd}
                format={(x) => format(".2s")(x)}
                height={30}
                width={300}
              />
            </div>
          {/if}
          {#if scales[demographicSelected]?.partScale}
            <div class="flex flex-col w-1/3 p-0">
              <span class="font-bold text-xs w-64">
                Participation (percentage)
              </span>
              <TableLegend
                numScale={scales[demographicSelected].partLin}
                colorScale={interpolateGnBu}
                format={(x) => `${x}%`}
                height={30}
                width={300}
              />
            </div>
          {/if}
        </div>
      </div>
    {/if}
    <!-- {/each} -->
  </div>
</div>
