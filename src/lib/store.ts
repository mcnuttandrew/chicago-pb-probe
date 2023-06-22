import { writable } from "svelte/store";

interface StoreData {
  sortOrder: string[];
  allocations: Record<string, number>;
  postCheckAllocations: Record<string, number>;
  demographics: Record<string, string>;
  userId: string;
}

const InitialStore = {
  sortOrder: [],
  allocations: {},
  postCheckAllocations: {},
  demographics: {},
  userId: `${Math.floor(Math.random() * 1000000)}`,
};

function createStore() {
  const storeData: StoreData = JSON.parse(localStorage.getItem("ue-pb")) || {
    ...InitialStore,
  };
  const { subscribe, set, update } = writable<StoreData>(storeData);
  const persistUpdate = (updateFunc: (old: StoreData) => StoreData) =>
    update((oldStore) => {
      const newVal: StoreData = updateFunc(oldStore);
      localStorage.setItem("ue-pb", JSON.stringify(newVal));
      return newVal;
    });

  const setIn = (group: string) => (key: string, val: number) =>
    persistUpdate((oldStore) => ({
      ...oldStore,
      [group]: { ...oldStore[group], [key]: val },
    }));
  const simpleSet = (key: keyof StoreData) => (val: any) =>
    persistUpdate((n) => ({ ...n, [key]: val }));

  return {
    subscribe,
    setSort: simpleSet("sortOrder"),
    setAllocation: simpleSet("allocations"),
    setPostAllocation: simpleSet("postCheckAllocations"),
    setDemographics: simpleSet("demographics"),
    setAllocationKey: setIn("allocations"),
    setPostAllocationKey: setIn("postCheckAllocations"),
    reset: () => set({ ...InitialStore }),
  };
}

export const store = createStore();
