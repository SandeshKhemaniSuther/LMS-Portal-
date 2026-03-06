// Simple Vue.js app for LMS Portal
const { createApp, ref } = Vue;
const { createRouter, createWebHistory } = VueRouter;

// Components
const Login = {
    template: `
    <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
        <div class="max-w-md w-full space-y-8">
            <div>
                <div class="mx-auto h-12 w-12 flex items-center justify-center rounded-full bg-blue-100">
                    <svg class="h-8 w-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"></path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z"></path>
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 14l9-5-9-5-9 5 9 5z"></path>
                    </svg>
                </div>
                <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
                    Sign in to LMS Portal
                </h2>
                <p class="mt-2 text-center text-sm text-gray-600">
                    Or
                    <a href="/register" class="font-medium text-blue-600 hover:text-blue-500">
                        create a new account
                    </a>
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

            <form @submit.prevent="login" class="mt-8 space-y-6">
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
                            <svg class="h-5 w-5 text-blue-500 group-hover:text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z"></path>
                            </svg>
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
    `,
    setup() {
        const userType = ref('student');
        const form = ref({
            email: '',
            password: '',
            remember: false
        });
        const loading = ref(false);
        const error = ref(null);
        
        const userTypes = [
            { value: 'student', label: 'Student' },
            { value: 'instructor', label: 'Teacher' },
            { value: 'admin', label: 'Admin' }
        ];

        const login = async () => {
            loading.value = true;
            error.value = null;
            
            // Simulate API call
            setTimeout(() => {
                localStorage.setItem('token', 'demo-token');
                localStorage.setItem('userType', userType.value);
                
                const routes = {
                    student: '/student/dashboard',
                    instructor: '/instructor/dashboard',
                    admin: '/admin/dashboard'
                };
                
                router.push(routes[userType.value]);
                loading.value = false;
            }, 1000);
        };

        const quickLogin = (type) => {
            const demoCredentials = {
                student: { email: 'student@lms.com', password: 'password123' },
                instructor: { email: 'teacher@lms.com', password: 'password123' },
                admin: { email: 'admin@lms.com', password: 'password123' }
            };
            
            form.value = demoCredentials[type];
            userType.value = type;
            login();
        };

        return {
            userType,
            form,
            loading,
            error,
            userTypes,
            login,
            quickLogin
        };
    }
};

// Router
const routes = [
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login, name: 'login' },
    { path: '/student/dashboard', component: Login, name: 'student.dashboard' },
    { path: '/instructor/dashboard', component: Login, name: 'instructor.dashboard' },
    { path: '/admin/dashboard', component: Login, name: 'admin.dashboard' },
    { path: '/:pathMatch(.*)*', redirect: '/login' }
];

const router = createRouter({
    history: createWebHistory(),
    routes
});

// App
const app = createApp({});
app.use(router);
app.mount('#app');
