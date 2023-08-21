<script lang="ts">
  import { Link } from "svelte-routing";
  import { buttonStyle } from "../lib/constants";
  import { store } from "../lib/store";

  let userId = "your Id";
  let submitId = false;
</script>

<div>
  <h3 class="text-lg">
    Welcome! You will be asked to 
    <!-- select four (4) projects and  -->
    decide how $1 million of the ward's 
    discretionary funds (a.k.a. "menu money")
    <!-- menu money -->
    should be allocated.
  </h3>

  <h3 class="text-lg text-sky-400">What happens after I vote?</h3>

  <p class="my-2">
    The Ward Alderperson
    <!-- Alderman Villegas  -->
    will submit the projects that win the most votes, up to $1
    million, to the City of Chicago for implementation. All the projects listed
    are feasible to the best of our knowledge, yet require final approval from
    the City of Chicago or its sister agencies.
  </p>

  <p class="my-2">
    While 
    the Alderperson
    <!-- Alderman Villegas  -->
    pledges to request funding and advocate for the
    winning projects, they cannot guarantee that the government agencies will
    grant final approval to each project request. If a winning project cannot be
    implemented for any reason, 
    the Alderperson
    <!-- Alderman Villegas  -->
    will use the allocated money to fund the next runner-up project that falls 
    within the budget.
  </p>

  <h3 class="text-lg text-sky-400">Before proceeding, please input your User Id for the study.</h3>

  <p class="italic">This will be provided by the interviewer.</p>

  <input bind:value={userId} style="padding: initial; border: 2px solid gray; border-radius: 4px;" size="10"/>
  <br>
  <button
    class="bg-white hover:bg-gray-100 border-2 border-gray-700 rounded px-4 py-0.4" 
    style="margin-top: 5px"
    on:click={() => {
      store.setUserId(userId);
      submitId = true;
    }}>
    Confirm
  </button>
  {#if submitId}
    <p>Thanks! We've logged your User Id as <b style="color:blue">{userId}</b>.</p>
  {/if}

  <div class="w-full flex items-center justify-center">
    <Link to="/sort">
      <div class={buttonStyle}>I'm ready to start</div>
    </Link>
  </div>
</div>
