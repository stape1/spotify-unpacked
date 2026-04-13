<script setup lang="ts">
import { RouterLink } from 'vue-router'

</script>

<template>
  <section class="mx-auto max-w-4xl p-6 space-y-6">
    <h1 class="text-2xl font-semibold">Download Instructions</h1>
    <p class="text-muted-foreground">
      Follow these steps to request and download your Spotify data.
    </p>

    <main class="panels">
      <figure>
        <img src="/Panel1_DownlaodTitle.png" alt="Instructions on how to download your Spotify data" />
      </figure>

      <figure>
        <img src="/Panel2_Explain.png" alt="The download files you donate have your listening history and account data to understand what you listen to in 2025 from your library and from the Spotify algorithm." />
      </figure>

      <figure>
        <img src="/Panel3_NavigateBrowserMenu.png" alt="Log into spotify in a browser, go to your account (icon top right window) and in the Security and Privacy section go to Account Privacy" />
      </figure>

      <figure>
        <img src="/Panel4_Choose2DownloadTypes.png" alt="Choose to download your Account Data and Extended streaming history" />
      </figure>

      <figure>
        <img src="/Panel5_Thankyou.png" alt="Thank you for requesting to download your Spotify data. When you donate your files to us, they will be visualised and sent back to you for your records." />

      </figure>
    </main>
    <RouterLink to="/">
      <button class="text-sm underline">Back to Dashboard</button>
    </RouterLink>
  </section>
</template>
