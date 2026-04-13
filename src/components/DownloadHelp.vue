<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

const firstInstructionPanel = {
  src: '/Panel1_DownlaodTitle.png',
  alt: 'Instructions on how to download your Spotify data',
}
</script>

<template>
  <Card>
    <RouterLink to="/downloadsteps" class="block rounded-lg transition hover:opacity-90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2">
      <CardHeader>
        <CardTitle>Download Help</CardTitle>
      </CardHeader>
      <CardContent class="space-y-3">
        <div class="overflow-hidden rounded-md border">
        <img :src="firstInstructionPanel.src" :alt="firstInstructionPanel.alt" class="h-auto w-full" />
        </div>
        <p class="text-sm text-muted-foreground">Click here to view the steps to request and download your Spotify data.</p>
      </CardContent>
    </RouterLink>
  </Card>
</template>
