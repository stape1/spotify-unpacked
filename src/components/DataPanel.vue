<script setup lang="ts">
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { ref } from 'vue'
import { ScrollArea } from '@/components/ui/scroll-area'
import { Button } from '@/components/ui/button'
import FileDropZone from '@/components/FileDropZone.vue'
import { useDataStore } from '@/stores/data'

const dataStore = useDataStore()
const dropZone = ref<InstanceType<typeof FileDropZone> | null>(null)

function onFilesDropped(files: File[]) {
  dataStore.loadFiles(files)
}

function onClear() {
  dataStore.clear()
  dropZone.value?.reset()
}
</script>

<template>
  <ScrollArea class="h-full">
    <div class="flex flex-col gap-4 p-4">
      <Card>
        <CardHeader>
          <CardTitle>Data</CardTitle>
          <CardDescription>Upload your Spotify data export</CardDescription>
        </CardHeader>
        <CardContent>
          <FileDropZone ref="dropZone" @files-dropped="onFilesDropped" />
        </CardContent>
      </Card>

      <Button v-if="dataStore.hasData" variant="outline" size="sm" class="w-full" @click="onClear">
        Clear data
      </Button>

      <Card>
        <CardHeader>
          <CardTitle>Statistics</CardTitle>
          <CardDescription>Summary of your loaded dataset</CardDescription>
        </CardHeader>
        <CardContent>
          <template v-if="dataStore.hasData">
            <ul class="text-sm space-y-1">
              <li>{{ dataStore.fileCount }} {{ dataStore.fileCount === 1 ? 'file' : 'files' }} loaded</li>
              <li v-for="file in dataStore.files" :key="file.name" class="text-muted-foreground truncate">
                {{ file.name }}
              </li>
            </ul>
          </template>
          <p v-else class="text-muted-foreground text-sm">No data loaded yet.</p>
        </CardContent>
      </Card>
    </div>
  </ScrollArea>
</template>
