<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Navigation -->
        <nav class="bg-white shadow-sm border-b">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between h-16">
                    <div class="flex items-center">
                        <h1 class="text-xl font-semibold text-gray-900">LMS Portal - Student Dashboard</h1>
                    </div>
                    <div class="flex items-center space-x-4">
                        <span class="text-sm text-gray-700">{{ studentName }}</span>
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
                        Welcome, {{ studentName }}! 👋
                    </h2>
                    <p class="text-gray-600">Continue your learning journey and acquire new skills</p>
                </div>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-6">
                <div class="bg-white overflow-hidden shadow rounded-lg">
                    <div class="p-5">
                        <div class="flex items-center">
                            <div class="flex-shrink-0">
                                <BookOpenIcon class="h-6 w-6 text-blue-600" />
                            </div>
                            <div class="ml-5 w-0 flex-1">
                                <dl>
                                    <dt class="text-sm font-medium text-gray-500 truncate">Courses</dt>
                                    <dd class="text-lg font-medium text-gray-900">{{ stats.courses }}</dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="bg-white overflow-hidden shadow rounded-lg">
                    <div class="p-5">
                        <div class="flex items-center">
                            <div class="flex-shrink-0">
                                <ClockIcon class="h-6 w-6 text-green-600" />
                            </div>
                            <div class="ml-5 w-0 flex-1">
                                <dl>
                                    <dt class="text-sm font-medium text-gray-500 truncate">Learning Hours</dt>
                                    <dd class="text-lg font-medium text-gray-900">{{ stats.hours }}</dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="bg-white overflow-hidden shadow rounded-lg">
                    <div class="p-5">
                        <div class="flex items-center">
                            <div class="flex-shrink-0">
                                <CheckCircleIcon class="h-6 w-6 text-yellow-600" />
                            </div>
                            <div class="ml-5 w-0 flex-1">
                                <dl>
                                    <dt class="text-sm font-medium text-gray-500 truncate">Completed</dt>
                                    <dd class="text-lg font-medium text-gray-900">{{ stats.completed }}</dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="bg-white overflow-hidden shadow rounded-lg">
                    <div class="p-5">
                        <div class="flex items-center">
                            <div class="flex-shrink-0">
                                <FireIcon class="h-6 w-6 text-red-600" />
                            </div>
                            <div class="ml-5 w-0 flex-1">
                                <dl>
                                    <dt class="text-sm font-medium text-gray-500 truncate">Streak</dt>
                                    <dd class="text-lg font-medium text-gray-900">{{ stats.streak }} days</dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- My Courses -->
            <div class="bg-white shadow rounded-lg mb-6">
                <div class="px-4 py-5 sm:p-6">
                    <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">My Courses</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        <div v-for="course in courses" :key="course.id" class="border rounded-lg p-4 hover:shadow-md transition-shadow">
                            <img :src="course.thumbnail || '/placeholder-course.jpg'" :alt="course.title" class="w-full h-32 object-cover rounded-md mb-3">
                            <h4 class="font-semibold text-gray-900 mb-2">{{ course.title }}</h4>
                            <p class="text-sm text-gray-600 mb-3">{{ course.description }}</p>
                            <div class="mb-3">
                                <div class="flex justify-between text-sm text-gray-600 mb-1">
                                    <span>Progress</span>
                                    <span>{{ course.progress }}%</span>
                                </div>
                                <div class="w-full bg-gray-200 rounded-full h-2">
                                    <div class="bg-blue-600 h-2 rounded-full" :style="`width: ${course.progress}%`"></div>
                                </div>
                            </div>
                            <button class="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 text-sm">
                                Continue
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Recent Activity -->
            <div class="bg-white shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                    <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Recent Activity</h3>
                    <div class="space-y-4">
                        <div v-for="activity in recentActivity" :key="activity.id" class="flex items-center space-x-3">
                            <div class="flex-shrink-0">
                                <component :is="activity.icon" class="h-5 w-5 text-gray-400" />
                            </div>
                            <div class="flex-1">
                                <p class="text-sm text-gray-900">{{ activity.description }}</p>
                                <p class="text-xs text-gray-500">{{ activity.time }}</p>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { BookOpenIcon, ClockIcon, CheckCircleIcon, FireIcon, PlayIcon, DocumentTextIcon } from '@heroicons/vue/outline'

export default {
    components: {
        BookOpenIcon,
        ClockIcon,
        CheckCircleIcon,
        FireIcon,
        PlayIcon,
        DocumentTextIcon,
    },
    
    data() {
        return {
            studentName: 'राज कुमार',
            stats: {
                courses: 5,
                hours: 24,
                completed: 2,
                streak: 7
            },
            courses: [
                {
                    id: 1,
                    title: 'Python प्रोग्रामिंग शुरुआती',
                    description: 'Python सीखने के लिए सबसे अच्छा कोर्स',
                    progress: 65,
                    thumbnail: null
                },
                {
                    id: 2,
                    title: 'Web डेवलपमेंट बेसिक्स',
                    description: 'HTML, CSS, और JavaScript की नींव',
                    progress: 30,
                    thumbnail: null
                },
                {
                    id: 3,
                    title: 'डेटाबेस फंडामेंटल्स',
                    description: 'SQL और डेटाबेस प्रबंधन सीखें',
                    progress: 85,
                    thumbnail: null
                }
            ],
            recentActivity: [
                {
                    id: 1,
                    description: 'Python कोर्स में "Functions" लेसन पूरा किया',
                    time: '2 घंटे पहले',
                    icon: CheckCircleIcon
                },
                {
                    id: 2,
                    description: 'Web डेवलपमेंट कोर्स में "CSS Basics" शुरू किया',
                    time: '5 घंटे पहले',
                    icon: PlayIcon
                },
                {
                    id: 3,
                    description: 'डेटाबेस असाइनमेंट सबमिट किया',
                    time: '1 दिन पहले',
                    icon: DocumentTextIcon
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
