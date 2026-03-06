<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Navigation -->
        <nav class="bg-white shadow-sm border-b">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between h-16">
                    <div class="flex items-center">
                        <h1 class="text-xl font-semibold text-gray-900">LMS Portal - Admin Dashboard</h1>
                    </div>
                    <div class="flex items-center space-x-4">
                        <span class="text-sm text-gray-700">{{ adminName }}</span>
                        <button @click="logout" class="text-red-600 hover:text-red-800 text-sm">
                            Logout
                        </button>
                    </div>
                </div>
            </div>
        </nav>

        <div class="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
            <!-- Welcome Section -->
            <div class="bg-white overflow-hidden shadow rounded-lg mb-6">
                <div class="px-4 py-5 sm:p-6">
                    <h2 class="text-2xl font-bold text-gray-900 mb-2">
                        Welcome, {{ adminName }}! ⚡
                    </h2>
                    <p class="text-gray-600">Manage and monitor the entire LMS system</p>
                </div>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
                <div class="bg-white overflow-hidden shadow rounded-lg">
                    <div class="p-5">
                        <div class="flex items-center">
                            <div class="flex-shrink-0">
                                <UserGroupIcon class="h-6 w-6 text-blue-600" />
                            </div>
                            <div class="ml-5 w-0 flex-1">
                                <dl>
                                    <dt class="text-sm font-medium text-gray-500 truncate">Total Users</dt>
                                    <dd class="text-lg font-medium text-gray-900">{{ stats.totalUsers }}</dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="bg-white overflow-hidden shadow rounded-lg">
                    <div class="p-5">
                        <div class="flex items-center">
                            <div class="flex-shrink-0">
                                <BookOpenIcon class="h-6 w-6 text-green-600" />
                            </div>
                            <div class="ml-5 w-0 flex-1">
                                <dl>
                                    <dt class="text-sm font-medium text-gray-500 truncate">Total Courses</dt>
                                    <dd class="text-lg font-medium text-gray-900">{{ stats.totalCourses }}</dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="bg-white overflow-hidden shadow rounded-lg">
                    <div class="p-5">
                        <div class="flex items-center">
                            <div class="flex-shrink-0">
                                <CurrencyDollarIcon class="h-6 w-6 text-yellow-600" />
                            </div>
                            <div class="ml-5 w-0 flex-1">
                                <dl>
                                    <dt class="text-sm font-medium text-gray-500 truncate">Total Revenue</dt>
                                    <dd class="text-lg font-medium text-gray-900">₹{{ stats.totalRevenue }}</dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="bg-white overflow-hidden shadow rounded-lg">
                    <div class="p-5">
                        <div class="flex items-center">
                            <div class="flex-shrink-0">
                                <TrendingUpIcon class="h-6 w-6 text-red-600" />
                            </div>
                            <div class="ml-5 w-0 flex-1">
                                <dl>
                                    <dt class="text-sm font-medium text-gray-500 truncate">Monthly Growth</dt>
                                    <dd class="text-lg font-medium text-gray-900">{{ stats.monthlyGrowth }}%</dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Quick Actions -->
            <div class="bg-white shadow rounded-lg mb-6">
                <div class="px-4 py-5 sm:p-6">
                    <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Quick Actions</h3>
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <button class="p-4 border rounded-lg hover:bg-gray-50 text-center">
                            <UserPlusIcon class="h-8 w-8 text-blue-600 mx-auto mb-2" />
                            <span class="text-sm text-gray-700">Add User</span>
                        </button>
                        <button class="p-4 border rounded-lg hover:bg-gray-50 text-center">
                            <PlusCircleIcon class="h-8 w-8 text-green-600 mx-auto mb-2" />
                            <span class="text-sm text-gray-700">Create Course</span>
                        </button>
                        <button class="p-4 border rounded-lg hover:bg-gray-50 text-center">
                            <ChartBarIcon class="h-8 w-8 text-yellow-600 mx-auto mb-2" />
                            <span class="text-sm text-gray-700">Reports</span>
                        </button>
                        <button class="p-4 border rounded-lg hover:bg-gray-50 text-center">
                            <CogIcon class="h-8 w-8 text-red-600 mx-auto mb-2" />
                            <span class="text-sm text-gray-700">Settings</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Recent Activities & Users Table -->
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Recent Activities -->
                <div class="bg-white shadow rounded-lg">
                    <div class="px-4 py-5 sm:p-6">
                        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Recent Activities</h3>
                        <div class="space-y-4">
                            <div v-for="activity in recentActivities" :key="activity.id" class="flex items-center space-x-3">
                                <div class="flex-shrink-0">
                                    <div :class="[
                                        'h-8 w-8 rounded-full flex items-center justify-center',
                                        activity.type === 'user' ? 'bg-blue-100' :
                                        activity.type === 'course' ? 'bg-green-100' :
                                        activity.type === 'payment' ? 'bg-yellow-100' : 'bg-gray-100'
                                    ]">
                                        <component :is="activity.icon" :class="[
                                            'h-4 w-4',
                                            activity.type === 'user' ? 'text-blue-600' :
                                            activity.type === 'course' ? 'text-green-600' :
                                            activity.type === 'payment' ? 'text-yellow-600' : 'text-gray-600'
                                        ]" />
                                    </div>
                                </div>
                                <div class="flex-1">
                                    <p class="text-sm text-gray-900">{{ activity.description }}</p>
                                    <p class="text-xs text-gray-500">{{ activity.time }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- New Users -->
                <div class="bg-white shadow rounded-lg">
                    <div class="px-4 py-5 sm:p-6">
                        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">New Users</h3>
                        <div class="space-y-4">
                            <div v-for="user in newUsers" :key="user.id" class="flex items-center justify-between">
                                <div class="flex items-center space-x-3">
                                    <div class="h-8 w-8 rounded-full bg-gray-200 flex items-center justify-center">
                                        <UserIcon class="h-4 w-4 text-gray-600" />
                                    </div>
                                    <div>
                                        <p class="text-sm text-gray-900">{{ user.name }}</p>
                                        <p class="text-xs text-gray-500">{{ user.email }}</p>
                                    </div>
                                </div>
                                <div class="text-right">
                                    <span :class="[
                                        'text-xs px-2 py-1 rounded-full',
                                        user.role === 'student' ? 'bg-blue-100 text-blue-700' :
                                        user.role === 'instructor' ? 'bg-green-100 text-green-700' :
                                        'bg-purple-100 text-purple-700'
                                    ]">
                                        {{ user.role }}
                                    </span>
                                    <p class="text-xs text-gray-500 mt-1">{{ user.joined }}</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { 
    UserGroupIcon, 
    BookOpenIcon, 
    CurrencyDollarIcon, 
    TrendingUpIcon,
    UserPlusIcon,
    PlusCircleIcon,
    ChartBarIcon,
    CogIcon,
    UserIcon,
    UserAddIcon,
    AcademicCapIcon,
    CreditCardIcon
} from '@heroicons/vue/outline'

export default {
    components: {
        UserGroupIcon,
        BookOpenIcon,
        CurrencyDollarIcon,
        TrendingUpIcon,
        UserPlusIcon,
        PlusCircleIcon,
        ChartBarIcon,
        CogIcon,
        UserIcon,
        UserAddIcon,
        AcademicCapIcon,
        CreditCardIcon,
    },
    
    data() {
        return {
            adminName: 'एडमिन',
            stats: {
                totalUsers: 1250,
                totalCourses: 45,
                totalRevenue: 245000,
                monthlyGrowth: 12.5
            },
            recentActivities: [
                {
                    id: 1,
                    description: 'नया छात्र रजिस्टर हुआ: राज कुमार',
                    time: '5 मिनट पहले',
                    type: 'user',
                    icon: UserAddIcon
                },
                {
                    id: 2,
                    description: 'नया कोर्स पब्लिश: React.js एडवांस्ड',
                    time: '1 घंटा पहले',
                    type: 'course',
                    icon: AcademicCapIcon
                },
                {
                    id: 3,
                    description: 'पेमेंट प्राप्त: ₹2999',
                    time: '2 घंटे पहले',
                    type: 'payment',
                    icon: CreditCardIcon
                },
                {
                    id: 4,
                    description: 'नया इंस्ट्रक्टर जुड़ा: डॉ. प्रिया सिंह',
                    time: '3 घंटे पहले',
                    type: 'user',
                    icon: UserAddIcon
                }
            ],
            newUsers: [
                {
                    id: 1,
                    name: 'राज कुमार',
                    email: 'raj@example.com',
                    role: 'student',
                    joined: '2 घंटे पहले'
                },
                {
                    id: 2,
                    name: 'प्रिया सिंह',
                    email: 'priya@example.com',
                    role: 'instructor',
                    joined: '5 घंटे पहले'
                },
                {
                    id: 3,
                    name: 'अमित शर्मा',
                    email: 'amit@example.com',
                    role: 'student',
                    joined: '1 दिन पहले'
                }
            ]
        }
    },
    
    methods: {
        logout() {
            localStorage.removeItem('token')
            localStorage.removeItem('userType')
            window.location.href = '/login'
        }
    }
}
</script>
