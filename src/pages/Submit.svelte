<script lang="ts">
  import { Link } from "svelte-routing";
  import { buttonStyle } from "../lib/constants";
</script>

<div class="flex flex-col">
  <h1>
    Thank you for your inputs! We have logged them and will analyze them shortly
  </h1>
  <div>To better understand the context of some of our results please see</div>
  <Link
    class={`${buttonStyle} flex items-center justify-center`}
    to="/feedback"
  >
    this explorer
  </Link>
  <div>to learn more</div>
</div>
