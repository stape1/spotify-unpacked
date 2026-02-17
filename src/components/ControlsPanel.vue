<script setup lang="ts">
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { ScrollArea } from '@/components/ui/scroll-area'
</script>

<template>
  <ScrollArea class="h-full">
    <div class="flex flex-col gap-4 p-4">
      <Card>
        <CardHeader>
          <CardTitle>Controls</CardTitle>
          <CardDescription>Configure your visualisation</CardDescription>
        </CardHeader>
        <CardContent>
          <p class="text-muted-foreground text-sm">
            No visualisation selected.
          </p>
        </CardContent>
      </Card>
    </div>
  </ScrollArea>
</template>
