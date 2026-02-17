<script setup lang="ts">
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { useDataStore } from '@/stores/data'

const dataStore = useDataStore()
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
          <li>{{ dataStore.fileCount }} {{ dataStore.fileCount === 1 ? 'file' : 'files' }} loaded</li>
          <li v-for="file in dataStore.files.slice(0, 12)" :key="file.name" class="text-muted-foreground truncate">
            {{ file.name }}
          </li>
          <li v-if="dataStore.fileCount > 12" class="text-muted-foreground/60 text-xs">
            ...and {{ dataStore.fileCount - 12 }} more
          </li>
        </ul>
      </template>
      <p v-else class="text-muted-foreground text-sm">No data loaded yet.</p>
    </CardContent>
  </Card>
</template>
