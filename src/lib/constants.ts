type Categories =
  | "Biking and Transport"
  | "Libraries and Schools"
  | "Parks and Environment"
  | "Arts and Culture"
  | "Streets and Sidewalks";
export const projects: Record<
  string,
  { min: number; max: number; description: string; category: Categories }
> = {
  "Street Resurfacing": {
    max: 93500, // 250000, 480000, 500000, 510000, 600000, 600000, 650000
    min: 34666,
    description:
      "Street resurfacing is determined by a percentage of the budget. 100% of the budget allows for 16 streets to be resurfaced, while 50% covers resurfacing for 9 streets.",
    category: "Streets and Sidewalks",
  },
  "Bike Lanes": {
    max: 75000, // 125000
    min: 10000,
    description:
      "The bike lanes would run with traffic on Maplewood from Montrose to Wilson; with traffic on Campbell from Wilson to Montrose. They would connect with the future Leland Greenway on Campbell. The bike lanes would not impact parking.",
    category: "Biking and Transport",
  },
  "School Improvements": {
    max: 500000,
    min: 50000, //  2500, 5000, 17000, 37000
    description:
      "A nature play space at Bateman would be a dream come true for the school, parents, and students. Bateman’s community is working collaboratively to design natural play and learning areas for the children. These funds would help make this proposal feasible and allow them to give their students a new and educational play area.",
    category: "Libraries and Schools",
  },
  "Picnic Tables": {
    max: 45000,
    min: 12500,
    description:
      "This proposal includes new pool tables with umbrellas as well as picnic tables outside of the California Park pool area, and ADA accessible picnic tables near the softball field to create pleasant gathering spots for all.",
    category: "Parks and Environment",
  },
  "Street Lights": {
    max: 130000, // 11200
    min: 55000, // 234600, 390000, 454000
    description:
      "This project focuses on improving safety at W. Belmont Ave and N. Narragansett Ave. Turn signals and refreshed crosswalks would dramatically improve the busy intersection!",
    category: "Streets and Sidewalks",
  },
  "Food Pantry": {
    max: 2500, // only one instance
    min: 2500, // only one instance
    description:
      "During the pandemic, neighbors came together to create a food pantry out of a plastic shed at the Drake Garden. This proposal is would fund the creation of permanent structure which will hold food pantry items, serve as a shed for neighbors and volunteers to store tools & supplies, and a fold-out stand to hold small event sales.",
    category: "Parks and Environment",
    // AM: unsure about this one
  },
  "Street Murals": {
    max: 190000,
    min: 32500, // 6000, 12000, 12000, 19200, 20000
    description:
      "In partnership with the Green Star Movement, this mural would go along the South-west side of the school by the main entrance on Lincoln Avenue.",
    category: "Arts and Culture",
  },
  "Curb Cuts": {
    max: 40000,
    min: 20000,
    description:
      "Install curb cuts and crosswalk at 7557 N. Paulina to allow people with strollers or mobility impairments to access the north end of the train station.",
    category: "Streets and Sidewalks",
  },
};

export const buttonStyle =
  "border-blue-700 border-2 rounded bg-blue-200 px-8 py-4";
