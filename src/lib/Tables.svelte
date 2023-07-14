<script lang="ts">
  import TableLegend from "../lib/TableLegend.svelte";
  import { scaleLinear } from "d3-scale";
  import { interpolateYlOrRd, interpolateGnBu } from "d3-scale-chromatic";
  import { format } from "d3-format";
  import { store } from "../lib/store";
  export let redSelect: string;
  export let blueSelect: string;
  export let tableData: Record<string, Record<string, number | string>[]>;

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

  const numFormat = format(",.6");
  const percentFormat = (x) => `${x}%`;
  const countFormat = (x) => numFormat(x);
  $: tableCols = [
    { scale: "popScale", key: `Ward ${redSelect} Pop`, format: countFormat },
    {
      scale: "partScale",
      key: `Ward ${redSelect} Part`,
      format: percentFormat,
    },
    { scale: "popScale", key: `Ward ${blueSelect} Pop`, format: countFormat },
    {
      scale: "partScale",
      key: `Ward ${blueSelect} Part`,
      format: percentFormat,
    },
  ];
</script>

<div class="flex flex-col">
  <div class="flex flex-col mr-2">
    Pick a demographic
    <select bind:value={demographicSelected} class="border-2 border-black">
      {#each demographicsOptions as demo}
        <option value={demo}>{shortToLongName[demo]}</option>
      {/each}
    </select>
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
              style={`background: ${scales[demographicSelected][column.scale](
                dataRow[column.key]
              )}`}
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
          <span class="font-bold text-xs w-64">Participation (percentage)</span>
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
</div>
