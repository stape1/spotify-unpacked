import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { ChartData } from 'chart.js'
import { parseStreamingFile, type MusicEntry } from '@/lib/parser'


export interface LoadedFile {
  name: string
  size: number
}

const dummyChartData: Record<string, ChartData> = {
  bar: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      { label: 'Streams', backgroundColor: '#6366f1', data: [120, 190, 80, 140, 200, 160] },
    ],
  },
  line: {
    labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
    datasets: [
      { label: 'Listeners', borderColor: '#6366f1', data: [65, 59, 80, 81, 56, 72], fill: false },
    ],
  },
  pie: {
    labels: ['Pop', 'Rock', 'Jazz', 'Hip-Hop', 'Electronic'],
    datasets: [
      {
        backgroundColor: ['#6366f1', '#ec4899', '#f59e0b', '#10b981', '#3b82f6'],
        data: [30, 20, 15, 25, 10],
      },
    ],
  },
  doughnut: {
    labels: ['Mobile', 'Desktop', 'Tablet', 'Smart TV'],
    datasets: [
      { backgroundColor: ['#6366f1', '#ec4899', '#f59e0b', '#10b981'], data: [45, 30, 15, 10] },
    ],
  },
  radar: {
    labels: ['Energy', 'Danceability', 'Valence', 'Acousticness', 'Tempo', 'Speechiness'],
    datasets: [
      {
        label: 'Track A',
        borderColor: '#6366f1',
        backgroundColor: 'rgba(99,102,241,0.2)',
        data: [80, 65, 70, 30, 55, 40],
      },
      {
        label: 'Track B',
        borderColor: '#ec4899',
        backgroundColor: 'rgba(236,72,153,0.2)',
        data: [50, 80, 60, 70, 45, 30],
      },
    ],
  },
  polarArea: {
    labels: ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness'],
    datasets: [
      {
        backgroundColor: ['#6366f1', '#ec4899', '#f59e0b', '#10b981', '#3b82f6'],
        data: [70, 85, 60, 30, 45],
      },
    ],
  },
  bubble: {
    datasets: [
      {
        label: 'Playlist A',
        backgroundColor: 'rgba(99,102,241,0.5)',
        data: [
          { x: 10, y: 20, r: 15 },
          { x: 25, y: 35, r: 10 },
          { x: 40, y: 10, r: 20 },
        ],
      },
      {
        label: 'Playlist B',
        backgroundColor: 'rgba(236,72,153,0.5)',
        data: [
          { x: 15, y: 40, r: 12 },
          { x: 30, y: 25, r: 18 },
          { x: 50, y: 30, r: 8 },
        ],
      },
    ],
  },
  scatter: {
    datasets: [
      {
        label: 'Tempo vs Energy',
        backgroundColor: '#6366f1',
        data: [
          { x: 80, y: 40 },
          { x: 100, y: 60 },
          { x: 120, y: 75 },
          { x: 140, y: 55 },
          { x: 160, y: 85 },
          { x: 90, y: 50 },
          { x: 110, y: 70 },
        ],
      },
    ],
  },
}

export const useDataStore = defineStore('data', () => {
  const entries = ref<MusicEntry[]>([])
  const files = ref<LoadedFile[]>([])
  const isLoading = ref(false)
  const chartData = ref<Record<string, ChartData>>({ ...dummyChartData })

  const fileCount = computed(() => files.value.length)
  const hasData = computed(() => files.value.length > 0)

  function getChartData(chartType: string): ChartData | undefined {
    return chartData.value[chartType]
  }
async function loadFiles(rawFiles: File[]) {
  isLoading.value = true

  for (const file of rawFiles) {
    const text = await file.text()
    const json = JSON.parse(text)
    const parsed = parseStreamingFile(json)
    entries.value.push(...parsed)
    files.value.push({ name: file.name, size: file.size })
  }

  isLoading.value = false
}

const listeningTimeHours = computed(() => {
  const totalMs = entries.value.reduce((sum, e) => sum + e.msPlayed, 0)
  return Math.round(totalMs / 1000 / 60 / 60)
})

const uniqueTrackCount = computed(() => {
  return new Set(entries.value.map((e) => e.trackUri)).size
})

const favouriteHour = computed(() => {
  const counts: Record<number, number> = {}
  for (const entry of entries.value) {
    const hour = new Date(entry.ts).getHours()
    counts[hour] = (counts[hour] ?? 0) + 1
  }
  const topHour = Object.entries(counts).sort((a, b) => b[1] - a[1])[0]
  if (!topHour) return null
  return new Date(0, 0, 0, Number(topHour[0])).toLocaleTimeString([], { hour: 'numeric', hour12: true })
})

function clear() {
  files.value = []
  entries.value = []
  chartData.value = { ...dummyChartData }
}

  return { files, entries, isLoading, fileCount, hasData, chartData, getChartData, loadFiles, clear, listeningTimeHours, uniqueTrackCount, favouriteHour }
})
