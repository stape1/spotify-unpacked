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
          <CardTitle>Data</CardTitle>
          <CardDescription>Upload your Spotify data export</CardDescription>
        </CardHeader>
        <CardContent>
          <div
            class="border-muted-foreground/25 flex h-32 flex-col items-center justify-center rounded-lg border-2 border-dashed"
          >
            <p class="text-muted-foreground text-sm">
              Drop files here or click to upload
            </p>
          </div>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Statistics</CardTitle>
          <CardDescription>Summary of your loaded dataset</CardDescription>
        </CardHeader>
        <CardContent>
          <p class="text-muted-foreground text-sm">No data loaded yet.</p>
        </CardContent>
      </Card>
    </div>
  </ScrollArea>
</template>
