<script lang="ts">
  // derived form https://github.com/isaacHagoel/svelte-dnd-action
  import { flip } from "svelte/animate";
  import { dndzone } from "svelte-dnd-action";
  import ElicitHeader from "../lib/ElicitHeader.svelte";
  import { projects, buttonStyle } from "../lib/constants";
  import { store } from "../lib/store";
  $: sortOrder = $store.sortOrder;
  $: showNext = sortOrder.length === Object.keys(projects).length;

  const flipDurationMs = 200;
  const keyNames = Object.fromEntries(
    Object.keys(projects).map((x, idx) => [x, idx + 1])
  );
  $: unsorted = Object.keys(projects).filter(
    (x) => !sortOrder.find((y) => x === y)
  );

  $: board = [
    { name: "unsorted", items: unsorted },
    { name: "sorted", items: sortOrder },
  ].map((x, id) => ({
    ...x,
    id,
    items: x.items.map((name) => ({ name, id: keyNames[name] })),
  }));

  function handleDndConsiderCards(cid, e) {
    const colIdx = board.findIndex((c) => c.id === cid);
    board[colIdx].items = e.detail.items;
    board = [...board];
  }
  function handleDndFinalizeCards(cid, e) {
    const colIdx = board.findIndex((c) => c.id === cid);
    board[colIdx].items = e.detail.items;
    board = [...board];
    store.setSort([...board[1].items.map((x) => x.name)]);
  }
  function handleRemove(name) {
    store.setSort(sortOrder.filter((x) => x !== name));
  }
  function handleAdd(name) {
    store.setSort([...sortOrder, name]);
  }
</script>

<div>
  <ElicitHeader />
  <section class="w-full flex h-full mt-8">
    {#each board as column (column.id)}
      <div
        class="h-full w-1/2 mx-2 px-4"
        animate:flip={{ duration: flipDurationMs }}
      >
        <div
          class="mb-4 flex flex-col justify-center content-center text-center"
        >
          {#if column.name === "unsorted"}
            <div class="text-2xl font-bold text-center">Unsorted</div>
            {#if showNext}
              <!-- hard linked (rather than using soft Links bc of animation sync bugs that cause faulty renders) -->
              <a href="/allocate" class={buttonStyle}>
                I'm happy with this sort order
              </a>
            {:else}
              <div class="italic">
                Drag projects from this list into the one on the right. You
                must order all projects to move on.
              </div>
            {/if}
          {:else}
            <div class="text-2xl font-bold text-center">Sorted</div>
            <div class="italic">
              Higher in the list means more important. Drag projects to order
              them in terms of importance.
            </div>
          {/if}
        </div>
        <div
          class="h-full"
          use:dndzone={{
            items: column.items,
            flipDurationMs,
            dropTargetClasses: [
              "border-black",
              "border-2",
              "outline-black",
              "border-dashed",
              "rounded",
            ],
            dropTargetStyle: { outline: "rgba(255, 255, 102, 0.7) solid 0px" },
          }}
          on:consider={(e) => handleDndConsiderCards(column.id, e)}
          on:finalize={(e) => handleDndFinalizeCards(column.id, e)}
        >
          {#if column.items.length === 0}
            <div class=" pointer-events-none mt-36 italic" style="background-color: lightgrey; padding: 1em">
              {#if column.name === "unsorted"}
                You've finished adding projects! Drag them to rearrange your
                preferences.
              {:else}
                Drag boxes from the list on the left into this one to specify
                how important they are to you
              {/if}
            </div>
          {/if}
          {#each column.items as item (item.id)}
            <!-- svelte-ignore a11y-click-events-have-key-events -->
            <div
              class="py-2 px-1 w-full mx-2 my-0 flex flex-col justify-center content-center border-2 border-gray-500 px-3 rounded bg-slate-100 my-1"
              animate:flip={{ duration: flipDurationMs }}
            >
              <span class="font-bold text-center">
                {#if column.name === "sorted"}
                  <!-- {#if sortOrder.findIndex((x) => x === item.name) === 0}
                    Most important:
                  {/if}
                  {#if sortOrder.findIndex((x) => x === item.name) === sortOrder.length - 1}
                    Least important:
                  {/if} -->
                  {#if sortOrder.findIndex((x) => x === item.name) !== -1}
                    {`${sortOrder.findIndex((x) => x === item.name) + 1}. `}
                  {/if}
                  <div
                    class="float-right"
                    on:click={() => handleRemove(item.name)}
                  >
                    X
                  </div>
                {:else}
                  <div
                    class="float-right font-light text-xs italic"
                    on:click={() => handleAdd(item.name)}
                  >
                    add
                  </div>
                {/if}
                {item.name}
              </span>
              <span class="text-sm">
                {projects[item.name].description}
              </span>
            </div>
          {/each}
        </div>
      </div>
    {/each}
  </section>
</div>
