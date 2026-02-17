<script setup lang="ts">
import { computed } from 'vue'
import { useDark } from '@vueuse/core'
import { useVisualisationStore } from '@/stores/visualisation'
import { Bar, Bubble, Doughnut, Line, Pie, PolarArea, Radar, Scatter } from 'vue-chartjs'

const store = useVisualisationStore()
const isDark = useDark({ storageKey: 'spotify-unpacked-colour-mode' })

const barData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [{ label: 'Streams', backgroundColor: '#6366f1', data: [120, 190, 80, 140, 200, 160] }],
}

const lineData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [{ label: 'Listeners', borderColor: '#6366f1', data: [65, 59, 80, 81, 56, 72], fill: false }],
}

const pieData = {
  labels: ['Pop', 'Rock', 'Jazz', 'Hip-Hop', 'Electronic'],
  datasets: [{ backgroundColor: ['#6366f1', '#ec4899', '#f59e0b', '#10b981', '#3b82f6'], data: [30, 20, 15, 25, 10] }],
}

const doughnutData = {
  labels: ['Mobile', 'Desktop', 'Tablet', 'Smart TV'],
  datasets: [{ backgroundColor: ['#6366f1', '#ec4899', '#f59e0b', '#10b981'], data: [45, 30, 15, 10] }],
}

const radarData = {
  labels: ['Energy', 'Danceability', 'Valence', 'Acousticness', 'Tempo', 'Speechiness'],
  datasets: [
    { label: 'Track A', borderColor: '#6366f1', backgroundColor: 'rgba(99,102,241,0.2)', data: [80, 65, 70, 30, 55, 40] },
    { label: 'Track B', borderColor: '#ec4899', backgroundColor: 'rgba(236,72,153,0.2)', data: [50, 80, 60, 70, 45, 30] },
  ],
}

const polarAreaData = {
  labels: ['Acousticness', 'Danceability', 'Energy', 'Instrumentalness', 'Liveness'],
  datasets: [{ backgroundColor: ['#6366f1', '#ec4899', '#f59e0b', '#10b981', '#3b82f6'], data: [70, 85, 60, 30, 45] }],
}

const bubbleData = {
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
}

const scatterData = {
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
}

const baseOptions = computed(() => {
  const textColour = isDark.value ? 'rgba(255,255,255,0.85)' : 'rgba(0,0,0,0.8)'
  const gridColour = isDark.value ? 'rgba(255,255,255,0.1)' : 'rgba(0,0,0,0.1)'
  return { textColour, gridColour }
})

const cartesianOptions = computed(() => {
  const { textColour, gridColour } = baseOptions.value
  return {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: { ticks: { color: textColour }, grid: { color: gridColour } },
      y: { ticks: { color: textColour }, grid: { color: gridColour } },
    },
    plugins: { legend: { labels: { color: textColour } } },
  }
})

const radialOptions = computed(() => {
  const { textColour, gridColour } = baseOptions.value
  return {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      r: { ticks: { color: textColour, backdropColor: 'transparent' }, grid: { color: gridColour }, pointLabels: { color: textColour } },
    },
    plugins: { legend: { labels: { color: textColour } } },
  }
})

const simpleOptions = computed(() => {
  const { textColour } = baseOptions.value
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { labels: { color: textColour } } },
  }
})
</script>

<template>
  <Bar v-if="store.selectedChart === 'bar'" :key="`bar-${isDark}`" :data="barData" :options="cartesianOptions" />
  <Line v-else-if="store.selectedChart === 'line'" :key="`line-${isDark}`" :data="lineData" :options="cartesianOptions" />
  <Pie v-else-if="store.selectedChart === 'pie'" :key="`pie-${isDark}`" :data="pieData" :options="simpleOptions" />
  <Doughnut v-else-if="store.selectedChart === 'doughnut'" :key="`doughnut-${isDark}`" :data="doughnutData" :options="simpleOptions" />
  <Radar v-else-if="store.selectedChart === 'radar'" :key="`radar-${isDark}`" :data="radarData" :options="radialOptions" />
  <PolarArea v-else-if="store.selectedChart === 'polarArea'" :key="`polar-${isDark}`" :data="polarAreaData" :options="radialOptions" />
  <Bubble v-else-if="store.selectedChart === 'bubble'" :key="`bubble-${isDark}`" :data="bubbleData" :options="cartesianOptions" />
  <Scatter v-else-if="store.selectedChart === 'scatter'" :key="`scatter-${isDark}`" :data="scatterData" :options="cartesianOptions" />
</template>
