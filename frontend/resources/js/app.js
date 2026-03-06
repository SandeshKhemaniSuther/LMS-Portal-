import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import Login from './Pages/Auth/Login.vue'
import StudentDashboard from './Pages/Student/Dashboard.vue'
import InstructorDashboard from './Pages/Instructor/Dashboard.vue'
import AdminDashboard from './Pages/Admin/Dashboard.vue'
import './bootstrap'

// Routes
const routes = [
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login, name: 'login' },
    { path: '/student/dashboard', component: StudentDashboard, name: 'student.dashboard' },
    { path: '/instructor/dashboard', component: InstructorDashboard, name: 'instructor.dashboard' },
    { path: '/admin/dashboard', component: AdminDashboard, name: 'admin.dashboard' },
    { path: '/:pathMatch(.*)*', redirect: '/login' }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

// Authentication guard
router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('token')
    const userType = localStorage.getItem('userType')
    
    if (to.path !== '/login' && !token) {
        next('/login')
    } else if (to.path === '/login' && token) {
        // Redirect to appropriate dashboard based on user type
        const routes = {
            student: '/student/dashboard',
            instructor: '/instructor/dashboard',
            admin: '/admin/dashboard'
        }
        next(routes[userType] || '/login')
    } else if (to.path.startsWith('/student') && userType !== 'student') {
        next('/login')
    } else if (to.path.startsWith('/instructor') && userType !== 'instructor') {
        next('/login')
    } else if (to.path.startsWith('/admin') && userType !== 'admin') {
        next('/login')
    } else {
        next()
    }
})

const app = createApp({})
app.use(router)
app.mount('#app')
