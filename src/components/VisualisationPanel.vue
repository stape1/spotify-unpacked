<script setup lang="ts">
import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import ChartDisplay from '@/visualisations/ChartDisplay.vue'
</script>

<template>
  <div class="flex h-full flex-col gap-4 p-4">
    <Card class="flex flex-1 flex-col">
      <CardHeader>
        <CardTitle>Visualisation</CardTitle>
      </CardHeader>
      <CardContent class="relative flex flex-1">
        <div class="absolute inset-0 p-6 pt-0">
          <ChartDisplay />
        </div>
      </CardContent>
    </Card>
  </div>
</template>
