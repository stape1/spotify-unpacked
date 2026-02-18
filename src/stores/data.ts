import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { ChartData } from 'chart.js'

export interface LoadedFile {
  name: string
  size: number
}

interface StreamingEntry {
  ts: string
  ms_played: number
  master_metadata_track_name?: string
  master_metadata_album_artist_name?: string
}

interface PlaylistData {
  playlists: {
    name: string
    lastModifiedDate: string
    items: Array<{
      track?: {
        trackName: string
        artistName: string
      }
      addedDate: string
    }>
  }[]
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
  const files = ref<LoadedFile[]>([])
  const isLoading = ref(false)
  const chartData = ref<Record<string, ChartData>>({ ...dummyChartData })
  const streamingData = ref<StreamingEntry[]>([])
  const playlistData = ref<PlaylistData | null>(null)

  const fileCount = computed(() => files.value.length)
  const hasData = computed(() => files.value.length > 0)

  function getChartData(chartType: string): ChartData | undefined {
    return chartData.value[chartType]
  }

  async function parseStreamingFile(file: File): Promise<StreamingEntry[]> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = (event) => {
        try {
          const content = event.target?.result as string
          const data = JSON.parse(content) as StreamingEntry[]
          resolve(data)
        } catch (error) {
          reject(error)
        }
      }
      reader.onerror = () => reject(reader.error)
      reader.readAsText(file)
    })
  }

  async function parsePlaylistFile(file: File): Promise<PlaylistData> {
    return new Promise((resolve, reject) => {
      const reader = new FileReader()
      reader.onload = (event) => {
        try {
          const content = event.target?.result as string
          const data = JSON.parse(content) as PlaylistData
          resolve(data)
        } catch (error) {
          reject(error)
        }
      }
      reader.onerror = () => reject(reader.error)
      reader.readAsText(file)
    })
  }

  function generateStreamingChart(): void {
    if (streamingData.value.length === 0) {
      chartData.value.bar = { ...dummyChartData.bar }
      return
    }

    // Group by month and sum minutes played
    const monthlyData: Record<string, number> = {}

    for (const entry of streamingData.value) {
      if (entry.ms_played > 0) {
        const date = new Date(entry.ts)
        const monthKey = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`
        const minutes = entry.ms_played / 60000

        monthlyData[monthKey] = (monthlyData[monthKey] || 0) + minutes
      }
    }

    // Sort by month
    const sortedMonths = Object.keys(monthlyData).sort()
    const labels = sortedMonths.map((month) => {
      const [year, monthNum] = month.split('-')
      const date = new Date(parseInt(year), parseInt(monthNum) - 1)
      return date.toLocaleDateString('en-US', { month: 'short', year: '2-digit' })
    })

    const data = sortedMonths.map((month) => Math.round(monthlyData[month]))

    chartData.value.bar = {
      labels,
      datasets: [
        {
          label: 'Minutes Streamed',
          backgroundColor: '#6366f1',
          data,
        },
      ],
    }
  }

  function generatePlaylistBubbleChart(): void {
    if (!playlistData.value || streamingData.value.length === 0) {
      chartData.value.bubble = { ...dummyChartData.bubble }
      return
    }

    const bubbleData = []
    const playlistStats: Record<
      string,
      { totalMinutes: number; uniqueDays: Set<string>; trackCount: number }
    > = {}

    // Build a map of track names to streaming data for quick lookup
    const trackStreamingMap: Record<string, StreamingEntry[]> = {}
    for (const entry of streamingData.value) {
      if (entry.ms_played > 0 && entry.master_metadata_track_name && entry.master_metadata_album_artist_name) {
        const key = `${entry.master_metadata_track_name}|${entry.master_metadata_album_artist_name}`.toLowerCase()
        if (!trackStreamingMap[key]) {
          trackStreamingMap[key] = []
        }
        trackStreamingMap[key].push(entry)
      }
    }

    // Process each playlist
    for (const playlist of playlistData.value.playlists) {
      playlistStats[playlist.name] = {
        totalMinutes: 0,
        uniqueDays: new Set(),
        trackCount: playlist.items.length,
      }

      // Match tracks in playlist with streaming data
      for (const item of playlist.items) {
        if (item.track) {
          const trackKey = `${item.track.trackName}|${item.track.artistName}`.toLowerCase()
          const streamingEntries = trackStreamingMap[trackKey] || []

          for (const entry of streamingEntries) {
            playlistStats[playlist.name].totalMinutes += entry.ms_played / 60000
            const dayKey = new Date(entry.ts).toISOString().split('T')[0]
            playlistStats[playlist.name].uniqueDays.add(dayKey)
          }
        }
      }
    }

    // Create bubble chart data
    const bubbleDataPoints = []
    const colors = [
      'rgba(99,102,241,0.6)',
      'rgba(236,72,153,0.6)',
      'rgba(245,158,11,0.6)',
      'rgba(16,185,129,0.6)',
      'rgba(59,130,246,0.6)',
      'rgba(139,92,246,0.6)',
      'rgba(236,72,153,0.6)',
      'rgba(34,197,94,0.6)',
    ]

    Object.entries(playlistStats).forEach(([playlistName, stats], index) => {
      if (stats.totalMinutes > 0) {
        const uniqueDaysCount = stats.uniqueDays.size
        const avgMinutesPerDay = stats.totalMinutes / (uniqueDaysCount || 1)

        bubbleDataPoints.push({
          x: uniqueDaysCount,
          y: Math.round(stats.totalMinutes),
          r: Math.round(avgMinutesPerDay / 5) + 5,
          label: playlistName,
        })
      }
    })

    chartData.value.bubble = {
      datasets: [
        {
          label: 'Playlists',
          backgroundColor: colors[0],
          data: bubbleDataPoints,
        },
      ],
    }
  }

  async function loadFiles(rawFiles: File[]) {
    isLoading.value = true

    files.value = rawFiles.map((f) => ({
      name: f.name,
      size: f.size,
    }))

    // Parse streaming files
    for (const file of rawFiles) {
      if (file.name.toLowerCase().includes('streaming')) {
        try {
          const entries = await parseStreamingFile(file)
          streamingData.value = entries
          generateStreamingChart()
          generatePlaylistBubbleChart()
        } catch (error) {
          console.error('Error parsing streaming file:', error)
        }
      }
    }

    // Parse playlist files
    for (const file of rawFiles) {
      if (file.name.toLowerCase().includes('playlist')) {
        try {
          const data = await parsePlaylistFile(file)
          playlistData.value = data
          generatePlaylistBubbleChart()
        } catch (error) {
          console.error('Error parsing playlist file:', error)
        }
      }
    }

    isLoading.value = false
  }

  async function addFiles(rawFiles: File[]) {
    isLoading.value = true

    const newFiles = rawFiles.map((f) => ({
      name: f.name,
      size: f.size,
    }))

    files.value.push(...newFiles)

    // Parse streaming files
    for (const file of rawFiles) {
      if (file.name.toLowerCase().includes('streaming')) {
        try {
          const entries = await parseStreamingFile(file)
          streamingData.value.push(...entries)
          generateStreamingChart()
          generatePlaylistBubbleChart()
        } catch (error) {
          console.error('Error parsing streaming file:', error)
        }
      }
    }

    // Parse playlist files
    for (const file of rawFiles) {
      if (file.name.toLowerCase().includes('playlist')) {
        try {
          const data = await parsePlaylistFile(file)
          playlistData.value = data
          generatePlaylistBubbleChart()
        } catch (error) {
          console.error('Error parsing playlist file:', error)
        }
      }
    }

    isLoading.value = false
  }

  function clear() {
    files.value = []
    streamingData.value = []
    playlistData.value = null
    chartData.value = { ...dummyChartData }
  }

  return { files, isLoading, fileCount, hasData, chartData, getChartData, loadFiles, addFiles, clear }
})
