<script setup lang="ts">
import { RouterLink } from 'vue-router'
import { Button } from '@/components/ui/button'
</script>

<template>
  <div class="flex h-full flex-col items-center justify-center gap-4 p-8">
    <p class="text-muted-foreground text-sm">Data donation details coming soon.</p>
    <RouterLink to="/">
      <Button variant="outline" size="sm">Back to Dashboard</Button>
    </RouterLink>
  </div>
</template>
