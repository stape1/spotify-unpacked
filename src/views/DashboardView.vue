<script setup lang="ts">
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from '@/components/ui/resizable'
import AppHeader from '@/components/AppHeader.vue'
import DataPanel from '@/components/DataPanel.vue'
import VisualisationPanel from '@/components/VisualisationPanel.vue'
import ControlsPanel from '@/components/ControlsPanel.vue'
</script>

<template>
  <div class="flex h-screen flex-col">
    <AppHeader />

    <ResizablePanelGroup direction="horizontal" class="flex-1">
      <ResizablePanel :default-size="20" :min-size="15" :max-size="30">
        <DataPanel />
      </ResizablePanel>

      <ResizableHandle with-handle />

      <ResizablePanel :default-size="55" :min-size="30">
        <VisualisationPanel />
      </ResizablePanel>

      <ResizableHandle with-handle />

      <ResizablePanel :default-size="25" :min-size="15" :max-size="35">
        <ControlsPanel />
      </ResizablePanel>
    </ResizablePanelGroup>
  </div>
</template>
