<script setup lang="ts">

import { computed } from 'vue'
import { useDark } from '@vueuse/core'
import { useDataStore } from '@/stores/data'


const dataStore = useDataStore()
const isDark = useDark({ storageKey: 'spotify-unpacked-colour-mode' })
const currentData = computed(() => dataStore.getChartData(visStore.selectedChart) as any)

const baseOptions = computed(() => {
  const textColour = isDark.value ? 'rgba(255,255,255,0.85)' : 'rgba(0,0,0,0.8)'
  const gridColour = isDark.value ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'
  return { textColour, gridColour }
})


</script>
<template>
  <div class="mx-auto max-w-4xl p-6 space-y-6">
    <h1 class="text-2xl font-semibold">Upload Status</h1>
    <p class="text-muted-foreground">
      Thank you for donating your Spotify data! We are currently processing your upload and will notify you when your visualisations are ready.
    </p>
    <p class="text-muted-foreground">
      In the meantime, feel free to explore the dashboard and see what insights you can find from the sample data.
    </p>
  </div>
</template>