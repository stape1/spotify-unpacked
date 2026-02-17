import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useVisualisationStore = defineStore('visualisation', () => {
  const selectedChart = ref('bar')

  return { selectedChart }
})
