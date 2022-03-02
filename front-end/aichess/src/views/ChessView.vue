<script lang="ts" setup>
import BoardComponent from '../components/BoardComponent.vue'
import LiveGirlComponent from '../components/LiveGirlComponent.vue'
const boardHeight = 8
const boardWidth = 8
</script>

<template>
  <BoardComponent
    :boardHeight="boardHeight"
    :board-height="boardHeight"
    :board-width="boardWidth"
  />
  <LiveGirlComponent />
</template>
