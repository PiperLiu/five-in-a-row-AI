<script lang="ts" setup>
import { chessState } from '../hooks/useChessBoardHook'
import { defineProps, toRefs } from 'vue'

interface Props {
  rowIndex: number,
  colIndex: number,
  state: chessState
}
const props = defineProps<Props>()
const { state } = toRefs(props)

const getChessClass = (): string => {
  if (state.value === 'Player1') {
    return 'chess-state--player-1'
  } else if (state.value === 'Player2') {
    return 'chess-state--player-2'
  } else {
    return 'chess-state--no-chess'
  }
}
</script>

<template>
  <div
    class="chess"
    :class="getChessClass()"
  ></div>
</template>

<style>
.chess {
  display: inline-block;
  width: 100%;
  border: 1px solid;
}

.chess:hover {
  background-color: rgb(94, 94, 93);
}

.chess-state--no-chess {
  background-color: rgb(227, 240, 240);
}

.chess-state--player-1 {
  background-color: brown;
}

.chess-state--player-2 {
  background-color: rgb(72, 0, 206);
}
</style>
