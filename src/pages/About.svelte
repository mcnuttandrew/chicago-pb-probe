<script lang="ts">
  import { Link } from "svelte-routing";
  import { buttonStyle } from "../lib/constants";
</script>

<div>
  <h3 class="text-lg">
    Welcome! You will be asked to select four (4) projects and decide how $1
    million of the ward's menu money should be allocated.
  </h3>

  <h3 class="text-lg text-blue-400">What happens after I vote?</h3>

  <p class="my-2">
    Alderman Villegas will submit the projects that win the most votes, up to $1
    million, to the City of Chicago for implementation. All the projects listed
    are feasible to the best of our knowledge, yet require final approval from
    the City of Chicago or its sister agencies.
  </p>

  <p class="my-2">
    While Alderman Villegas pledges to request funding and advocate for the
    winning projects, he cannot guarantee that the government agencies will
    grant final approval to each project request. If a winning project cannot be
    implemented for any reason, Alderman Villegas will use the allocated money
    to fund the next runner-up project that falls within the project.
  </p>

  <h2 id="voting">Voting Period: October 20 - November 30, 2022</h2>

  <div class="w-full flex items-center justify-center">
    <Link to="/sort">
      <div class={buttonStyle}>I'm ready to allocate</div>
    </Link>
  </div>
</div>
