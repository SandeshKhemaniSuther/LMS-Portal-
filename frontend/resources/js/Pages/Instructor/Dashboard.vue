<template>
    <div class="min-h-screen bg-gray-50">
        <!-- Navigation -->
        <nav class="bg-white shadow-sm border-b">
            <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div class="flex justify-between h-16">
                    <div class="flex items-center">
                        <h1 class="text-xl font-semibold text-gray-900">LMS Portal - Instructor Dashboard</h1>
                    </div>
                    <div class="flex items-center space-x-4">
                        <span class="text-sm text-gray-700">{{ instructorName }}</span>
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
                        Welcome, {{ instructorName }}! 🎓
                    </h2>
                    <p class="text-gray-600">Manage your courses and track student progress</p>
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
                                    <dt class="text-sm font-medium text-gray-500 truncate">Total Courses</dt>
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
                                <UserGroupIcon class="h-6 w-6 text-green-600" />
                            </div>
                            <div class="ml-5 w-0 flex-1">
                                <dl>
                                    <dt class="text-sm font-medium text-gray-500 truncate">Total Students</dt>
                                    <dd class="text-lg font-medium text-gray-900">{{ stats.students }}</dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="bg-white overflow-hidden shadow rounded-lg">
                    <div class="p-5">
                        <div class="flex items-center">
                            <div class="flex-shrink-0">
                                <StarIcon class="h-6 w-6 text-yellow-600" />
                            </div>
                            <div class="ml-5 w-0 flex-1">
                                <dl>
                                    <dt class="text-sm font-medium text-gray-500 truncate">Average Rating</dt>
                                    <dd class="text-lg font-medium text-gray-900">{{ stats.rating }}/5</dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="bg-white overflow-hidden shadow rounded-lg">
                    <div class="p-5">
                        <div class="flex items-center">
                            <div class="flex-shrink-0">
                                <CurrencyDollarIcon class="h-6 w-6 text-red-600" />
                            </div>
                            <div class="ml-5 w-0 flex-1">
                                <dl>
                                    <dt class="text-sm font-medium text-gray-500 truncate">Earnings</dt>
                                    <dd class="text-lg font-medium text-gray-900">₹{{ stats.earnings }}</dd>
                                </dl>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- My Courses -->
            <div class="bg-white shadow rounded-lg mb-6">
                <div class="px-4 py-5 sm:p-6">
                    <div class="flex justify-between items-center mb-4">
                        <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">My Courses</h3>
                        <button class="bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700 text-sm">
                            + Create New Course
                        </button>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        <div v-for="course in courses" :key="course.id" class="border rounded-lg p-4 hover:shadow-md transition-shadow">
                            <img :src="course.thumbnail || '/placeholder-course.jpg'" :alt="course.title" class="w-full h-32 object-cover rounded-md mb-3">
                            <h4 class="font-semibold text-gray-900 mb-2">{{ course.title }}</h4>
                            <p class="text-sm text-gray-600 mb-3">{{ course.description }}</p>
                            <div class="flex justify-between items-center mb-3">
                                <span class="text-sm text-gray-500">{{ course.students }} students</span>
                                <div class="flex items-center">
                                    <StarIcon class="h-4 w-4 text-yellow-400 mr-1" />
                                    <span class="text-sm text-gray-600">{{ course.rating }}</span>
                                </div>
                            </div>
                            <div class="flex space-x-2">
                                <button class="flex-1 bg-blue-600 text-white py-2 px-3 rounded-md hover:bg-blue-700 text-sm">
                                    Edit
                                </button>
                                <button class="flex-1 bg-gray-200 text-gray-700 py-2 px-3 rounded-md hover:bg-gray-300 text-sm">
                                    View
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Recent Student Activity -->
            <div class="bg-white shadow rounded-lg">
                <div class="px-4 py-5 sm:p-6">
                    <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">Recent Student Activity</h3>
                    <div class="space-y-4">
                        <div v-for="activity in recentActivity" :key="activity.id" class="flex items-center justify-between border-b pb-3">
                            <div class="flex items-center space-x-3">
                                <div class="flex-shrink-0">
                                    <div class="h-8 w-8 rounded-full bg-blue-100 flex items-center justify-center">
                                        <UserIcon class="h-4 w-4 text-blue-600" />
                                    </div>
                                </div>
                                <div>
                                    <p class="text-sm text-gray-900">{{ activity.student }} - {{ activity.action }}</p>
                                    <p class="text-xs text-gray-500">{{ activity.course }}</p>
                                </div>
                            </div>
                            <span class="text-xs text-gray-500">{{ activity.time }}</span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import { BookOpenIcon, UserGroupIcon, StarIcon, CurrencyDollarIcon, UserIcon } from '@heroicons/vue/outline'

export default {
    components: {
        BookOpenIcon,
        UserGroupIcon,
        StarIcon,
        CurrencyDollarIcon,
        UserIcon,
    },
    
    data() {
        return {
            instructorName: 'अमित शर्मा',
            stats: {
                courses: 8,
                students: 245,
                rating: 4.7,
                earnings: 45600
            },
            courses: [
                {
                    id: 1,
                    title: 'Python प्रोग्रामिंग शुरुआती',
                    description: 'Python सीखने के लिए सबसे अच्छा कोर्स',
                    students: 89,
                    rating: 4.8,
                    thumbnail: null
                },
                {
                    id: 2,
                    title: 'Web डेवलपमेंट बेसिक्स',
                    description: 'HTML, CSS, और JavaScript की नींव',
                    students: 67,
                    rating: 4.6,
                    thumbnail: null
                },
                {
                    id: 3,
                    title: 'डेटाबेस फंडामेंटल्स',
                    description: 'SQL और डेटाबेस प्रबंधन सीखें',
                    students: 45,
                    rating: 4.5,
                    thumbnail: null
                }
            ],
            recentActivity: [
                {
                    id: 1,
                    student: 'राज कुमार',
                    action: 'असाइनमेंट सबमिट किया',
                    course: 'Python प्रोग्रामिंग शुरुआती',
                    time: '10 मिनट पहले'
                },
                {
                    id: 2,
                    student: 'प्रिया सिंह',
                    action: 'कोर्स पूरा किया',
                    course: 'Web डेवलपमेंट बेसिक्स',
                    time: '1 घंटा पहले'
                },
                {
                    id: 3,
                    student: 'अजय कुमार',
                    action: 'क्विज में 95% स्कोर',
                    course: 'डेटाबेस फंडामेंटल्स',
                    time: '2 घंटे पहले'
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
