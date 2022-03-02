<script lang="ts" setup>
import { computed, onMounted, ref } from 'vue'
import { liveGirlMessage, liveGirlMessageTime, setNewLiveGirlMessage } from '@/hooks/useLiveGirlMessageHook'

onMounted(() => {
  (window as unknown as Record<'loadlive2d', (arg1: string, arg2: string) => void>)
    .loadlive2d('live2d', '/live2d/model/tia/model.json')
})

const messageHidden = computed(() => {
  return liveGirlMessageTime.value === 0
})

const timeHidden = ref(0)
const hiddenWrapper = computed(() => {
  return timeHidden.value !== 0
})

setInterval(() => {
  if (timeHidden.value > 200) timeHidden.value -= 200
  else timeHidden.value = 0

  if (liveGirlMessageTime.value > 200) liveGirlMessageTime.value -= 200
  else liveGirlMessageTime.value = 0
}, 200)

const mouseOver = () => {
  setNewLiveGirlMessage('你碰不到我(●ˇ∀ˇ●)', 1000)
  timeHidden.value = 1000
}
</script>

<template>
<div class="wrapper"
  @mouseover="mouseOver"
  :style="{
    opacity: hiddenWrapper ? 0.3 : 1.0,
    'pointer-events': hiddenWrapper ? 'none' : 'auto'
  }"
>
  <div
    class="message"
    v-show="!messageHidden"> {{ liveGirlMessage }} </div>
  <canvas
    id="live2d"
    width="280"
    height="250"
  ></canvas>
</div>
</template>

<style>
.wrapper {
  display: inline-block;
  position: absolute;
  right: 30px;
  bottom: 5px;
  pointer-events: none;
}
</style>
