import { computed, ref } from 'vue'
import { chessState, Board } from './useChessBoardHook'
import { setNewLiveGirlMessage } from './useLiveGirlMessageHook'

type Player = 'Player1' | 'Player2'

const useChessGame = (
  board: Board,
  changeChessState: (row: number, col: number, state: chessState | Player) => void
) => {
  const currentPlayer = ref<Player>('Player1')
  const oppositePlayer = computed(
    () => currentPlayer.value === 'Player1' ? 'Player2' : 'Player1'
  )

  const changeCurrentPlayerTo = (player: Player) => {
    currentPlayer.value = player
  }

  const NextPlayerTurn = () => {
    if (currentPlayer.value === 'Player1') {
      currentPlayer.value = 'Player2'
    } else {
      currentPlayer.value = 'Player1'
    }
  }

  const initGame = () => {
    for (let i = 0; i < board.length; i++) {
      for (let j = 0; j < board[0].length; j++) {
        changeChessState(i, j, 'noChess')
      }
    }
    changeCurrentPlayerTo('Player1')
    setNewLiveGirlMessage('请君先手（￣︶￣）↗', 3000)
  }

  const putChess = (row: number, col: number) => {
    if (board[row][col] !== 'noChess') {
      throw Error(`${row},${col} 必须是无子的!`)
    }
    changeChessState(row, col, currentPlayer.value)
    NextPlayerTurn()
  }

  const getWinner = (move: number): Player | boolean => {
    if (move === -2) return 'Player2'
    else if (move === -1) return 'Player1'
    return false
  }

  return {
    currentPlayer,
    oppositePlayer,
    changeCurrentPlayerTo,
    NextPlayerTurn,
    initGame,
    putChess,
    getWinner
  }
}

export default useChessGame

export { Player }
