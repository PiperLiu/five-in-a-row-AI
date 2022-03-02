import { reactive } from 'vue'

type chessState = 'noChess' | 'Player1' | 'Player2'

type ChessRow = Array<chessState>
type Board = Array<ChessRow>

const useChessBoard = (row: number, col: number) => {
  const initBoard = (): Board => {
    const board = reactive<Board>([])
    for (let i = 0; i < row; i++) {
      board.push([])
      for (let j = 0; j < col; j++) {
        board[i].push('noChess')
      }
    }
    return board
  }

  const board = initBoard()

  const changeChessState = (r: number, c: number, state: chessState): void => {
    board[r][c] = state
  }

  return {
    board,
    changeChessState
  }
}

export default useChessBoard

export { chessState, Board }
