<template>
    <ion-page>
        <ion-content :fullscreen="true">
            <div class="w-full relative md:px-12 px-8 bg-base-100 overflow-x-hidden text-base-content">
                <div class="min-h-screen flex items-center">
                    <div class="absolute left-0 w-full top-0 flex justify-center">
                        <img src="/image.png" class="lg:w-1/4 md:w-1/2 w-full scale-[1.2] md:scale-100" alt="KWH Meter Illustration">
                    </div>
                    <div class="w-full absolute top-0 p-8 gap-4 left-0 flex items-center justify-center justify-items-center">
                        <img src="/pln.png" class="w-12" alt="Logo PENS">
                        <img src="/pens.png" class="w-12" alt="Logo PENS">
                    </div>
                    <div class="relative top-72 mx-auto p-8 bg-base-200/70 backdrop-blur-md rounded-xl">
                        <h1 class="font-bold mb-2 text-2xl">Smart Control KWH Meter</h1>
                        <p>Monitor, Remote Control and Auto Detect your KWH Status in one app</p>
                        <button @click="googleLogin()" class="btn bg-orange-500 hover:bg-orange-600 w-full rounded-full mt-4 text-white">Login with Google</button>
                        <button @click="anonymousLogin()" class="btn btn-ghost w-full rounded-full mt-4x">Skip</button>
                    </div>
                </div>
            </div>
        </ion-content>
    </ion-page>
</template>

<script setup lang="ts">
import { IonContent, IonPage } from '@ionic/vue'
import { useRouter } from 'vue-router';
import { GoogleAuthProvider, signInWithPopup, signInAnonymously } from 'firebase/auth'
import { auth } from '@/firebase';

const router = useRouter()

const googleLogin = async() => {
    const provider = new GoogleAuthProvider()
    try {
        const result = await signInWithPopup(auth, provider)
        const credential = GoogleAuthProvider.credentialFromResult(result)
        const token = credential?.accessToken
        const user = result.user
        sessionStorage.setItem('token', token!)
        sessionStorage.setItem('user', JSON.stringify(user))
        router.push({name: 'Home'})
    } catch(error) {
        console.error('Error logging in with Google: ', error)
    }
}

const anonymousLogin = async() => {
    try {
        const result = await signInAnonymously(auth)
        const user = result.user
        sessionStorage.setItem('user', JSON.stringify(user))
        router.push({name: 'Home'})
    } catch(error) {
        console.error('Error logging in with Anonymous: ', error)
    }
}
</script>