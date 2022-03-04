import axios from 'axios'
import { ref } from 'vue'
import { Board } from './useChessBoardHook'
import { Player } from './useChessGameHook'
import { setNewLiveGirlMessage } from './useLiveGirlMessageHook'

axios.defaults.baseURL = ''

const useChessRequest = (board: Board, aiPlayer: Player) => {
  const chessRequestingLock = ref<boolean>(false)

  const lock = () => {
    chessRequestingLock.value = true
    console.log('lock chessRequestingLock')
  }
  const unlock = () => {
    chessRequestingLock.value = false
    console.log('unlock chessRequestingLock')
  }

  const reformData = (lastMove: number) => {
    const states: Record<number, number> = {}
    for (let i = 0; i < board.length; i++) {
      for (let j = 0; j < board[0].length; j++) {
        if (board[i][j] !== 'noChess') {
          states[i * board[0].length + j] = board[i][j] === 'Player1' ? 1 : 2
        }
      }
    }
    return {
      states,
      last_move: lastMove,
      player: aiPlayer === 'Player1' ? 1 : 2
    }
  }

  const post = (url: string, data = {}) => {
    return new Promise((resolve, reject) => {
      axios.post(url, data, {
        baseURL: 'http://aichess.piperliu.xyz',
        headers: {
          'Content-Type': 'application/json'
        }
      }).then((response) => {
        resolve(response)
      }, err => {
        reject(err)
      })
    })
  }

  const requestAi = async (url: string, lastMove: number) => {
    lock()
    try {
      const request: any = await post(url, reformData(lastMove))
      return request.data
    } catch (e) {
      setNewLiveGirlMessage('(⊙x⊙;) 遇到了故障...', 5000)
      throw Error('requestAi post error')
    } finally {
      unlock()
    }
  }

  return {
    chessRequestingLock,
    lock,
    unlock,
    requestAi
  }
}

export default useChessRequest
