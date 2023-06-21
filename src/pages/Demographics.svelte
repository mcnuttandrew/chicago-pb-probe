<script lang="ts">
  import { Link } from "svelte-routing";

  const questions = [
    {
      question: "What is your age?",
      options: [
        "14 to 17 years old",
        "18 to 24 years old",
        "25 to 34 years old",
        "35 to 44 years old",
        "45 to 54 years old",
        "55 to 64 years old",
        "65 years or older",
        "I prefer not to say",
      ],
    },
    {
      question: "How would you identify your race or ethnicity?",
      options: [
        "American Indian/ Alaskan Native",
        "Asian",
        "Black or African American",
        "Hispanic or Latino/a",
        "White",
        "I prefer not to say",
        "Other",
      ],
    },
    {
      question: "What is your estimated yearly household income?",
      options: [
        "Less than $10,000",
        "$10,000 to $14,999",
        "$15,000 to $24,999",
        "$25,000 to $34,999",
        "$35,000 to $49,999",
        "$50,000 to $79,999",
        "$80,000 to $99,999",
        "$100,000 to $149,999",
        "$150,000 or more",
        "I prefer not to say",
      ],
    },
  ];

  let answers = Object.fromEntries(questions.map((x) => [x.question, ""]));
  let otherValue = "Other";
  $: allAnswered = Object.values(answers).every((x) => x);
</script>

<div class="flex flex-col">
  <p>Next we have a handful of demographics questions for you to answer.</p>
  {#each questions as { question, options }, idx}
    <div class="flex flex-col my-4">
      <div><b>{question}</b></div>
      <div class="flex flex-wrap">
        {#each options as option}
          {#if option === "Other"}
            <label class="mr-5">
              <div class="flex">
                <input
                  type="radio"
                  bind:group={answers[question]}
                  name={`${idx}-response`}
                  value={otherValue}
                />
                <input
                  bind:value={otherValue}
                  class="ml-2 border-b-2 border-black"
                />
              </div>
            </label>
          {:else}
            <label class="mr-5">
              <input
                type="radio"
                bind:group={answers[question]}
                name={`${idx}-response`}
                value={option}
              />
              {option}
            </label>
          {/if}
        {/each}
      </div>
    </div>
  {/each}
  {#if allAnswered}
    <Link to={"/feedback"}>Next</Link>
  {/if}
</div>
