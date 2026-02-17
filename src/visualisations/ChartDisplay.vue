<script setup lang="ts">
import { useVisualisationStore } from '@/stores/visualisation'
import { Bar, Bubble, Doughnut, Line, Pie, PolarArea, Radar, Scatter } from 'vue-chartjs'

const store = useVisualisationStore()

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

const chartOptions = { responsive: true, maintainAspectRatio: false }
</script>

<template>
  <Bar v-if="store.selectedChart === 'bar'" :data="barData" :options="chartOptions" />
  <Line v-else-if="store.selectedChart === 'line'" :data="lineData" :options="chartOptions" />
  <Pie v-else-if="store.selectedChart === 'pie'" :data="pieData" :options="chartOptions" />
  <Doughnut v-else-if="store.selectedChart === 'doughnut'" :data="doughnutData" :options="chartOptions" />
  <Radar v-else-if="store.selectedChart === 'radar'" :data="radarData" :options="chartOptions" />
  <PolarArea v-else-if="store.selectedChart === 'polarArea'" :data="polarAreaData" :options="chartOptions" />
  <Bubble v-else-if="store.selectedChart === 'bubble'" :data="bubbleData" :options="chartOptions" />
  <Scatter v-else-if="store.selectedChart === 'scatter'" :data="scatterData" :options="chartOptions" />
</template>
