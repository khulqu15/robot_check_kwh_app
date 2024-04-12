<template>
  <ion-page>
    <ion-content :fullscreen="true">
      <div class="w-full relative md:p-12 p-6 bg-base-100 overflow-x-hidden text-base-content">
        <div class="min-h-screen">
          <div class="flex w-full items-center justify-between">
            <div class="flex justify-start items-center gap-3">
              <img src="/flash.png" class="w-10" alt="Lighting Logo">
              <h1 class="text-xl font-bold">Home</h1>
            </div>
            <div class="dropdown dropdown-end">
              <div tabindex="0" role="button" class="avatar">
                <div class="w-12 mask mask-squircle bg-orange-500">
                  <img :src="user_data.photoURL" alt="Photo Profile">
                </div>
              </div>
              <ul tabindex="0" class="dropdown-content z-[1] menu p-2 shadow bg-base-100 rounded-box w-52">
                <li><a @click="changeTheme()">Change Theme</a></li>
                <li><a @click="onLogout()">Logout</a></li>
              </ul>
            </div>
          </div>
          <div class="w-full mt-5 bg-orange-500/10 w-full p-6 rounded-xl text-orange-500">
            <h1 class="font-bold mb-4">For your information</h1>
            <p class="text-orange-500/60">When you clicked the pads button the robot XY will clicked the buttons same with button’s you clicked</p>
          </div>
          <div class="mx-auto max-w-md bg-base-200 w-full p-6 mt-6 rounded-xl">
            <div class="grid grid-cols-6 gap-4 items-center">
              <div class="col-span-4">
                <div class="w-full p-3 bg-base-300 h-24 rounded-lg">
                  <div class="flex items-center justify-between">
                    <h6>01</h6>
                    <h6>kWH</h6>
                  </div>
                  <div class="flex mt-3 justify-end overflow-x-auto">
                    <h1 v-if="number == null || number == ''" class="text-4xl font-bold">{{ kwh }}</h1>
                    <h1 v-else class="text-4xl font-bold">{{ number }}</h1>
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
          <div class="mt-6">
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
    </ion-content>
  </ion-page>
</template>

<script setup lang="ts">
import { IonContent, IonPage } from '@ionic/vue';
import { onMounted, Ref, ref } from 'vue';
import { useRouter } from 'vue-router';
import { Icon } from '@iconify/vue'
import { database } from '@/firebase'
import { set, ref as dbRef } from 'firebase/database'

const router = useRouter()
const user_data: any = ref({
  photoURL: 'pln.png'
})

const kwh: Ref<number> = ref(3100)
const number: Ref<any> = ref(null)

onMounted(() => {
  const user = JSON.parse(sessionStorage.getItem('user')!)
  if(user == null) router.replace({path: '/'})
  else user_data.value = user

  if(user_data.value.photoURL == null || user_data.value.photoURL == undefined) user_data.value.photoURL = 'https://i.pravatar.cc/300'

  let localTheme = sessionStorage.getItem('theme') || 'dark'
  if(localTheme == 'dark') document.documentElement.setAttribute('data-theme', 'dark')
  else document.documentElement.setAttribute('data-theme', 'light')
  console.log(localTheme)
})

const onLogout = async() => {
  sessionStorage.removeItem('token')
  sessionStorage.removeItem('user')
  router.replace({path: '/'})
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
    console.log(number.value)
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