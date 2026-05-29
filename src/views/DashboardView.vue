<script setup lang="ts">
import { ResizableHandle, ResizablePanel, ResizablePanelGroup } from '@/components/ui/resizable'
import DataPanel from '@/components/DataPanel.vue'
import UploadPanel from '@/components/UploadPanel.vue'
import ControlsPanel from '@/components/ControlsPanel.vue'
</script>

<template>
  <ResizablePanelGroup direction="horizontal" class="flex-1">
    <ResizablePanel :default-size="20" :min-size="15" :max-size="30">
      <DataPanel />
    </ResizablePanel>

    <ResizableHandle with-handle />

    <ResizablePanel :default-size="55" :min-size="30">
      <UploadPanel />
    </ResizablePanel>

    <ResizableHandle with-handle />

    <ResizablePanel :default-size="25" :min-size="15" :max-size="35">
      <ControlsPanel />
    </ResizablePanel>
  </ResizablePanelGroup>
</template>
