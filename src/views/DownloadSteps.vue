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
        <img src="/Panel1_DownloadTitle.png" alt="Instructions on how to download your Spotify data" />
      </figure>

      <figure>
        <img src="/Panel2_Explain.png" alt="The download files you donate have your listening history and account data to understand what you listen to in 2025 from your library and from the Spotify algorithm." />
      </figure>

      <figure>
        <img src="/Panel3_OpenWebBrowser.png" alt="Log into Spotify in a browser" />
      </figure>

      <figure>
        <img src="/Panel4_AccessAccount.png" alt="Go to your account settings" />
      </figure>

      <figure>
        <img src="/Panel5_SelectAccountPrivacy.png" alt="Navigate to the Security and Privacy section" />
      </figure>

      <figure>
        <img src="/Panel6_RequestData.png" alt="Choose to download your Account Data and Extended streaming history" />
      </figure>

      <figure>
        <img src="/Panel7_Wait.png" alt="Wait for your data request to be processed" />
      </figure>

      <figure>
        <img src="/Panel8_ThankYou.png" alt="Thank you for requesting to download your Spotify data. When you donate your files to us, they will be visualised and sent back to you for your records." />
      </figure>
    </main>
    <RouterLink to="/">
      <button class="text-sm underline">Back to Dashboard</button>
    </RouterLink>
  </section>
</template>
