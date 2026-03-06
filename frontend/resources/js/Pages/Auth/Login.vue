<template>
    <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md w-full space-y-8">
            <div>
                <div class="mx-auto h-12 w-12 flex items-center justify-center rounded-full bg-blue-100">
                    <AcademicCapIcon class="h-8 w-8 text-blue-600" />
                </div>
                <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
                    Sign in to LMS Portal
                </h2>
                <p class="mt-2 text-center text-sm text-gray-600">
                    Or
                    <Link href="/register" class="font-medium text-blue-600 hover:text-blue-500">
                        create a new account
                    </Link>
                </p>
            </div>
            
            <!-- User Type Selection -->
            <div class="mt-6">
                <label class="block text-sm font-medium text-gray-700 mb-2">
                    Select Login Type
                </label>
                <div class="grid grid-cols-3 gap-2">
                    <button
                        v-for="type in userTypes"
                        :key="type.value"
                        @click="userType = type.value"
                        :class="[
                            'px-3 py-2 text-sm font-medium rounded-md border transition-colors',
                            userType === type.value
                                ? 'bg-blue-600 text-white border-blue-600'
                                : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
                        ]"
                    >
                        {{ type.label }}
                    </button>
                </div>
            </div>

            <form class="mt-8 space-y-6" @submit.prevent="login">
                <div class="rounded-md shadow-sm -space-y-px">
                    <div>
                        <label for="email" class="sr-only">Email address</label>
                        <input
                            id="email"
                            name="email"
                            type="email"
                            autocomplete="email"
                            required
                            v-model="form.email"
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                            placeholder="Email address"
                        />
                    </div>
                    <div>
                        <label for="password" class="sr-only">Password</label>
                        <input
                            id="password"
                            name="password"
                            type="password"
                            autocomplete="current-password"
                            required
                            v-model="form.password"
                            class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                            placeholder="Password"
                        />
                    </div>
                </div>

                <div class="flex items-center justify-between">
                    <div class="flex items-center">
                        <input
                            id="remember-me"
                            name="remember-me"
                            type="checkbox"
                            v-model="form.remember"
                            class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                        />
                        <label for="remember-me" class="ml-2 block text-sm text-gray-900">
                            Remember me
                        </label>
                    </div>

                    <div class="text-sm">
                        <a href="#" class="font-medium text-blue-600 hover:text-blue-500">
                            Forgot your password?
                        </a>
                    </div>
                </div>

                <div v-if="error" class="text-red-600 text-sm text-center">
                    {{ error }}
                </div>

                <div>
                    <button
                        type="submit"
                        :disabled="loading"
                        class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
                    >
                        <span class="absolute left-0 inset-y-0 flex items-center pl-3">
                            <LockClosedIcon class="h-5 w-5 text-blue-500 group-hover:text-blue-400" />
                        </span>
                        {{ loading ? 'Signing in...' : 'Sign in' }}
                    </button>
                </div>

                <!-- Quick Login Buttons for Demo -->
                <div class="mt-6 border-t pt-6">
                    <p class="text-sm text-gray-600 text-center mb-4">Demo Login:</p>
                    <div class="space-y-2">
                        <button
                            type="button"
                            @click="quickLogin('student')"
                            class="w-full px-4 py-2 bg-green-100 text-green-700 rounded-md hover:bg-green-200 text-sm"
                        >
                            Student Demo Login
                        </button>
                        <button
                            type="button"
                            @click="quickLogin('instructor')"
                            class="w-full px-4 py-2 bg-blue-100 text-blue-700 rounded-md hover:bg-blue-200 text-sm"
                        >
                            Teacher Demo Login
                        </button>
                        <button
                            type="button"
                            @click="quickLogin('admin')"
                            class="w-full px-4 py-2 bg-purple-100 text-purple-700 rounded-md hover:bg-purple-200 text-sm"
                        >
                            Admin Demo Login
                        </button>
                    </div>
                </div>
            </form>
        </div>
    </div>
</template>

<script>
import { Link } from '@inertiajs/inertia-vue3'
import { AcademicCapIcon, LockClosedIcon } from '@heroicons/vue/solid'

export default {
    components: {
        Link,
        AcademicCapIcon,
        LockClosedIcon,
    },
    
    data() {
        return {
            userType: 'student',
            form: {
                email: '',
                password: '',
                remember: false
            },
            loading: false,
            error: null,
            userTypes: [
                { value: 'student', label: 'Student' },
                { value: 'instructor', label: 'Teacher' },
                { value: 'admin', label: 'Admin' }
            ]
        }
    },
    
    methods: {
        async login() {
            this.loading = true
            this.error = null
            
            try {
                const response = await fetch('/api/v1/auth/login', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                    body: new URLSearchParams({
                        username: this.form.email,
                        password: this.form.password,
                    })
                })
                
                const data = await response.json()
                
                if (response.ok) {
                    localStorage.setItem('token', data.access_token)
                    localStorage.setItem('userType', this.userType)
                    
                    // Redirect based on user type
                    const routes = {
                        student: '/student/dashboard',
                        instructor: '/instructor/dashboard',
                        admin: '/admin/dashboard'
                    }
                    
                    window.location.href = routes[this.userType]
                } else {
                    this.error = data.detail || 'Login failed. Please check your email and password.'
                }
            } catch (error) {
                this.error = 'Network error. Please try again later.'
            } finally {
                this.loading = false
            }
        },
        
        quickLogin(type) {
            const demoCredentials = {
                student: { email: 'student@lms.com', password: 'password123' },
                instructor: { email: 'teacher@lms.com', password: 'password123' },
                admin: { email: 'admin@lms.com', password: 'password123' }
            }
            
            this.userType = type
            this.form.email = demoCredentials[type].email
            this.form.password = demoCredentials[type].password
            this.login()
        }
    }
}
</script>
