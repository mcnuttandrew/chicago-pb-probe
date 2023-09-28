<script lang="ts">
  import TableLegend from "../lib/TableLegend.svelte";
  import { scaleLinear } from "d3-scale";
  // import { interpolateYlOrRd, interpolateGnBu } from "d3-scale-chromatic";
  import { interpolateGreys } from "d3-scale-chromatic";
  import { format } from "d3-format";
  import { store } from "../lib/store";
  export let redSelect: string;
  export let blueSelect: string;
  export let tableData: Record<string, Record<string, number | string>[]>;

  const shortToLongName = { race: "Race", educ: "Education", income: "Income" };
  const demographicsOptions = Object.keys(shortToLongName);
  let demographicSelected = demographicsOptions[0];
  
  let mode: "count" | "percent" = "percent";

  $: demos = $store.demographics;
  let demoToCat = {
    race: "How would you identify your race or ethnicity?",
    age: "What is your age?",
    income: "What is your estimated yearly household income?",
    educ: "What is your highest level of education?",
  };
  $: yourDemoValue = demos[demoToCat[demographicSelected]];
  const getDomain = (x: number[]) => [0, Math.max(...x)];

  $: scales = Object.fromEntries(
    Object.entries(tableData || {}).map(
      ([name, data]: [string, Record<string, number>[]]) => {
        const buildDomain = (str: string) =>
          data.flatMap((row) =>
            Object.entries(row)
              .filter(([key]) => key.endsWith(str))
              .map(([key, value]) => value)
          );

        //   use a clipped range to make sure the text stays legible
        const countLin = scaleLinear()
          .domain(getDomain(buildDomain("Count")))
          .range([0, 0.8]);
        const percLin = scaleLinear()
          .domain(getDomain(buildDomain("Perc")))
          .range([0, 0.8]);
        const countScale = (v: number) => interpolateGreys(countLin(v));
        const percScale = (v: number) => interpolateGreys(percLin(v));
        return [name, { countScale, percScale, countLin, percLin }];
      }
    )
  );

  const numFormat = format(",.6");
  const percentFormat = (x) => `${Math.round(x * 1000) / 10}%`;
  const countFormat = (x) => numFormat(x);
  const countTextWhite = (x) => scales[demographicSelected].countLin(x) > 0.6;
  const percTextWhite = (x) => scales[demographicSelected].percLin(x) > 0.6;
  $: tableCols = (mode == "count") ? [
    { 
      scale: "countScale", 
      key: `Ward ${redSelect} Pop Count`, 
      format: countFormat,
      textWhite: countTextWhite
    },
    {
      scale: "countScale",
      key: `Ward ${redSelect} Part Count`,
      format: countFormat,
      textWhite: countTextWhite
    },
    { 
      scale: "countScale", 
      key: `Ward ${blueSelect} Pop Count`, 
      format: countFormat,
      textWhite: countTextWhite 
    },
    {
      scale: "countScale",
      key: `Ward ${blueSelect} Part Count`,
      format: countFormat,
      textWhite: countTextWhite
    },
  ] : 
  [
    { 
      scale: "percScale", 
      key: `Ward ${redSelect} Pop Perc`, 
      format: percentFormat,
      textWhite: percTextWhite 
    },
    {
      scale: "percScale",
      key: `Ward ${redSelect} Part Perc`,
      format: percentFormat,
      textWhite: percTextWhite 
    },
    { 
      scale: "percScale", 
      key: `Ward ${blueSelect} Pop Perc`, 
      format: percentFormat,
      textWhite: percTextWhite  
    },
    {
      scale: "percScale",
      key: `Ward ${blueSelect} Part Perc`,
      format: percentFormat,
      textWhite: percTextWhite 
    },
  ];
</script>

<div class="flex flex-col">
  <div class="flex flex-row">
    <div class="flex-none w-50 mr-2" style="padding-top: 10px;">
      Pick a demographic
      <select bind:value={demographicSelected} class="border-2 border-black">
        {#each demographicsOptions as demo}
          <option value={demo}>{shortToLongName[demo]}</option>
        {/each}
      </select>
    </div>
    <div class="flex-none w-80 mr-2">
      Pick a metric
      <button
        on:click={() => {
          mode = "count";
        }}
        class={`border-black border-2 cursor-pointer py-2 px-1 rounded mr-2`}
        class:bg-black={mode === "count"}
        class:text-white={mode === "count"}
      >
        Counts
      </button>
      <button
        on:click={() => {
          mode = "percent";
        }}
        class={`  border-black border-2 cursor-pointer py-2 px-1 rounded mr-2`}
        class:bg-black={mode === "percent"}
        class:text-white={mode === "percent"}
      >
        Percents
      </button>
    </div>
  </div>
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
          {#if redSelect}
            Ward {redSelect}
          {:else}
            No Ward Selected
          {/if}
        </th>
        <th
          colspan="2"
          scope="colgroup"
          class="mx-4 border-2 border-white"
          style="background: #ed963c"
        >
        {#if blueSelect}
          Ward {blueSelect}
        {:else}
          No Ward Selected
        {/if}
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
          <th style="text-wrap: nowrap;" scope="row" class="font-normal">
            {dataRow.category}
          </th>
          {#each tableCols as column}
            <td
              class="mx-4 text-center"
              class:text-white={column.textWhite(dataRow[column.key])}
              style={`background: ${scales[demographicSelected][column.scale](dataRow[column.key])}`}
            >
              {column.format(dataRow[column.key])}
            </td>
          {/each}
        </tr>
      {/each}
    </table>
    <span class="text-xs italic">
      Boxed line shows the demographic you selected on the previous page
    </span>
    <!-- legends -->
    <div class="pl-52">
      {#if scales[demographicSelected]?.countScale && mode == "count"}
        <div class="flex flex-col w-1/3 p-0">
          <span class="font-bold text-xs w-64">Count (number of people)</span>
          <TableLegend
            numScale={scales[demographicSelected].countLin}
            colorScale={interpolateGreys}
            format={(x) => format(".2s")(x)}
            height={30}
            width={300}
          />
        </div>
      {/if}
      {#if scales[demographicSelected]?.percScale && mode == "percent"}
        <div class="flex flex-col w-1/3 p-0">
          <span class="font-bold text-xs w-64">Percentage (compared to numbers of residents and voters)</span>
          <TableLegend
            numScale={scales[demographicSelected].percLin}
            colorScale={interpolateGreys}
            format={percentFormat}
            height={30}
            width={300}
          />
        </div>
      {/if}
    </div>
  </div>
</div>
