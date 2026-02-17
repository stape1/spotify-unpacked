<script setup lang="ts">
import { ref } from 'vue'
import { Upload, FileCheck, LoaderCircle } from 'lucide-vue-next'

const emit = defineEmits<{
  filesDropped: [files: File[]]
}>()

const isDragOver = ref(false)
const isProcessing = ref(false)
const fileCount = ref(0)
const fileInput = ref<HTMLInputElement | null>(null)

function onDragOver(event: DragEvent) {
  event.preventDefault()
  isDragOver.value = true
}

function onDragLeave() {
  isDragOver.value = false
}

async function readDirectoryEntries(directory: FileSystemDirectoryEntry): Promise<File[]> {
  const reader = directory.createReader()
  const files: File[] = []

  let batch: FileSystemEntry[] = []
  do {
    batch = await new Promise((resolve, reject) => reader.readEntries(resolve, reject))
    for (const entry of batch) {
      if (entry.isFile) {
        const file = await new Promise<File>((resolve, reject) =>
          (entry as FileSystemFileEntry).file(resolve, reject),
        )
        files.push(file)
      } else if (entry.isDirectory) {
        files.push(...(await readDirectoryEntries(entry as FileSystemDirectoryEntry)))
      }
    }
  } while (batch.length > 0)

  return files
}

async function collectFiles(event: DragEvent): Promise<File[]> {
  const items = Array.from(event.dataTransfer?.items ?? [])
  const files: File[] = []

  for (const item of items) {
    const entry = item.webkitGetAsEntry?.()
    if (entry?.isDirectory) {
      files.push(...(await readDirectoryEntries(entry as FileSystemDirectoryEntry)))
    } else if (entry?.isFile) {
      const file = await new Promise<File>((resolve, reject) =>
        (entry as FileSystemFileEntry).file(resolve, reject),
      )
      files.push(file)
    }
  }

  return files
}

async function onDrop(event: DragEvent) {
  event.preventDefault()
  isDragOver.value = false
  isProcessing.value = true

  const files = await collectFiles(event)
  isProcessing.value = false
  if (files.length > 0) {
    fileCount.value = files.length
    emit('filesDropped', files)
  }
}

function onClickBrowse() {
  fileInput.value?.click()
}

function onFileSelected(event: Event) {
  const input = event.target as HTMLInputElement
  const files = Array.from(input.files ?? [])
  if (files.length > 0) {
    fileCount.value = files.length
    emit('filesDropped', files)
  }
  input.value = ''
}

function reset() {
  fileCount.value = 0
  isProcessing.value = false
}

defineExpose({ reset })
</script>

<template>
  <div
    class="flex h-32 cursor-pointer flex-col items-center justify-center gap-2 rounded-lg border-2 border-dashed transition-colors"
    :class="
      isDragOver
        ? 'border-primary bg-primary/5'
        : 'border-muted-foreground/25 hover:border-muted-foreground/50'
    "
    @dragover="onDragOver"
    @dragleave="onDragLeave"
    @drop="onDrop"
    @click="onClickBrowse"
  >
    <template v-if="isProcessing">
      <LoaderCircle class="text-primary h-6 w-6 animate-spin" />
      <p class="text-muted-foreground text-sm">Reading files...</p>
    </template>
    <template v-else-if="fileCount > 0 && !isDragOver">
      <FileCheck class="text-primary h-6 w-6" />
      <p class="text-muted-foreground text-sm">
        Uploaded {{ fileCount }} {{ fileCount === 1 ? 'file' : 'files' }}
      </p>
    </template>
    <template v-else>
      <Upload class="text-muted-foreground h-6 w-6" :class="{ 'text-primary': isDragOver }" />
      <p class="text-muted-foreground text-sm">
        {{ isDragOver ? 'Drop files to upload' : 'Drop files here or click to browse' }}
      </p>
    </template>
    <input
      ref="fileInput"
      type="file"
      multiple
      accept=".json"
      class="hidden"
      @change="onFileSelected"
    />
  </div>
</template>
