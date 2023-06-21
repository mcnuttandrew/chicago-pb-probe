<script lang="ts">
  import { onMount } from "svelte";
  import { scaleLinear } from "d3-scale";
  import { interpolateYlOrRd, interpolateGnBu } from "d3-scale-chromatic";
  import Map from "../lib/Map.svelte";
  let features = [];
  let tableData: Record<string, any> = {};
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
        return [name, { popScale, partScale }];
      }
    )
  );
  const shortToLongName = { race: "Race", educ: "Education", income: "Income" };
  const tableCols = [
    { scale: "popScale", key: `Ward ${redSelect} Pop` },
    { scale: "partScale", key: `Ward ${redSelect} Part` },
    { scale: "popScale", key: `Ward ${blueSelect} Pop` },
    { scale: "partScale", key: `Ward ${blueSelect} Part` },
  ];
</script>

<div>
  <p>Voting has concluded for the 2022/2023 Participatory Budgeting cycle.</p>

  <p>
    Explore the projects that received the most votes and the allocations
    proposed by the residents.
  </p>

  <p>
    Here you can compare participation across Wards, relative to each Ward's
    demographics for the 2022/2023 Participatory Budgeting.
  </p>
</div>

<div class="flex flex-col">
  Pick two wards to compare
  <div class="flex">
    <div>
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
<div class="flex">
  <Map height={600} width={400} {features} {redSelect} {blueSelect} />
  <div class="flex flex-col items-center">
    {#each Object.entries(tableData) as [key, rows]}
      <div class="mt-6">
        <table>
          <col />
          <colgroup span="2" />
          <colgroup span="2" />
          <tr>
            <th rowspan="2">{shortToLongName[key]}</th>
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
          {#each rows as dataRow}
            <tr>
              <th style="width: 211px" scope="row" class="font-normal">
                {dataRow.category}
              </th>
              {#each tableCols as column}
                <td
                  class="mx-4 border-2 border-white text-center"
                  class:text-white={false}
                  style={`background: ${scales[key][column.scale](
                    dataRow[column.key]
                  )}`}
                >
                  {dataRow[column.key]}
                </td>
              {/each}
            </tr>
          {/each}
        </table>
      </div>
    {/each}
  </div>
</div>
