<script lang="ts">
  import { Router, Link, Route } from "svelte-routing";

  import About from "./pages/About.svelte";
  import Demographics from "./pages/Demographics.svelte";
  import Submit from "./pages/Submit.svelte";
  import Allocate from "./pages/Allocate.svelte";
  import Sort from "./pages/Sort.svelte";
  import Feedback from "./pages/Feedback.svelte";

  import TailwindCss from "./TailwindCSS.svelte";

  export let url = location.pathname;
</script>

<TailwindCss />

<main class="w-full h-full flex flex-col items-center">
  <Router {url}>
    <nav
      class="w-full bg-black text-white flex flex-row justify-between px-2 py-1"
    >
      <div>
        <Link to="/">About</Link>
        <Link to="/sort">Sort</Link>
        <Link to="/allocate">Allocate</Link>
        <Link to="/demographics">Demographics</Link>
        <Link to="/feedback">Feedback</Link>
        <Link to="/submit">Submit</Link>
      </div>
      <div>
        <p id="language">English | Español</p>
      </div>
    </nav>
    <div class="w-full flex flex-col px-32 py-8">
      <div>
        <h1 class="text-5xl font-bold">49th Ward Participatory Budgeting</h1>
        <h2 class="text-xl">2022 / 2023 cycle</h2>
      </div>
      <Route path="/" component={About} />
      <Route path="/demographics" component={Demographics} />
      <Route path="/feedback" component={Feedback} />
      <Route path="/sort" component={Sort} />
      <Route path="/allocate" component={Allocate} />
      <Route path="/submit" component={Submit} />
    </div>
  </Router>
</main>
