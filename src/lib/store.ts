import { writable } from "svelte/store";

interface StoreData {
  sortOrder: string[];
  allocations: Record<string, number>;
  postCheckAllocations: Record<string, number>;
  demographics: Record<string, string>;
}

const InitialStore = {
  sortOrder: [],
  allocations: {},
  postCheckAllocations: {},
  demographics: {},
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

  const setIn = (group: keyof StoreData) => (key: string, val: number) =>
    persistUpdate((oldStore) => ({
      ...oldStore,
      [group]: { ...oldStore[group], [key]: val },
    }));

  return {
    subscribe,
    setSort: (sortOrder: string[]) =>
      persistUpdate((n) => ({ ...n, sortOrder })),
    setAllocation: (allocations: Record<string, number>) =>
      persistUpdate((n) => ({ ...n, allocations })),
    setAllocationKey: setIn("allocations"),
    setPostAllocationKey: setIn("allocations"),
    setDemographics: setIn("demographics"),
    reset: () => set({ ...InitialStore }),
  };
}

export const store = createStore();
