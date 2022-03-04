<script lang="ts" setup>
import { defineProps, toRefs, withDefaults } from 'vue'
import ChessComponent from './ChessComponent.vue'
import useChessBoard from '../hooks/useChessBoardHook'
import useChessGame from '../hooks/useChessGameHook'
import useChessRequest from '@/hooks/useChessRequestHook'
import { setNewLiveGirlMessage } from '@/hooks/useLiveGirlMessageHook'

interface Props {
  boardHeight?: number,
  boardWidth?: number
}

const props = withDefaults(defineProps<Props>(), {
  boardHeight: 15,
  boardWidth: 15
})

const { boardHeight, boardWidth } = toRefs(props)
const { board, changeChessState } = useChessBoard(boardHeight.value, boardWidth.value)
const { initGame, putChess, getWinner } = useChessGame(board, changeChessState)
const { requestAi, chessRequestingLock } = useChessRequest(board, 'Player2')

initGame()

const click = async (rowIndex: number, colIndex: number) => {
  if (chessRequestingLock.value) {
    setNewLiveGirlMessage('等下(￣ ‘i ￣;) 人家还没想完', 50000)
  } else {
    putChess(rowIndex, colIndex)
    setNewLiveGirlMessage('让我想想ヾ(≧▽≦*)', 50000)
    const move = await requestAi('/', rowIndex * board[0].length + colIndex)
    const winner = getWinner(move)
    if (!winner) {
      const x = Math.floor(move / board[0].length)
      const y = move % board[0].length
      setNewLiveGirlMessage(`我要下在 ${x}, ${y} !`, 1000)
      putChess(x, y)
    } else {
      if (winner === 'Player1') {
        setNewLiveGirlMessage('不可能的(⊙_⊙)', 50000)
      } else if (winner === 'Player2') {
        setNewLiveGirlMessage('正常正常~下次再战 ( •̀ .̫ •́ )✧', 50000)
      }
    }
  }
}
</script>

<template>
  <div class="container">
    <div class="dummy"></div>
    <div class="board">
      <div class="row" v-for="i in boardHeight" :key="'row' + (i - 1)">
        <ChessComponent
          v-for="j in boardWidth" :key="(i - 1).toString() + ',' + (j - 1).toString()"
          :row-index="i - 1"
          :col-index="j - 1"
          :state="board[i - 1][j - 1]"
          @click="click(i - 1, j - 1)"
        ></ChessComponent>
      </div>
    </div>
  </div>
</template>

<style>
/* 自适应高度 */
.container {
  display: inline-block;
  position: relative;
  width: 90%;
  max-width: 75vh;
  text-align: center;
}

.dummy {
  margin-top: 100%;
}

.board {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: silver;
}

/* 棋子 flex 布局 */
.board {
  display: flex;
  flex: 1;
  flex-direction: column;
  justify-content: space-around;
  align-items: center;
}

.row {
  width: 100%;
  display: flex;
  flex: 1;
  flex-direction: row;
  justify-content: space-around;
}
</style>
