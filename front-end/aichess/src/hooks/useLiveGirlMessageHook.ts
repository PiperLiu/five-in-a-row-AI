import { ref } from 'vue'

const liveGirlMessage = ref('')
const liveGirlMessageTime = ref(0)

const setNewLiveGirlMessage = (message: string, time = 3000) => {
  liveGirlMessage.value = message
  liveGirlMessageTime.value = time
}

export {
  liveGirlMessage,
  liveGirlMessageTime,
  setNewLiveGirlMessage
}
