<script setup lang="ts">
import { RouterLink } from 'vue-router'

const panels = [
  {
    src: '/Panel1_DownloadTitle.png',
    alt: 'Instructions on how to download your Spotify data',
  },
  {
    src: '/Panel2_Explain.png',
    alt: 'The download files you donate have your listening history and account data to understand what you listen to in 2025 from your library and from the Spotify algorithm.',
  },
  {
    src: '/Panel3_OpenWebBrowser.png',
    alt: 'Log into Spotify in a browser',
  },
  {
    src: '/Panel4_AccessAccount.png',
    alt: 'Go to your account settings',
  },
  {
    src: '/Panel5_SelectAccountPrivacy.png',
    alt: 'Navigate to the Security and Privacy section',
  },
  {
    src: '/Panel6_RequestData.png',
    alt: 'Choose to download your Account Data and Extended streaming history',
  },
  {
    src: '/Panel7_Wait.png',
    alt: 'Wait for your data request to be processed',
  },
  {
    src: '/Panel8_ThankYou.png',
    alt: 'Thank you for requesting to download your Spotify data. When you donate your files to us, they will be visualised and sent back to you for your records.',
  },
]
</script>

<template>
  <section class="mx-auto max-w-4xl p-6 space-y-6">
    <h1 class="text-2xl font-semibold">Download Instructions</h1>
    <p class="text-muted-foreground">
      Follow every step to request and download your Spotify data.
    </p>

    <main class="panels">
      <figure v-for="panel in panels" :key="panel.src">
        <img :src="panel.src" :alt="panel.alt" />
      </figure>
    </main>
    <RouterLink to="/">
      <button class="text-sm underline">Back to Dashboard</button>
    </RouterLink>
  </section>
</template>
