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
            },
            {
                path: 'users',
                component: () => import("../components/settings/UserAccess.vue"),
                meta: {
                    name: "Пользователи"
                }
            }
        ]
    }
]

const listsRoutes: RouteRecordRaw[] = [
    {
        path: "/lists",
        component: MainLayout,
        children: [
            {
                path: "retail_stores",
                component: () => import("../components/lists/RetailStores.vue"),
                meta: {
                    name: "Точки продаж"
                }
            },
            {
                path: "payment_purposes",
                component: () => import("../components/lists/PaymentPurpose.vue"),
                meta: {
                    name: "Назначения платежа"
                }
            },
            {
                path: "bonuses",
                component: () => import("../components/lists/Bonuses.vue"),
                meta: {
                    name: "Премии"
                }
            }
        ]
    }
]

const testRoutes: RouteRecordRaw[] = [
    {
        path: "/tests",
        component: MainLayout,
        children: [
            {
                path: '',
                component: () => import("../components/tests/TestsPage.vue"),
                meta: {
                    name: "Тестирования"
                }
            },
            {
                path: 'result',
                component: () => import("../components/tests/TestResult.vue"),
                meta: {
                    name: "Результаты тестирований"
                }
            },
            {
                path: 'create',
                component: () => import("../components/tests/admin/TestCreatePage.vue"),
                meta: {
                    name: "Добавление тестирования"
                }
            },
            {
                name: 'TestEdit',
                path: 'edit',
                component: () => import('../components/tests/admin/TestEditPage.vue'),
                meta: {
                    name: 'Редактирование теста'
                }
            },
        ]
    }
]

const reportRoutes: RouteRecordRaw[] = [
    {
        path: '/reports',
        component: MainLayout,
        children: [
            {
                path: 'auditor',
                component: () =>  import("../components/reports/Auditor.vue"),
                meta: {
                    name: "Ревизор"
                }
            },
            {
                path: 'sales-journal',
                component: () => import("../components/reports/SalesJournal.vue"),
                meta: {
                    name: "Журнал продаж"
                }
            },
            {
                path: 'payment-journal',
                component: () => import("../components/reports/PaymentJournal.vue"),
                meta: {
                    name: "Журнал платежей"
                }
            }
        ]
    }
]

const errorRoutes: RouteRecordRaw[] = [
    {
        path: '/error',
        component: MainLayout,
        children: [
            {
                path: 'access_denied',
                component: () => import("../components/errors/AccessDenied.vue"),
            },
            {
                path: 'not_found',
                component: () => import("../components/errors/PageNotFound.vue"),
            }
        ]
    }
]

const inventoryRoutes: RouteRecordRaw[] = [
    {
        path: '/error',
        component: MainLayout,
        children: [
        ]
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
        ...listsRoutes,
        ...reportRoutes,
        ...settingsRoutes,
        ...errorRoutes,
        ...testRoutes,
        ...inventoryRoutes
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