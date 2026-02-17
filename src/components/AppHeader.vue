<script setup lang="ts">
import { ref } from 'vue'
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from '@/components/ui/popover'

const isOpen = ref(false)
</script>

<template>
  <header
    class="bg-background border-b flex h-12 shrink-0 items-center justify-between px-4"
  >
    <span class="text-base font-semibold">Spotify Unpacked</span>

    <Popover v-model:open="isOpen">
      <PopoverTrigger as-child>
        <button
          class="text-muted-foreground hover:text-foreground text-sm transition-colors"
        >
          About
        </button>
      </PopoverTrigger>

      <Teleport to="body">
        <div
          v-if="isOpen"
          class="fixed inset-0 z-40 bg-black/20 backdrop-blur-[1px]"
          @click="isOpen = false"
        />
      </Teleport>

      <PopoverContent align="end" class="z-50 w-96">
        <div class="space-y-2">
          <h4 class="text-sm font-semibold">About Spotify Unpacked</h4>
          <p class="text-muted-foreground text-sm">
            An interactive tool for exploring your Spotify data export. All
            processing happens locally in your browser.
          </p>
          <p class="text-muted-foreground text-sm">
            Built by <!-- TODO: add names and links -->
          </p>
        </div>
      </PopoverContent>
    </Popover>
  </header>
</template>
