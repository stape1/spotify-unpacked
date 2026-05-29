<script setup lang="ts">
import FileCard from '@/components/FileCard.vue';
import BanCard from '@/components/BanCard.vue';
import { useDataStore } from '@/stores/data';
import { fileTypes } from '@/lib/fileTypes';

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

    <div class="grid grid-cols-1 gap-4">
      <FileCard
        v-for="ft in fileTypes"
        :key="ft.key"
        :label="ft.label"
        :satisfied="datastore.fileTypeStatus[ft.key]"
        :what="ft.what"
        :file="ft.file"
        :why="ft.why"
      />
    </div>

  </div>

</template>

