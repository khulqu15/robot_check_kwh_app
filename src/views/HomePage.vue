<template>
  <ion-page>
    <ion-content :fullscreen="true">
      <div class="w-full relative md:p-12 p-6 bg-base-100 overflow-x-hidden text-base-content">
        <div class="min-h-screen">
          <div class="flex w-full items-center justify-between">
            <div class="flex justify-start items-center gap-3">
              <img src="/flash.png" class="w-10" alt="Lighting Logo">
              <h1 class="text-xl font-bold">{{ menu_selected == 'home' ? 'Home' : menu_selected == 'token' ? 'Token' : 'Daily Usage' }}</h1>
            </div>
            <div class="dropdown dropdown-end">
              <div tabindex="0" role="button" class="avatar">
                <div class="w-12 mask mask-squircle bg-orange-500">
                  <img :src="user_data.photoURL" alt="Photo Profile">
                </div>
              </div>
              <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
                <li><label for="request_modal">My Request</label></li>
                <li><a @click="changeTheme()">Change Theme</a></li>
                <li><a @click="onLogout()">Logout</a></li>
              </ul>
            </div>
          </div>
          <input type="checkbox" id="request_modal" class="modal-toggle" />
          <div class="modal" role="dialog">
            <div class="modal-box">
              <h3 class="font-bold text-lg">My Current Request</h3>
              <div class="overflow-x-auto mt-4">
                <table class="table">
                  <thead>
                    <tr>
                      <th>Request</th>
                      <th>Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(item, index) in requests" :key="index">
                      <td>{{ index }}</td>
                      <td>{{ item }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div class="modal-action">
                <label for="request_modal" class="btn w-full">Close</label>
              </div>
            </div>
          </div>
          <div class="grid grid-cols-3 gap-x-3 max-w-md mx-auto p-3 rounded-xl bg-base-200 mt-5">
            <div class="w-full">
              <button @click="menu_selected = 'home'" :class="{'bg-base-300': menu_selected != 'home', 'bg-orange-500 hover:bg-orange-600 text-white': menu_selected == 'home'}" class="btn w-full">Home</button>
            </div>
            <div class="w-full">
              <button @click="menu_selected = 'token'" :class="{'bg-base-300': menu_selected != 'token', 'bg-orange-500 hover:bg-orange-600 text-white': menu_selected == 'token'}" class="btn w-full">Token</button>
            </div>
            <div class="w-full">
              <button @click="menu_selected = 'daily'" :class="{'bg-base-300': menu_selected != 'daily', 'bg-orange-500 hover:bg-orange-600 text-white': menu_selected == 'daily'}" class="btn w-full">Daily Usage</button>
            </div>
          </div>
          
          <div id="home" v-if="menu_selected == 'home'">
            <div class="w-full mt-5 bg-orange-500/10 w-full p-6 rounded-xl text-orange-500">
              <h1 class="font-bold mb-4">For your information</h1>
              <p class="text-orange-500/60">When you clicked the pads button the robot XY will clicked the buttons same with button’s you clicked</p>
            </div>

            <div class="grid md:grid-cols-2 grid-cols-1 gap-4">
              <div class="mx-auto max-w-md bg-base-200 w-full p-6 mt-6 rounded-xl relative">
                <div class="absolute -top-3 right-0 p-3 bg-orange-500/20 backdrop-blur-md text-orange-500 rounded-xl" v-if="kwh_updated_at != null">{{ kwh_updated_at }}</div>
                <div class="grid grid-cols-6 gap-4 items-center">
                  <div class="col-span-4">
                    <div class="w-full p-3 bg-base-300 h-24 rounded-lg overflow-hidden">
                      <div class="flex items-center justify-between">
                        <h6 v-if="number == null || number == ''">0{{ kwh.toString().replace('.', '').length }}</h6>
                        <h6 v-else>{{ number.length < 10 ? '0' : '' }}{{ number.length }}</h6>
                        <h6>kWH</h6>
                      </div>
                      <div class="flex mt-3 justify-end">
                        <h1 v-if="number == null || number == ''" class="text-5xl font-bold">{{ reformatNumber(kwh, '.') }}</h1>
                        <h1 v-else class="text-5xl font-bold text-right">{{ reformatNumber(number, '') }}</h1>
                      </div>
                    </div>
                    <div class="grid grid-cols-3 mt-3">
                      <div class="text-center">
                        <div class="inline-block w-4 h-4 rounded-full bg-base-300"></div> <br>
                        <span class="text-xs">1600imp/kWH</span>
                      </div>
                      <div class="text-center">
                        <div class="inline-block w-4 h-4 rounded-full bg-base-300"></div> <br>
                        <span class="text-xs">Warning</span>
                      </div>
                      <div class="text-center">
                        <div class="inline-block w-4 h-4 rounded-full bg-base-300"></div> <br>
                        <span class="text-xs">Credit</span>
                      </div>
                    </div>
                  </div>
                  <div class="col-span-2 flex justify-end">
                    <div class="w-24 h-24 bg-orange-500 rounded-full flex items-center justify-center">
                      <div class="w-12 h-12 bg-orange-800 rounded-full"></div>
                    </div>
                  </div>
                </div>
                <div class="flex justify-between w-full mt-3 items-center">
                  <div class="flex items-center gap-4">
                    <img src="/pln.png" class="w-12" alt="Logo PENS">
                    <img src="/pens.png" class="w-12" alt="Logo PENS">
                  </div>
                  <div>
                    <div class="p-2 bg-white rounded">
                      <img src="/barcode.png" alt="Dummy barcode">
                    </div>
                  </div>
                </div>
              </div>
              <div class="mt-6 max-w-md mx-auto w-full">
                <div class="grid grid-cols-3 gap-4">
                  <div>
                    <button @click="setNumber(1)" class="w-full btn bg-white hover:bg-white/90 white-button-shadowed text-black text-2xl">1</button>
                  </div>
                  <div>
                    <button @click="setNumber(2)" class="w-full btn bg-white hover:bg-white/90 white-button-shadowed text-black text-2xl">2</button>
                  </div>
                  <div>
                    <button @click="setNumber(3)" class="w-full btn bg-white hover:bg-white/90 white-button-shadowed text-black text-2xl">3</button>
                  </div>
                  <div>
                    <button @click="setNumber(4)" class="w-full btn bg-white hover:bg-white/90 white-button-shadowed text-black text-2xl">4</button>
                  </div>
                  <div>
                    <button @click="setNumber(5)" class="w-full btn bg-white hover:bg-white/90 white-button-shadowed text-black text-2xl">5</button>
                  </div>
                  <div>
                    <button @click="setNumber(6)" class="w-full btn bg-white hover:bg-white/90 white-button-shadowed text-black text-2xl">6</button>
                  </div>
                  <div>
                    <button @click="setNumber(7)" class="w-full btn bg-white hover:bg-white/90 white-button-shadowed text-black text-2xl">7</button>
                  </div>
                  <div>
                    <button @click="setNumber(8)" class="w-full btn bg-white hover:bg-white/90 white-button-shadowed text-black text-2xl">8</button>
                  </div>
                  <div>
                    <button @click="setNumber(9)" class="w-full btn bg-white hover:bg-white/90 white-button-shadowed text-black text-2xl">9</button>
                  </div>
                  <div>
                    <button @click="setNumber(-1)" class="w-full btn bg-base-300 hover:bg-base-300/90 gray-button-shadowed text-2xl">
                      <Icon icon="mingcute:arrow-left-fill" />
                    </button>
                  </div>
                  <div>
                    <button @click="setNumber(0)" class="w-full btn bg-white hover:bg-white/90 white-button-shadowed text-black text-2xl">0</button>
                  </div>
                  <div>
                    <button @click="setNumber('Enter')" class="w-full btn bg-orange-500 hover:bg-orange-500/90 orange-button-shadowed text-white text-2xl">
                      <Icon icon="fluent:arrow-enter-left-24-filled" />
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div id="token" v-if="menu_selected == 'token'">
            <div class="w-full bg-base-200 p-6 rounded-xl mt-4">
              <h6 class="font-bold mb-6">My Token</h6>
              <div class="flex items-center justify-end gap-3">
                <h1 class="text-2xl text-orange-500 font-bold">{{ token }}</h1> 
                <button @click="onCopyToken()" class="btn bg-base-300 active:bg-green-500 focus:bg-green-500 focus:text-white btn-sm">copy</button>
              </div>
            </div>
          </div>

          <div id="daily" v-if="menu_selected == 'daily'">
            <h6 class="font-bold mb-6 mt-4">Daily Usage History</h6>
            <div  v-if="Object.keys(histories).length > 0" class="grid grid-cols-2 gap-3">
              <div v-for="(item, index) in histories" :key="index">
                <div class="relative p-3 rounded-xl bg-base-200">
                  <h1 class="font-bold text-xl">{{ item }}</h1>
                  <div class="absolute right-0 bottom-0 p-3 text-sm text-base-content/60">{{ index }}</div>
                </div>
              </div>
            </div>
            <div v-else>
              <div role="alert" class="alert alert-error">
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>Daily Usahe Not Found</span>
              </div>
            </div>
          </div>
          
        </div>
      </div>
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonContent, IonPage } from '@ionic/vue';
import { onMounted, Ref, ref } from 'vue';
import { useRouter } from 'vue-router';
import { Icon } from '@iconify/vue'
import { database } from '@/firebase'
import { onValue, set, ref as dbRef, get } from 'firebase/database'

const router = useRouter()
const user_data: any = ref({
  photoURL: 'pln.png'
})

const kwh: Ref<any> = ref(0)
const number: Ref<any> = ref(null)
const kwh_updated_at: Ref<any> = ref(null)
const menu_selected: Ref<string> = ref('daily')
const token: Ref<any> = ref(null)
const histories: Ref<any> = ref([])
const requests: Ref<any> = ref({})

onMounted(() => {
  const user = JSON.parse(sessionStorage.getItem('user')!)
  if(user == null) router.replace({path: '/'})
  else user_data.value = user

  if(user_data.value.photoURL == null || user_data.value.photoURL == undefined) user_data.value.photoURL = 'https://i.pravatar.cc/300'

  let localTheme = sessionStorage.getItem('theme') || 'dark'
  if(localTheme == 'dark') document.documentElement.setAttribute('data-theme', 'dark')
  else document.documentElement.setAttribute('data-theme', 'light')
  console.log(localTheme)

  fetchData('data/balances')
  fetchData('data/lastUpdateBalances')
  fetchData('token/token')
  fetchData('dailyUsage')
  fetchData('request')
})

const onCopyToken = async() => {
  if(token.value != null) await navigator.clipboard.writeText(token.value)
}

const reformatNumber = (value: any, separator: any) => {
  return value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, separator);
}

const onLogout = async() => {
  sessionStorage.removeItem('token')
  sessionStorage.removeItem('user')
  router.replace({path: '/'})
}

const fetchData = async(path: any) => {
  const dataRef = dbRef(database, path)
  onValue(dataRef, (snapshot) => {
    if(snapshot.exists()) {
      if(path == 'data/balances') kwh.value = snapshot.val()
      if(path == 'data/lastUpdateBalances') kwh_updated_at.value = snapshot.val()
      if(path == 'token/token') token.value = snapshot.val()
      if(path == 'dailyUsage') histories.value = snapshot.val()
      if(path == 'request') requests.value = snapshot.val()
    } else {
      if(path == 'data/balances') kwh.value = 0
      if(path == 'data/lastUpdateBalances') kwh_updated_at.value = null
      if(path == 'token/token') token.value = null
      if(path == 'dailyUsage') histories.value = []
      if(path == 'request') requests.value = []
    }
  })
}

const setNumber = async(value: any) => {
  if(number.value == null) number.value = ''
  let number_string = number.value.toString()
  if(value == 'Enter') {
    number.value = null
    try {
      await set(dbRef(database, 'number'), 'enter ')
    } catch(error) {
      console.error('Error saving data: ', error)
    }
    return false
  }
  if(value == -1) {
    if(number_string.length == 1) number.value = null
    else {
      let deleted_last_char = number_string.slice(0, value)
      number.value = deleted_last_char
    }
    saveData()
    return false
  }
  let new_number_string = number_string + value.toString()
  number.value = new_number_string
  saveData()
}

const saveData = async() => {
  try {
    await set(dbRef(database, 'number'), number.value)
  } catch(error) {
    console.error('Error saving data: ', error)
  }
}

const changeTheme = () => {
  let localTheme = sessionStorage.getItem('theme') || 'dark'
  if(localTheme == 'dark') {
    document.documentElement.setAttribute('data-theme', 'light')
    sessionStorage.setItem('theme', 'light')
  } 
  else {
    document.documentElement.setAttribute('data-theme', 'dark')
    sessionStorage.setItem('theme', 'dark')
  }
}

</script>

<style scoped>
.white-button-shadowed {
  box-shadow: 0px 7px 0px gray;
  position: relative;
}
.white-button-shadowed:active {
  box-shadow: 0px 1px 0px gray;
  top: 7px;
}
.gray-button-shadowed {
  box-shadow: 0px 7px 0px rgb(8, 9, 24);
  position: relative;
}
.gray-button-shadowed:active {
  box-shadow: 0px 1px 0px rgb(8, 9, 24);
  top: 7px;
}
.orange-button-shadowed {
  box-shadow: 0px 7px 0px rgb(125, 54, 3);
  position: relative;
}
.orange-button-shadowed:active {
  box-shadow: 0px 1px 0px rgb(125, 54, 3);
  top: 7px;
}
</style>