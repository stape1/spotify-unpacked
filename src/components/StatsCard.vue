<script setup lang="ts">
import { computed } from 'vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { useDataStore } from '@/stores/data'

const dataStore = useDataStore()

const fileCounts = computed(() => {
  const counts = {
    streaming: 0,
    library: 0,
    playlist: 0,
    unrecognised: 0,
  }

  dataStore.files.forEach((file) => {
    const nameLower = file.name.toLowerCase()
    if (nameLower.includes('streaming')) {
      counts.streaming++
    } else if (nameLower.includes('library')) {
      counts.library++
    } else if (nameLower.includes('playlist')) {
      counts.playlist++
    } else {
      counts.unrecognised++
    }
  })

  return counts
})
</script>

<template>
  <Card>
    <CardHeader>
      <CardTitle>Statistics</CardTitle>
      <CardDescription>Summary of your loaded dataset</CardDescription>
    </CardHeader>
    <CardContent>
      <template v-if="dataStore.hasData">
        <ul class="text-sm space-y-1">
          <li>
            {{ fileCounts.streaming }} {{ fileCounts.streaming === 1 ? 'streaming file' : 'streaming files' }} loaded
          </li>
          <li>
            {{ fileCounts.library }} {{ fileCounts.library === 1 ? 'library file' : 'library files' }} loaded
          </li>
          <li>
            {{ fileCounts.playlist }} {{ fileCounts.playlist === 1 ? 'playlist file' : 'playlist files' }} loaded
          </li>
          <li v-if="fileCounts.unrecognised > 0">
            {{ fileCounts.unrecognised }} {{ fileCounts.unrecognised === 1 ? 'unrecognised file' : 'unrecognised files' }} loaded
          </li>
        </ul>
      </template>
      <p v-else class="text-muted-foreground text-sm">No data loaded yet.</p>
    </CardContent>
  </Card>
</template>
