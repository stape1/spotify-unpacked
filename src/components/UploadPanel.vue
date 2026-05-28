<script setup lang="ts">
import BanCard from '@/components/BanCard.vue';
import FilesProgressPanel from '@/components/FilesProgressPanel.vue';
import { useDataStore } from '@/stores/data';

const datastore = useDataStore(); // initialise store 

</script>

<template>

  <div class="flex flex-col flex-1 gap-4 p-4">

    <!-- BAN row -->
    <div class="grid grid-cols-3 gap-4">
      <BanCard label="Listening time in 2025" :value="datastore.listeningTimeHours.toLocaleString()" unit="hours" />
      <BanCard label="Unique songs" :value="datastore.uniqueTrackCount.toLocaleString()" />
      <BanCard label="Favourite time of day" :value="datastore.favouriteHour ?? '-'"/>
    </div>

    <!-- File details panel -->
    <div class="flex-1">
      <FilesProgressPanel />
    </div>

  </div>

</template>

