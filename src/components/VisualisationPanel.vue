<script setup lang="ts">
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
</script>

<template>
  <div class="flex h-full flex-col gap-4 p-4">
    <Card class="flex flex-1 flex-col">
      <CardHeader>
        <CardTitle>Visualisation</CardTitle>
      </CardHeader>
      <CardContent class="flex flex-1 items-center justify-center">
        <p class="text-muted-foreground text-sm">
          Upload data to get started.
        </p>
      </CardContent>
    </Card>
  </div>
</template>
