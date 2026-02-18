<script setup lang="ts">
import { RouterView } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
</script>

<template>
  <div class="flex h-screen flex-col">
    <AppHeader />
    <RouterView />
  </div>
</template>
