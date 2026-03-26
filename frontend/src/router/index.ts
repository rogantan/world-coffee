import { createRouter, createWebHistory } from 'vue-router';
import type { RouteRecordRaw, Router } from 'vue-router';
import LoginLayout from '../components/layouts/LoginLayout.vue';
import MainLayout from '../components/layouts/MainLayout.vue';
import HomePage from '../components/HomePage.vue';

const loginRoutes: RouteRecordRaw[] = [
    {
        path: '/signin',
        component: LoginLayout,
        children: [
            {
                path: '',
                component: () => import("../views/auth/AuthorizationView.vue"),
            },
        ],
    }
]

const mainRoutes: RouteRecordRaw[] = [
    {
        path: '/main',
        component: MainLayout,
        meta: { requiresAuth: true },
        children: [
            {
                path: '',
                component: HomePage,
                meta: {
                    name: "Главная страница"
                }
            }
        ]
    }
]

const settingsRoutes: RouteRecordRaw[] = [
    {
        path: '/settings',
        component: MainLayout,
        meta: { requiresAuth: true },
        children: [
            {
                path: 'synch',
                component: () => import("../components/settings/Synchronization.vue"),
                meta: {
                    name: "Проверка синхронизации"
                }
            }
        ]
    }
]

const reportRoutes: RouteRecordRaw[] = [
    {
        path: '/reports',
        component: MainLayout,
        // children: [
        //     {
        //         path: '',
        //         meta: {
        //             name: "frf"
        //         }
        //     }
        // ]
    }
]

const router: Router = createRouter({
    history: createWebHistory(''),
    routes: [
        {
            path: "/",
            redirect: "/signin",
        },
        ...loginRoutes,
        ...mainRoutes,
        ...reportRoutes,
        ...settingsRoutes
    ]
});
router.beforeEach((to, from, next) => {
    const isAuthenticated = !!localStorage.getItem('token')

    if (to.matched.some(record => record.meta.requiresAuth) && !isAuthenticated) {
        return next('/signin')
    }

    next()
})
export default router;